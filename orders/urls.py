
from django.urls import path
from . import views


urlpatterns = [
    path('place_order/',views.place_order,name="place_order"),
    path('payment/', views.payment, name='payment'),
    path('pay/', views.create_checkout_session, name='pay'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('webhook/', views.stripe_webhook, name='webhook'),
]
