from django.shortcuts import render
from .models import Person, Category,Order,FoodItem,otp,Cart,CartItem,OrderItem
from rest_framework.views import APIView
from .serializers import Personserializer,categoryserializer,foodserializer,ReviewSerializer,otpserializer,CartSerializer,CartItemserializer,orderSerializer,orderitemSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as django_login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,filters
from .models import Review
import random
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken


#functions to get the token for the user

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

#view r the signup
class submitData(APIView):
    def post(self, request):
        serialized_data = Personserializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response({'registration': 'success'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)

#view for the login
class login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({
                'login': 'failed',
                'message': 'Email and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if user:
            tokens = get_tokens_for_user(user)
            return Response({
                'login': 'success',
                'access_token': tokens['access'],  # Access the correct key 'access'
                'refresh_token': tokens['refresh']  # Access the correct key 'refresh'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'login': 'failed',
                'message': 'Invalid email or password.'
            }, status=status.HTTP_401_UNAUTHORIZED)
#view for logout


#view to add aditional details to the profile
class profile(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        serialized_data = Personserializer(user, data=request.data, partial=True)
        if serialized_data.is_valid():
            serialized_data.save()
            user.refresh_from_db()
            return Response({
                'message':'profile updated succesfully',
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_number': user.phonenumer,
                'email':user.email,
                'address':user.address
            }, status=status.HTTP_200_OK)
        
        else:
            return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request):
        user=request.user
        serialiazeddata=Personserializer(user)
        user.refresh_from_db()
        return Response({
            'data':serialiazeddata.data
        },status=status.HTTP_200_OK)
    
#api for displaying front end homepage

class home(APIView):
    #permission_classes=[IsAuthenticated]
    #permission_classes=[IsAuthenticated]
    
    def get(self,request):
        catergories=Category.objects.all()
        catergoryserializedata=categoryserializer(catergories, many=True)

        #code to popular food items
        Popularfooditems=[]
        PopularFooditemreview=Review.objects.filter(review__gte=2)[0:3]
        
        for eachreview in PopularFooditemreview:
            fooditemserializeddata=foodserializer(eachreview.food_item)
            Popularfooditems.append(fooditemserializeddata.data)
        
        return Response({
            'categories':catergoryserializedata.data,
            'popularitems':Popularfooditems
        },status=status.HTTP_200_OK)
    

class displayCategories(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,category_name):
        category=Category.objects.filter(category_name=category_name).first()
        Categoryfooditems=FoodItem.objects.filter(category=category)
        Categoryfooditemsserializedata=foodserializer(Categoryfooditems, many=True)
        return Response({
            'categoryfooditems':Categoryfooditemsserializedata.data
        })
    

class review(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,item_name):
        User=request.user
        food_item=FoodItem.objects.get(item_name=item_name)
        data=request.data.copy()
        data['food_item']=food_item.id
        data['person']=User.id
        serialized_review=ReviewSerializer(data=data)
        if serialized_review.is_valid():
            serialized_review.save()
            return Response({
                'data_submission':'success'
            })
        

    def get(self,request,item_name):
        user=request.user
        food_item=FoodItem.objects.get(item_name=item_name)
        if Review.objects.filter(food_item=food_item).exists():
            review=Review.objects.filter(food_item=food_item)
            serialized_review=ReviewSerializer(review, many=True)
            return Response({
                'reviews':serialized_review.data,
            })
        else:
            return Response({
                'empty':'no reviews'
            },status=status.HTTP_404_NOT_FOUND)
        
    
class Reviewpatch(APIView):

    def patch(self,request,item_name,review_id):
        user=request.user
        food_item=FoodItem.objects.get(item_name=item_name)
        review = Review.objects.get(person=user, food_item=food_item,id=review_id)
        serialized_review=ReviewSerializer(review,data=request.data, partial=True)
        if serialized_review.is_valid():
            serialized_review.save()
            return Response({
                'success':'updated successfully'
            }, status=status.HTTP_200_OK)
        
        

class ForgotPassword(APIView):
    def post(self,request):
        email=request.data['email']
        if Person.objects.filter(email=request.data['email']).exists():
            person=Person.objects.filter(email=email).first()
            otpn=random.randint(1000,9999)
            opt_num=otp(otp_number=otpn,person=person)
            opt_num.save()
            response = Response({
                'otp': opt_num.otp_number
            })

            #subject = 'otp'
            #message = f'Your OTP code for password reset is: {opt_num.otp_number}'
            #from_email = settings.DEFAULT_FROM_EMAIL
            #recipient_list = [email]

            
            #send_mail(subject, message, from_email, recipient_list)


            
            # Set the email in the cookie
            response.set_cookie(
                'email',
                email,
                httponly=True,  
                secure=True     
            )
            return response
        else:
            return Response({'error': 'Email does not exist'}, status=404)
    
class verifyOtp(APIView):
    def post(self,request):
        email=request.COOKIES['email']
        user=Person.objects.filter(email=email).first()
        if user:
            Otp=otp.objects.filter(person=user).last()
            if Otp.otp_number == request.data['otp_num']:
                django_login(request,user)
                return Response({
                    'login':'sucess'
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'false':'invalid otp'
                },status=status.HTTP_401_UNAUTHORIZED)
            


class Cartaccess(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,item_name):
        user=request.user
        #cart, created=Cart.objects.get_or_create(person=user,defaults={'quantity':0,'total_price':0})
        

        fooditem=FoodItem.objects.filter(item_name=item_name).first()
        if not fooditem:
            return Response({
                'failed':'true'
            },status=status.HTTP_400_BAD_REQUEST)
        
        cart, created=Cart.objects.get_or_create(person=user)
       
        
        cartitem, created1=CartItem.objects.get_or_create(cart=cart,fooditems=fooditem)
        
        cartitem.quantity+=1
        cartitem.save()
        cartItems=cart.cart_items.all()

        total_price=sum(item.fooditems.item_price*item.quantity for item in cartItems)
        total_quantity=sum(item.quantity for item in cartItems)

        cart.total_price=total_price
        cart.quantity=total_quantity
        cart.save()

        cartitemserialized=CartItemserializer(cartitem)
        cartserialized=CartSerializer(cart)

        return Response({
            'cartitems':cartitemserialized.data,
            'cartdata':cartserialized.data
        },status=status.HTTP_200_OK)
    

    def get(self,request,item_name=None):
        user=request.user
        cart,created=Cart.objects.get_or_create(person=user)

        if not cart.cart_items.exists():
            return Response({
                'display':'cart empty'
            },status=status.HTTP_200_OK)
        
        
        cartitems=cart.cart_items.all()
        cartitemsserialized=CartItemserializer(cartitems, many=True)
        cartserializeddata=CartSerializer(cart)

        food_items_details=[]

        for cartitem in cartitems:
            fooditem=foodserializer(cartitem.fooditems)
            food_items_details.append({
                'items_detailes':fooditem.data,
                'quantity':cartitem.quantity
            })

        return Response({
            'cart_items':cartitemsserialized.data,
            'fooditems':food_items_details,
            'cart_details':cartserializeddata.data
        },status=status.HTTP_200_OK)
    

    def delete(self,request,item_name):
        user=request.user
        cart=Cart.objects.filter(person=user).first()

        fooditem=FoodItem.objects.filter(item_name=item_name).first()

        cartitem=CartItem.objects.filter(cart=cart,fooditems=fooditem).first()
        cartitem.delete()

        if not cart.cart_items.exists():
            cart.total_price=0
            cart.quantity=0
            cart.save()
        else:
            cart.total_price=sum(item.fooditems.item_price*item.quantity for item in cart.cart_items.all())
            cart.quantity=sum(item.quantity for item in cart.cart_items.all())
            cart.save()

        return Response({
            'success':'item deleted successfully'
        },status=status.HTTP_200_OK)
    

class displayCart(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        cart=Cart.objects.filter(person=user).first()
        if not cart:
            return Response({
                'error':'cart not found with person'
            },status=status.HTTP_404_NOT_FOUND)
        serialized_cart=CartSerializer(cart)
 
        serialized_fooditems=foodserializer(cart.items.all(), many=True)
        return Response({
            'cart_data':serialized_cart.data, 
            'food_item_data':serialized_fooditems.data
            },status=status.HTTP_200_OK)
    

class OrderView(APIView):
    permission_classes=[IsAuthenticated]

    def post(self,request,item_name):
        user=request.user
        fooditem=FoodItem.objects.filter(item_name=item_name).first()
        data=request.data.copy()
        data['person']=user.id
        orderserialized=orderSerializer(data=data)
        if orderserialized.is_valid():
            orderserialized.save()









    






        
        



        



        


            
        



    
            
        
        




        
        

            
        

    






    
    
