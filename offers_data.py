import json
import pandas as pd
import datetime

def output_data(result_to_sheet):
    e = datetime.datetime.now()
    date = e.strftime("%d/%m/%Y")
    offers_data_compiled = pd.read_json(r'%s' %result_to_sheet)
    # print(offers_data_compiled)
    offers_data = []
    offers_asins = []
    offer_id = []
    price = []
    seller_name = []
    seller_id = []
    ASIN = []
    date_list = []
    buybox = []
    condition = []
    isfba = []
    delivery = []
    request = []
    for i in range(0,len(offers_data_compiled)):
        if 'offers' in offers_data_compiled['result'][i]:
            offers_data.extend(offers_data_compiled['result'][i]['offers'])
        request.append(offers_data_compiled['request'][i])
    for j in range(0,len(offers_data)):
        date_list.append(date)
        if 'offer_asin'in offers_data[j]:
            ASIN.append(offers_data[j]['offer_asin'])
        else:
            print('NO ASIN IN THIS OFFER')
            if j==0:
                ASIN.append(request[0])
            else:
                ASIN.append(ASIN[j-1])
        if 'delivery' in offers_data[j]:
            if 'comments' in offers_data[j]['delivery']:
                delivery.append(offers_data[j]['delivery']['comments'])
            else:
                delivery.append('No delivery Time Mentioned')
        else:
            delivery.append('No delivery Time Mentioned')
        if 'offer_id'in offers_data[j]:
            offer_id.append(offers_data[j]['offer_id'])
        else:
            print('NO OFFER ID')
            offer_id.append('NO OFFER ID')
        if 'price' in offers_data[j]:
            price.append(offers_data[j]['price']['value'])
        else:
            price.append('0')
        if 'seller' in (offers_data[j]):
            seller_name.append(offers_data[j]['seller']['name'])
            if 'id' in offers_data[j]['seller']:
                seller_id.append(offers_data[j]['seller']['id'])
            else:
                seller_id.append('No Seller ID')
        else:
            seller_name.append('No Seller Name')
            seller_id.append('No Seller ID')
        if 'buybox_winner' in offers_data[j]:
            buybox.append(offers_data[j]['buybox_winner'])
        else:
            buybox.append("FALSE")
        if 'condition' in offers_data[j]:
            if 'title' in offers_data[j]['condition']:
                condition.append(offers_data[j]['condition']['title'])
            else:
                condition.append('No Title')
        else:
            condition.append('No Title')
        if 'delivery' in offers_data[j]:
            if 'fulfilled_by_amazon' in offers_data[j]['delivery']:
                isfba.append(offers_data[j]['delivery']['fulfilled_by_amazon'])
            else:
                isfba.append('FALSE')
        else:
            isfba.append('FALSE')
    return date_list,ASIN,price,seller_name,seller_id,offer_id, isfba, condition, buybox, delivery
