from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
import datetime
import json
from .filters import *
from .main import *

def home(request):
    """
        params : request [ WSGI request object ]
        url    : /dashboard/home
        returns: render object of home.html with data or redirect object to /login/signin
    """
    if request.user.is_authenticated:
        invoices = Invoice.objects.all().order_by('-id')
        total_invoices = len(invoices)
        total_clients  = len(Client.objects.all())
        total_items    = len(Item.objects.all())

        data = {
            'total_invoices':total_invoices,
            'total_clients' :total_clients,
            'total_items'   : total_items,
            'invoices'      : invoices
        }
        return render(request,'home.html',data)
    return redirect('/login/signin')

def clients(request):
    if request.method == 'POST':
        client_name = request.POST['client_name']
        client_contact = request.POST['client_contact']
        client_address = request.POST['client_address']
        client_email = request.POST['client_email']
        client_ins = Client(
                    name=client_name,
                    contact=client_contact,
                    address=client_address,
                    email=client_email,
                    )
        response = json.loads(create_customer_on_qbo(client_ins).text)
        client_ins.qbo_id = response['Customer']['Id']
        client_ins.save()
        

        return redirect('/dashboard/clients?page=1')

    clients_data = Client.objects.all().order_by('-id')
    cfilter = client_filter(request.GET,queryset=clients_data)
    clients_data = cfilter.qs

    paginator = Paginator(clients_data,2)
    page_number = request.GET.get('page')
    clients_data_final = paginator.get_page(page_number)
    data = {
        'clients':clients_data_final,
        'client_filter':cfilter
    }

    return render(request,'clients.html',data)

@csrf_exempt
def client_update(request):
    if request.method == 'POST':
        data = json.load(request)
        id = int(data['id'])
        field = data['field']
        value = data['value']
        
        client_ins = Client.objects.get(pk=id)
        if field == 'name':
            client_ins.name = value
        elif field == 'contact':
            client_ins.contact = value
        elif field == 'email':
            client_ins.email = value
        elif field == 'address':
            client_ins.address = value

        client_ins.save()
        return JsonResponse({'status': 'Todo added!'})
    else:
        return HttpResponseBadRequest('Invalid request')

def items(request):
    if request.method == 'POST':
        item_name = request.POST['item_name']
        item_desc = request.POST['item_desc']
        item_price = request.POST['item_price']

        item_ins = Item(
            name = item_name,
            desc = item_desc,
            price = item_price
        )
        response = json.loads(create_item_on_qbo(item_ins).text)
        #print(response)
        item_ins.qbo_id = response['Item']['Id']
        item_ins.save()
        return redirect('/dashboard/items?page=1')
    
    items_data = Item.objects.all().order_by('-id')
    ifilter = item_filter(request.GET,queryset=items_data)
    items_data = ifilter.qs

    paginator = Paginator(items_data,2)
    page_number = request.GET.get('page')
    items_data_final = paginator.get_page(page_number)

    data = {
        'items':items_data_final,
        'item_filter':ifilter
    }
    return render(request,'items.html',data)


@csrf_exempt
def item_update(request):
    if request.method == 'POST':
        data = json.load(request)
        id = int(data['id'])
        field = data['field']
        value = data['value']
        
        item_ins = Item.objects.get(pk=id)
        if field == 'name':
            item_ins.name = value
        elif field == 'desc':
            item_ins.desc = value
        elif field == 'price':
            item_ins.price = float(value)
        
        item_ins.save()
        return JsonResponse({'status': 'Todo added!'})
    else:
        return HttpResponseBadRequest('Invalid request')



def invoices(request):

    clients_data=Client.objects.all().order_by('-id')
    items_data = Item.objects.all().order_by('-id')
    invoices_data = Invoice.objects.all().order_by('-id')

    infilter = invoice_filter(request.GET,queryset=invoices_data)
    invoices_data = infilter.qs

    paginator = Paginator(invoices_data,2)
    page_number = request.GET.get('page')
    invoices_data_final = paginator.get_page(page_number)


    data = {
        'clients':clients_data,
        'items': items_data,
        'invoices':invoices_data_final,
        'invoice_filter':infilter
    }
    return render(request,'invoices.html',data)


@csrf_exempt
def create_invoice(request):
    data = json.load(request)
    
    client_id = int(data['client_id'])
    client_ins = Client.objects.get(pk=client_id)
    #print(data)
    invoice_ins = Invoice(
        client = client_ins,
        total = float(data['total_final']),
        sync_status = "Not Sync With QBO"

    )
    invoice_ins.save()
    for i in data['invoice_data']:
        qbo_id = Item.objects.get(pk=int(data['invoice_data'][i][0])).qbo_id
        invoice_item_ins = InvoiceItem(
            invoice = invoice_ins,
            name = data['invoice_data'][i][1],
            desc = data['invoice_data'][i][2],
            price = data['invoice_data'][i][3],
            qty = data['invoice_data'][i][4],
            total =  data['invoice_data'][i][5],
            qbo_id = qbo_id
        )
        invoice_item_ins.save()
    
    return JsonResponse({'status':200})



def generate_invoice(request):
    id = int(request.GET.get('id'))
    invoice_ins = Invoice.objects.get(pk=id)
    invoice_items = InvoiceItem.objects.all().filter(invoice=invoice_ins)
    data = {
        'invoice':invoice_ins,
        'items':invoice_items
    }
    return render(request,'invoice_pdf.html',data)

@csrf_exempt
def sync_invoices(request):
    invoices_ins = Invoice.objects.all().filter(sync_status='Not Sync With QBO')

    for invoice_ins in invoices_ins:
        invoice_items = InvoiceItem.objects.all().filter(invoice=invoice_ins)
        response = json.loads(create_invoice_on_qbo(invoice_ins,invoice_items).text)
        invoice_ins.qbo_id = response['Invoice']['Id']
        invoice_ins.sync_date = datetime.date.today()
        invoice_ins.sync_status = 'Synced'
        invoice_ins.save()
    return JsonResponse({'status':200})