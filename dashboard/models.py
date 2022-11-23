from django.db import models


class Client(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField(null=True)
    email = models.EmailField(null=True)
    qbo_id = models.CharField(max_length=100,null=True)

    def __str__(self):
         return str(self.id)+'_'+self.name

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.FloatField()
    qbo_id = models.CharField(max_length=100,null=True)

    def __str__(self):
         return str(self.id)+'_'+self.name


class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client,null=True,on_delete=models.SET_NULL)
    total = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sync_date = models.DateField(null=True)
    sync_status = models.CharField(max_length=20)
    qbo_id = models.CharField(max_length=100,null=True)

    def __str__(self):
         return str(self.id)

class InvoiceItem(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    desc = models.TextField()
    price = models.FloatField()
    qty = models.IntegerField()
    total = models.FloatField()
    qbo_id = models.CharField(max_length=100,null=True)

    def __str__(self):
         return str(self.id)+'_'+self.name


