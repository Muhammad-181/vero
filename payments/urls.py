from django.urls import path
from . import views


app_name = "payments"


urlpatterns = [
    # path('', views.index, name="index"),
    path('', views.initialize_payment, name='initialize_payment'),
    path('get_levels/', views.get_levels, name='get_levels'),
    path('get_amount/', views.get_amount, name='get_amount'),
    # path('make_payment/', views.make_payment, name='make_payment'), 
    # path('verify-reciept/<uuid:reference>/', views.verify_reciept, name='verify-reciept'),
    path('verify/<uuid:reference>/', views.verify_payment, name='verify_payment'),
    path('reciept2pdf/<uuid:reference>/', views.print_reciept, name='reciept2pdf'),
    # path('reciept2pdf/<uuid:reference>/', views.reciept2pdf, name='reciept2pdf'),
]