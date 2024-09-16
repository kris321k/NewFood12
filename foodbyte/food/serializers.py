from rest_framework import serializers
from .models import Person,FoodItem,Category,Review,otp,Cart,CartItem,Order,OrderItem
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


user = get_user_model()


class Personserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phonenumer = serializers.IntegerField(required=False)
    address=serializers.CharField(required=False)


    class Meta:
        model = user
        fields = ['email', 'password', 'first_name', 'last_name','phonenumer','address']

    def validate(self, data):
        if 'email' in data and self.instance is None:
            if Person.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('Email already exists')
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = Person.objects.create(**validated_data)
        return user

    #def update(self, instance, validated_data):
    #for attr, value in validated_data.items():
    #        setattr(instance, attr, value)
    #    instance.save()
    #    return instance

class categoryserializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['category_name']




class foodserializer(serializers.ModelSerializer):
    class Meta:
        model=FoodItem
        fields=['item_name','item_desc','item_price','item_img']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields=['person','food_item','review_text','created_at','updated_at','is_paid','review']
    
class otpserializer(serializers.ModelSerializer):
    class Meta:
        model=otp
        fields=['otp_number','otp_created']
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields=['person','quantity','total_price']

class CartItemserializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['cart','fooditems','quantity']
        

class orderSerializer(serializers.ModelSerializer):
    created_at=serializers.CharField(required=False)
    status=serializers.CharField(required=False)
    class Meta:
        model=Order
        fields=['person','created_at','status']


class orderitemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['order','fooditem','quantity']
    
