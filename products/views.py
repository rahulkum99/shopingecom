from django.shortcuts import render ,redirect
from products.models import Product 
from accounts.models import Cart,CartItem
from django.http import HttpResponseRedirect
# Create your views here.


def get_product(request,slug):
    try:
        product  = Product.objects.get(slug=slug)
        context = {'product':product}
        if request.GET.get('size'):
            size = request.GET.get('size')
            price = product.get_product_price_by_size(size)
            context['selected_size'] = size
            context['updated_price'] = price
        return render(request,'product/products.html',context =context)
    except Exception as e:
        print(e)



def add_to_cart(request,uid):
    varient = request.GET.get('varient')
    product = Product.objects.get(uid=uid)
    user = request.user
    cart ,_ = Cart.objects.get_or_create(user=user,is_paid=False)
    cart_item = CartItem.objects.create(cart=cart,product=product)
    if varient:
        varient = request.GET.get('varient')
        size_varient = SizeVariant.objects.get(size_name=varient)
        cart_item.size_varient = size_varient
        cart_item.save()
#    return HttpResponseRedirect(request.path_info)
    return redirect('/')
