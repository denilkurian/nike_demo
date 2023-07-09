from django.shortcuts import render,redirect,get_object_or_404
from rest_framework import generics, status, permissions
from django.views.generic import TemplateView,ListView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from .models import Shoes
from .serializers import ShoeSerializer
from django.db.models import Q

def welcomepage(request):
    return render(request, 'landing.html')


######## listing shoes
class ListShoes(generics.ListCreateAPIView, TemplateView):
    queryset = Shoes.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.AllowAny]
    serializer_class = ShoeSerializer
    template_name = 'Mens.html'

    def list(self, request, *args, **kwargs):
        shoes = self.get_queryset()
        serializer = self.get_serializer(shoes, many=True)
        context = {'shoes': serializer.data}
        return render(request, self.template_name, context)


########## details
class DetailShoes(generics.RetrieveUpdateAPIView):
    queryset = Shoes.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [permissions.AllowAny]
    serializer_class = ShoeSerializer
    lookup_field = 'id'
    template_name = 'detail.html'


    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        form = ShoeSerializer(instance=instance)
        context = {'shoes': serializer.data}
        return render(request, self.template_name, context)



####### filter
class Filter(ListView):
    model = Shoes
    template_name = 'filter.html'

    def get_queryset(self):
        query = self.request.GET.get('f')
        return Shoes.objects.filter(Q(color=query)| Q(season=query) | Q(categaory=query) | Q(name=query))



from django.http import JsonResponse
from django.views.decorators.http import require_GET
######### search suggessions
@require_GET
def autocomplete_shoes(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        names = Shoes.objects.filter(name__istartswith=term).values_list('name', flat=True)
        return JsonResponse(list(names), safe=False)
    return JsonResponse([])




from .models import Cart,Shoes
from .serializers import CartSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

######## cart

# def add_to_cart(request, product_id):
#     Product = get_object_or_404(Shoes, pk=product_id)
#     cart_item, created = Cart.objects.get_or_create(
#         user=request.user,
#         product=Product,
#         price=Product.price,
#         image_url=Product.main_image_url,
#     )
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     return redirect('cart')
#
#
#
# def remove_from_cart(request, cart_id):
#     cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     else:
#         cart_item.delete()
#     return redirect('cart')
#
#
# def remove_from_cart_all(request, cart_id):
#     cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
#     cart_item.delete()
#     return redirect('cart')
#
#
# def Cart_view(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     total = sum(item.price * item.quantity for item in cart_items)
#     return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class AddToCartAPIView(LoginRequiredMixin,APIView):
    login_url = 'login'

    def post(self, request, product_id):
        product = get_object_or_404(Shoes, pk=product_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            price=product.price,
            image_url=product.main_image_url,
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartSerializer(cart_item)
        return redirect('cart')



@api_view(['POST'])
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@api_view(['POST'])
def remove_from_cart_all(request, cart_id):
    cart_item = get_object_or_404(Cart, pk=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')



@login_required(login_url='login')
@api_view(['GET'])
def Cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    serializer = CartSerializer(cart_items, many=True)
    total = sum(item.price * item.quantity for item in cart_items)
    response_data = {
        'cart_items': serializer.data,
        'total': total
    }
    # return Response(response_data)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})



