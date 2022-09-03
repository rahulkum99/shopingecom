from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_email
from products.models import Product , SizeVarient,ColorVarient
# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profile')

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False,cart__user=self.user).count()

class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True)
    color_varient = models.ForeignKey(ColorVarient, on_delete=models.SET_NULL,null=True,blank=True)
    size_varient = models.ForeignKey(SizeVarient, on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.product.product_name


@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    try:
        email_token = str(uuid.uuid4())
        print(email_token)
        Profile.objects.create(user=instance,email_token=email_token)
        email= instance.email
        send_account_activation_email=(email,email_token)
    except Exception as e:
        print(e)