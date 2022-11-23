from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Item)
admin.site.register(Invoice)
admin.site.register(InvoiceItem)