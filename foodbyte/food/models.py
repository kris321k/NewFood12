from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManger
import random

class Person(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=30)
    bio = models.CharField(max_length=40, blank=True, null=True)
    phonenumer=models.IntegerField(default=0000)
    address=models.TextField(max_length=200)
    isOwner = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManger()


    def __str__(self):
        return self.email

class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    category_img=models.ImageField(upload_to='images/')

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


class Review(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='person_reviews')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews')
    review_text = models.TextField(max_length=500)
    




class otp(models.Model):
    person=models.ForeignKey(Person,on_delete=models.CASCADE,related_name='otp')
    #email=models.EmailField(max_length=254)
    otp_number=models.CharField(max_length=4)
    otp_created=models.DateTimeField(auto_now_add=True)





class Restaurent(models.Model) :
    Rname = models.CharField(max_length=50)
    Rimg = models.ImageField(upload_to='images/')
    Rdesc = models.CharField(max_length=100)
    Fooditems = models.ManyToManyField(FoodItem)
    address = models.CharField(max_length=150)
    Radmin = models.OneToOneField(Person, on_delete = models.CASCADE)
    RcontactNumber = models.IntegerField() 


class order(models.Model) :
    Res = models.ForeignKey(Restaurent, on_delete=models.CASCADE)
    User = models.ForeignKey(Person, on_delete=models.CASCADE)
    fooditem = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, default='pending')
    Ispayment = models.BooleanField(default=False)
    OrderId = models.CharField(max_length=100)




class AditionalFoodItems(models.Model) :
    order = models.OneToOneField(order, on_delete=models.CASCADE)
    Additems = models.ManyToManyField(FoodItem)





    











    













    
    