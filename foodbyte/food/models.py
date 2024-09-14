from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManger

class Person(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=30)
    bio = models.CharField(max_length=40, blank=True, null=True)
    phonenumer=models.IntegerField(default=0000)
    address=models.TextField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManger()


    def __str__(self):
        return self.email

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category_name

class FoodItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    item_img = models.ImageField(upload_to='images/')
    item_name = models.CharField(max_length=15)
    item_desc = models.CharField(max_length=30)
    item_price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return self.item_name

class Cart(models.Model):
    person=models.OneToOneField(Person,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)
    total_price=models.IntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart=models.ForeignKey(Cart,related_name='cart_items',on_delete=models.CASCADE)
    fooditems=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)


class Order(models.Model):
    person=models.ForeignKey(Person,on_delete=models.CASCADE,related_name='ordereditems')
    created_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=200,default='pending')


class OrderItem(models.Model):
    
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    fooditem=models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)



class Review(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_reviews')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(max_length=500)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    is_paid=models.BooleanField(default=False)
    review=models.IntegerField()

    def __str__(self):
        return f"Review by {self.person.email} on {self.food_item.item_name}"


class otp(models.Model):
    person=models.ForeignKey(Person,on_delete=models.CASCADE,related_name='otp')
    #email=models.EmailField(max_length=254)
    otp_number=models.CharField(max_length=4)
    otp_created=models.DateTimeField(auto_now_add=True)

