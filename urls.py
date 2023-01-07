from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage),
    path('login', views.login),
    path('signup', views.signup),
    path('Showpizza/<id>',views.Showpizza),
    path('Viewdetails/<id>',views.Viewdetails),
    path('signout', views.signout),
    path('addtocart', views.addtocart),
    path('ShowAllCartItems',views.ShowAllCartItems),
    path("removeItem",views.removeItem),
    path('MakePayment',views.MakePayment),
    path('Orderdetails',views.Orderdetails),
    path('review',views. review),
    #path(' reviewList',views.reviewList),
    #path('deleteReview',views.deleteReview),
    path('reviewsave',views.reviewsave),
   

]