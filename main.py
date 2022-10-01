import requests
import json
import os

"""
This script corrects the personal data (name, address, city and company) that were 
entered in all upper case examp. "JOHN JOHNSON" or all lower case "john johnson" or 
a mix of both "JoHn joHnson". 

folder status - is an id number of folder with concerning orders

API key - is available after loging onto Baselinker and checking settings.
"""

API_key = os.getenv('BL_TOKEN')
folder_status = 56977
BLToken = {'X-BLToken': API_key}


def get_data():
    get_orders = {'method': 'getOrders',
                            'parameters': json.dumps({'status_id': folder_status,
                                                      'get_unconfirmed_orders': 'true'})}

    response = requests.post('https://api.baselinker.com/connector.php', headers=BLToken, data=get_orders)
    print(json.dumps(response.json(), indent=4))
    return response


def set_changes():
    set_order_fields = {'method': 'setOrderFields',
                        'parameters': json.dumps({'order_id': order_id,
                                                  'invoice_fullname': invoice_data[0],
                                                  'invoice_address': invoice_data[1],
                                                  'invoice_city': invoice_data[2],
                                                  'invoice_company': invoice_data[3],
                                                  'delivery_fullname': delivery_data[0],
                                                  'delivery_address': delivery_data[1],
                                                  'delivery_city': delivery_data[2],
                                                  'delivery_company': delivery_data[3]
                                                  })}
    requests.post('https://api.baselinker.com/connector.php', headers=BLToken, data=set_order_fields)


def fix(name: str):
    name = name.split(' ')
    name = [word.title() for word in name]
    name = ' '.join(name)
    return name


response_data = get_data()  # connecting via API
orders_ids = []
orders_count = len(response_data.json()['orders'])

index1 = 0
while index1 < orders_count:
    orders_ids.append(response_data.json()["orders"][index1]["order_id"])
    index1 += 1
print(orders_ids)

for index2, order in enumerate(orders_ids):
    # data that we want to correct
    full_name = str(response_data.json()['orders'][index2]["invoice_fullname"])
    address = str(response_data.json()['orders'][index2]["invoice_address"])
    city = str(response_data.json()['orders'][index2]["invoice_city"])
    company = str(response_data.json()['orders'][index2]["invoice_company"])
    invoice_data = [full_name, address, city, company]

    # shipping data we want to also correct
    delivery_full_name = str(response_data.json()['orders'][index2]['delivery_fullname'])
    delivery_address = str(response_data.json()['orders'][index2]["delivery_address"])
    delivery_city = str(response_data.json()['orders'][index2]["delivery_city"])
    delivery_company = str(response_data.json()['orders'][index2]["delivery_company"])
    delivery_data = [delivery_full_name, delivery_address, delivery_city, delivery_company]

    for index3, item in enumerate(invoice_data):
        invoice_data[index3] = fix(item)

    for index3, item in enumerate(delivery_data):
        delivery_data[index3] = fix(item)

    order_id = orders_ids[index2]

    set_changes()
    invoice_data.clear()
    delivery_data.clear()

print(response_data.json())
