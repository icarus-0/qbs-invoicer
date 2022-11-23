from django.urls import path
from . import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('clients',views.clients,name='clients'),
    path('items',views.items,name='items'),
    path('invoices',views.invoices,name='invoices'),
    path('client_update',views.client_update,name='client_update'),
    path('item_update',views.item_update,name='item_update'),
    path('create_invoice',views.create_invoice,name="create_invoice"),
    path('generate_invoice',views.generate_invoice,name="generate_invoice"),
    path('sync_invoices',views.sync_invoices,name="sync_invoices")
   
]