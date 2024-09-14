from django.contrib import admin

from .models import Person,FoodItem,Review,Order,Category,otp,Cart,CartItem,OrderItem
admin.site.register(Person)
admin.site.register(FoodItem)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(otp)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)



# Register your models here.
