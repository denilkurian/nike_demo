from django.urls import path
from .views import welcomepage,ListShoes,Filter,DetailShoes,autocomplete_shoes,AddToCartAPIView,remove_from_cart,remove_from_cart_all,Cart_view


urlpatterns = [
    path('',welcomepage,name='welcome'),
    path('listshoes',ListShoes.as_view(),name='listshoes'),
path('detailshoes/<int:id>/',DetailShoes.as_view(),name='detailshoes'),
path('filter',Filter.as_view(),name='filter'),
path('autocomplete-shoes/', autocomplete_shoes, name='autocomplete_shoes'),


path('add_to_cart/<int:product_id>/', AddToCartAPIView.as_view(), name='add_to_cart'),
path('cart',Cart_view,name='cart'),
path('remove-from-cart/<int:cart_id>/', remove_from_cart, name='remove_from_cart'),
path('remove_from_cart_all/<int:cart_id>/',remove_from_cart_all, name='remove_from_cart_all'),

]


