from .qbClient import AuthClient
from .constants import *
import requests
from future.moves.urllib.parse import urlencode

auth_client = AuthClient(**client_secrets)


def refresh_token():
    '''
        refresh_token argument : None
        refresh_tiken returns  : JsonResponse [ dict ]
        refresh_token is using refresh token to genrate new access token
    '''
    response = auth_client.refresh(refresh_token=refreshToken)
    return response

def get_companyinfo_from_qbo(access_token):
    '''
        get_companyinfo_from_qbo arguments : acsess_token [ string ]
        get_companyinfo_from_qbo returns : JsonResponse [ dict ]
        get_comapnyinfo_from_qbo takes access_token as argument and returns a jsonresponse with company info
    '''

    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/companyinfo/{1}'.format(base_url, qBData["realm_id"])
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response



def create_customer_on_qbo(customer_ins):
    '''
        create_customer_on_qbo arguments : customer_ins [ django model object ]
        create_customer_on_qbo returns   : JsonResponse [ dict ]
        creat_customer_on_qbo takes access_token as argument and returns a success/failed response as jsonresponse
    '''
    access_token = refresh_token()['access_token']
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/customer?minorversion=65'.format(base_url, qBData["realm_id"])
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    data = {
            "FullyQualifiedName": customer_ins.name, 
            "PrimaryEmailAddr": {
                "Address": customer_ins.email
            }, 
            "DisplayName": customer_ins.name,
            "Notes": "Customer added from the app", 
            "FamilyName": customer_ins.name, 
            "PrimaryPhone": {
                "FreeFormNumber": customer_ins.contact,
            }, 
            "CompanyName": customer_ins.name, 
            "GivenName": customer_ins.name,
            }
    response = requests.post(url, headers=headers,json=data)
    return response

def query_customer_on_qbo(access_token,sql_query): 
    '''
        query_customer_on_qbo arguments : access_token [ string ] , sql_query [ string ]
        query_customer_on_qbo returns   : jsonresponse [ dict ]

        query_customer_on_qbo takes access_token and a sql query ( ex. select * from Customer Where Id='15') and
        returns queried data as json_response
    '''

    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/query?query={2}&minorversion=65'.format(base_url, qBData["realm_id"],sql_query)
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    
    response = requests.get(url, headers=headers)
    return response

def update_customer_on_qbo(access_token, update_data):
    '''
        update_customer_on_qbo arguments : access_token [ string ] , update_data [ dict ]
        update_customer_on_qbo returns   : JsonResponse [ dict ]
        update_customer_on_qbo takes access_token and update_data 
        ( ex. 
            {
                "MiddleName": "Mark", 
                "Id": "15", 
                "sparse": True
            } Id and sparse is required  ) and returns success/failed response
    '''
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/customer&minorversion=65'.format(base_url, qBData["realm_id"])
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    

    response = requests.post(url, headers=headers,json=update_data)
    return response


def create_item_on_qbo(item_ins):
    '''
        create_item_on_qbo arguments : item_ins [ django model object ]
        create_item_on_qbo returns   : JsonResponse [ dict ]
        creat_item_on_qbo takes access_token as argument and returns a success/failed response as jsonresponse
    '''
    access_token = refresh_token()['access_token']
    base_url = 'https://sandbox-quickbooks.api.intuit.com'
    url = '{0}/v3/company/{1}/item?minorversion=65'.format(base_url, qBData["realm_id"])
    auth_header = 'Bearer {0}'.format(access_token)
    headers = {
        'Authorization': auth_header,
        'Accept': 'application/json'
    }
    data = {
            "TrackQtyOnHand": True, 
            "Name": item_ins.name, 
            "QtyOnHand": 1000, 
            "IncomeAccountRef": {
                "name": "Sales of Product Income", 
                "value": "79"
            }, 
            "AssetAccountRef": {
                "name": "Inventory Asset", 
                "value": "81"
            }, 
            "Type": "Inventory", 
            "ExpenseAccountRef": {
                "name": "Cost of Goods Sold", 
                "value": "80"
            }
        }
    response = requests.post(url, headers=headers,json=data)
    return response