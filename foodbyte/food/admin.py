from django.contrib import admin

from .models import Person,FoodItem,Review,Category,otp,Cart,CartItem,Restaurent, AditionalFoodItems, order
admin.site.register(Person)
admin.site.register(FoodItem)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(otp)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Restaurent)
admin.site.register(AditionalFoodItems)
admin.site.register(order)




# Register your models here.
