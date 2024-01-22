import pandas as pd
import datetime

def output_data(resulta_to_sheet):
    e = datetime.datetime.now()
    date = e.strftime("%d/%m/%Y")
    # stock_data_compiled = resulta_to_sheet
    stock_data_compiled = pd.read_json(r'%s' %resulta_to_sheet)
    stock_estimation =[]
    request = []
    for i in range(0,len(stock_data_compiled)):
        if 'stock_estimation' in stock_data_compiled['result'][i]:
            stock_estimation.append(stock_data_compiled['result'][i]['stock_estimation'])
        request.append(stock_data_compiled['request'][i])
            
    stock_level = []
    min_quantity = []
    dates = []
    availability_message = []
    is_prime = []
    in_stock = []
    has_stock_estimation = []
    message = []
    stock_asin = []
    stock_offerid = []
    stock_price= []
    print(len(stock_estimation))
    for i in range(0, len(stock_estimation)):
        dates.append(date)
        if 'stock_level' in stock_estimation[i]:
            stock_level.append(stock_estimation[i]['stock_level'])
        else:
            stock_level.append('No Stock')
        if 'min_quantity' in stock_estimation[i]:
            min_quantity.append(stock_estimation[i]['min_quantity'])
        else:
            min_quantity.append('0')
        if 'availability_message' in stock_estimation[i]:
            availability_message.append(stock_estimation[i]['availability_message'])
        else:
            availability_message.append('No availability message')
        if 'message' in stock_estimation[i]:
            message.append(stock_estimation[i]['message'])
        else:
            message.append('No message')
        if 'is_prime' in stock_estimation[i]:
            is_prime.append(stock_estimation[i]['is_prime'])
        else:
            is_prime.append('FALSE')
        if 'in_stock' in stock_estimation[i]:
            in_stock.append(stock_estimation[i]['in_stock'])
        else:
            in_stock.append('FALSE')
        if 'has_stock_estimation' in stock_estimation[i]:
            has_stock_estimation.append(stock_estimation[i]['has_stock_estimation'])
        else:
            has_stock_estimation.append('FALSE')
        if 'asin' in stock_estimation[i]:
            stock_asin.append(stock_estimation[i]['asin'])
        else:
            stock_asin.append(request[i]['asin'])
        # stock_asin.append(request[i]['asin'])
        if 'offer_id' in stock_estimation[i]:
            stock_offerid.append(stock_estimation[i]['offer_id'])
        else:
            stock_offerid.append(request[i]['offer_id'])

    return dates, stock_asin, stock_offerid,stock_price,stock_level, min_quantity, availability_message, message, is_prime, in_stock, has_stock_estimation
