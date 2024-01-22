import create_collection
import offers_data
import request_collection
import start_till_delect_collection
import pandas as pd
import math
import create_collection_stock
import request_collection_stock
from GoogleSheet_stock import GoogleSheet_SE
import stock_data
import time
import csv
import datetime
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pandas import DataFrame


class MainFile(QtCore.QThread):
    update = QtCore.pyqtSignal(str)
    progressbar = QtCore.pyqtSignal(int)
    def __init__(self,excel_google,Google_id, worksheet_to_store, excel_sheet_address):
        super().__init__()
        self.offers_data = []
        self.GOOGLE_SHEET_LINK = Google_id
        self.WORKSHEET = worksheet_to_store
        self.excel_or_googlesheet = excel_google
        self.ASIN_SHEET = "ASIN"
        self.excel_sheet = excel_sheet_address
        self.stock_sheet_object = GoogleSheet_SE("./resources/client_secret.json",
                                                 self.GOOGLE_SHEET_LINK)
        if self.excel_or_googlesheet == "EXCEL" or self.excel_or_googlesheet == "excel":
            self.data = pd.read_excel(r'%s' % excel_sheet_address, sheet_name='ASIN')
        else:
            self.data = pd.read_csv(f'https://docs.google.com/spreadsheets/d/%s/export?format=csv' % self.GOOGLE_SHEET_LINK)
        print("********************************")
        print('Length of input data is: ',len(self.data))
        print("********************************")
    def run(self):
        self.progressbar.emit(10)
        self.collection_id = create_collection.collection_creation()
        self.update.emit("Offers Collection Created.")
        self.update.emit("Offer's Collection ID is: %s" %self.collection_id)
        try:
            print(len(self.data))
            self.length_asin = request_collection.requesting_collection(self.collection_id,self.data)
        except Exception as l:
            self.update.emit("%s" %l)
            time.sleep(120)
            self.length_asin = request_collection.requesting_collection(self.collection_id,self.data)
        self.update.emit("Offers Requested and Started.")
        self.progressbar.emit(20)
        try:
            start_till_delect_collection.collection_started(self.collection_id,self.length_asin)
        except Exception as error:
            self.update.emit(error)
            time.sleep(120)
            start_till_delect_collection.collection_started(self.collection_id,self.length_asin)
        # n = self.length_asin
        # count=0
        # while(n>0):
        #     count=count+1
        #     n=n//10
        # print("The number of digits in the number are:",count)
        # if count == 1:
        #     self.update.emit("You have to wait for 4 minutes")
        #     time.sleep(200)
        # elif count == 2:
        #     self.update.emit("You have to wait for 5 minutes")
        #     time.sleep(300)
        # elif count == 3:
        #     self.update.emit("You have to wait for 7 minutes")
        #     time.sleep(400)
        # elif count == 4:
        #     self.update.emit("You have to wait for 9 minutes")
        #     time.sleep(500)
        # else:
        #     self.update.emit("You have to wait for 10 minutes")
        #     time.sleep(600)
        try:
            start_till_delect_collection.stopping_collection(self.collection_id)
        except Exception as k:
            self.update.emit("%s" %k)
            time.sleep(120)
            start_till_delect_collection.stopping_collection(self.collection_id)
        self.update.emit("Offers Collection Stopped.")
        try:
            self.length_results, self.result_links = start_till_delect_collection.getting_results(self.collection_id)
        except Exception as j:
            self.update.emit("%s" %j)
            time.sleep(120)
            self.length_results, self.result_links = start_till_delect_collection.getting_results(self.collection_id)
        # start_till_delect_collection.collection_deletion(self.collection_id)
        self.progressbar.emit(30)
        self.date_list =[]
        self.ASIN = []
        self.price = []
        self.seller_name = []
        self.seller_id = []
        self.offer_id =[]
        self.isfba = []
        self.condition = []
        self.buyboxwinner = []
        delivery_time = []
        self.update.emit("Collecting Offers Data.")
        for i in range(0,self.length_results):
            self.result_to_sheet = self.result_links[i]
            print(self.result_to_sheet)
            print("*******************")
            date, asins, valueprice , sellername, \
            sellerid, offerid, FBA, Condition, \
            buy_box_winner , delivery = offers_data.output_data(self.result_to_sheet)
            self.date_list.extend(date)
            self.ASIN.extend(asins)
            self.price.extend(valueprice)
            self.seller_name.extend(sellername)
            self.seller_id.extend(sellerid)
            self.offer_id.extend(offerid)
            self.isfba.extend(FBA)
            self.condition.extend(Condition)
            self.buyboxwinner.extend(buy_box_winner)
            delivery_time.extend(delivery)
        self.update.emit("Offers Collection Completed.")
        self.progressbar.emit(40)
        print("Offers without filter ", len(self.offer_id))
        '''OFFERS DATA ENDED AND RETURN'''
        self.tab_name = self.stock_sheet_object.create_tabs(self.stock_sheet_object, self.WORKSHEET)
        self.rows_present = self.stock_sheet_object.read_data(self.stock_sheet_object, self.tab_name)
        self.ASIN_DATA = []
        self.OFFERS_DATA = []
        indices_to_remove = [index for (index, item) in enumerate(self.offer_id) if item == "NO OFFER ID"]
        for i in range(0,len(indices_to_remove)):
            if i == 0:
                pass
            else:
                indices_to_remove = [x - 1 for x in indices_to_remove]
            self.offer_id.pop(indices_to_remove[i])
            self.ASIN.pop(indices_to_remove[i])
            self.date_list.pop(indices_to_remove[i])
            self.price.pop(indices_to_remove[i])
            self.seller_name.pop(indices_to_remove[i])
            self.seller_id.pop(indices_to_remove[i])
            self.isfba.pop(indices_to_remove[i])
            self.condition.pop(indices_to_remove[i])
            self.buyboxwinner.pop(indices_to_remove[i])
            delivery_time.pop(indices_to_remove[i])
        self.ASIN_DATA = self.ASIN
        # print(self.ASIN_DATA)
        self.OFFERS_DATA = self.offer_id
        # print(self.OFFERS_DATA)
        # print(self.price, self.seller_name, self.isfba, self.condition, self.buyboxwinner)
        df = DataFrame({'DATE': self.date_list, 'ASIN': self.ASIN_DATA , 'OFFER ID': self.OFFERS_DATA,
                            'PRICE': self.price, 'SELLER NAME': self.seller_name,
                            'SELLER ID': self.seller_id,'IS FBA': self.isfba, 
                            'CONDITION': self.condition,'BUY BOX WINNER': self.buyboxwinner, 'DELIVERY_DATE' : delivery_time})
        e = datetime.datetime.now()
        datetoday = e.strftime("%d/%m/%Y")
        datetoday = datetoday.replace("/", "_")
        # print(df)
        df.to_excel('%s_offers_data.xlsx'%datetoday,sheet_name='offers', index=False)
            
        self.columns = {"DATE": [], "ASIN": [], "OFFER_ID": [], "SELLER_NAME": [], "PRICE": [],
                        "IS_FBA": [], "CONDITION": [], "BUYBOX_WINNER": [], "DELIVERY_DATE": [] , "STOCK_LEVEL": [],
                        "MIN_QUANTITY": [], "AVAILABILITY_MESSAGE": [], "MESSAGE": [],
                        "IS_PRIME": [], "IN_STOCK": [], "HAS_STOCK_ESTIMATION": []}
        self.progressbar.emit(50)
        print("Offers received after filter", len(self.OFFERS_DATA))
        if len(self.OFFERS_DATA) < 15000:
            self.collection_id_stock = create_collection_stock.collection_creation()
            self.update.emit("Stock Estimation Collection Created.")
            self.update.emit("Stock's Collection ID is: %s" %self.collection_id_stock)
            self.progressbar.emit(60)
            try: 
                self.length_offers_stock = request_collection_stock.requesting_collection(self.collection_id_stock,
                                                                                     self.ASIN_DATA,self.OFFERS_DATA)
            except Exception as i:
                self.update.emit("%s" %i)
                time.sleep(120)
                self.length_offers_stock = request_collection_stock.requesting_collection(self.collection_id_stock,
                                                                                     self.ASIN_DATA,self.OFFERS_DATA)
            self.update.emit("Stock Requested and Started.")
            try:
                start_till_delect_collection.collection_started(self.collection_id_stock,self.length_offers_stock)
            except Exception as h:
                self.update.emit("%s" %h)
                time.sleep(120)
                start_till_delect_collection.collection_started(self.collection_id_stock,self.length_offers_stock)
            
            self.progressbar.emit(70)
            self.update.emit("Finalizing Collection.")
            try:
                start_till_delect_collection.stopping_collection(self.collection_id_stock)
            except Exception as g:
                self.update.emit("%s" %g)
                time.sleep(120)
                start_till_delect_collection.stopping_collection(self.collection_id_stock)
            self.update.emit("Stock Estimation Collection Stopped.")
            try:
                self.length_results, self.result_links = start_till_delect_collection.getting_results(self.collection_id_stock)
            except Exception as f:
                self.update.emit("%s" %f)
                time.sleep(120)
                self.length_results, self.result_links = start_till_delect_collection.getting_results(self.collection_id_stock)
            # start_till_delect_collection.collection_deletion(self.collection_id_stock)
            self.update.emit("Stock Estimation Collection Completed.")
            self.progressbar.emit(80)
            self.dates =[]
            self.stock_asin =[]
            self.stock_offerid = []
            self.stock_level =[]
            self.min_quantity =[]
            self.availability_message =[]
            self.message =[]
            self.is_prime = []
            self.in_stock = []
            self.has_stock_estimation = []
            self.stockprice = []
            self.update.emit("Collecting Stock Estimation Data.")
            for i in range(0,self.length_results):
                self.results_to_sheet = self.result_links[i]
                print(self.results_to_sheet)
                print("*******************************")
                date, stockasin, stockofferid, stock_price, stocklevel, minquantity, \
                availabilitymessage, Message, isprime, instock, hasstockestimation = stock_data.output_data(self.results_to_sheet)
                self.dates.extend(date)
                self.stock_asin.extend(stockasin)
                self.stock_offerid.extend(stockofferid)
                # self.stockprice.extend(stock_price)
                self.stock_level.extend(stocklevel)
                self.min_quantity.extend(minquantity)
                self.availability_message.extend(availabilitymessage)
                self.message.extend(Message)
                self.is_prime.extend(isprime)
                self.in_stock.extend(instock)
                self.has_stock_estimation.extend(hasstockestimation)
            seller = []
            isfba = []
            conditionofstock = []
            buybox = []
            pprice = []
            stockdelivery = []
            for i in range(0,len(self.stock_offerid)):
                index = self.OFFERS_DATA.index(self.stock_offerid[i])
                seller.append(self.seller_name[index])
                isfba.append(self.isfba[index])
                conditionofstock.append(self.condition[index])
                buybox.append(self.buyboxwinner[index])
                pprice.append(self.price[index])
                stockdelivery.append(delivery_time[index])
                
            self.columns["DATE"].extend(self.dates)
            self.columns["ASIN"].extend(self.stock_asin)
            self.columns["OFFER_ID"].extend(self.stock_offerid)
            # self.columns["SELLER_NAME"].extend(self.seller_name)
            self.columns["SELLER_NAME"].extend(seller)
            # self.columns["PRICE"].extend(self.stockprice)
            self.columns["PRICE"].extend(pprice)
            # self.columns["IS_FBA"].extend(self.isfba)
            self.columns["IS_FBA"].extend(isfba)
            self.columns["CONDITION"].extend(conditionofstock)
            # self.columns["CONDITION"].extend(self.condition)
            self.columns["BUYBOX_WINNER"].extend(buybox)
            # self.columns["BUYBOX_WINNER"].extend(self.buyboxwinner)
            self.columns["DELIVERY_DATE"].extend(stockdelivery)
            self.columns["STOCK_LEVEL"].extend(self.stock_level)
            self.columns["MIN_QUANTITY"].extend(self.min_quantity)
            self.columns["AVAILABILITY_MESSAGE"].extend(self.availability_message)
            self.columns["MESSAGE"].extend(self.message)
            self.columns["IS_PRIME"].extend(self.is_prime)
            self.columns["IN_STOCK"].extend(self.in_stock)
            self.columns["HAS_STOCK_ESTIMATION"].extend(self.has_stock_estimation)
            self.progressbar.emit(90)
            self.rows_present = self.rows_present + 1
            
            df = DataFrame({'DATE': self.dates, 'ASIN': self.stock_asin , 'OFFER_ID': self.stock_offerid,
                        'PRICE': pprice, 'SELLER_NAME': seller, 'IS_FBA':isfba , 
                        # 'SELLER_ID': self.seller_id,
                        'CONDITION': conditionofstock,'BUYBOX_WINNER': buybox, 'DELIVERY_DATE': stockdelivery,
                        'STOCK_LEVEL': self.stock_level,'MIN_QUANTITY': self.min_quantity,
                        'AVAILABILITY_MESSAGE': self.availability_message,'MESSAGE': self.message,
                        'IS_PRIME': self.is_prime,'IN_STOCK': self.in_stock,
                        'HAS_STOCK_ESTIMATION': self.has_stock_estimation})
            
            # df = DataFrame({'DATE': self.dates, 'ASIN': self.stock_asin , 'OFFER_ID': self.stock_offerid,
            #             'PRICE': self.stockprice, 'SELLER_NAME': self.seller_name, 'IS_FBA': self.isfba, 
            #             # 'SELLER_ID': self.seller_id,
            #             'CONDITION': self.condition,'BUYBOX_WINNER': self.buyboxwinner,
            #             'STOCK_LEVEL': self.stock_level,'MIN_QUANTITY': self.min_quantity,
            #             'AVAILABILITY_MESSAGE': self.availability_message,'MESSAGE': self.message,
            #             'IS_PRIME': self.is_prime,'IN_STOCK': self.in_stock,
            #             'HAS_STOCK_ESTIMATION': self.has_stock_estimation})
            
            df.to_excel('%s_stock_data.xlsx'%datetoday,sheet_name=self.tab_name, index=False)
            
            if (self.rows_present == 1):
                self.stock_sheet_object.write_data(self.columns, self.stock_sheet_object, self.tab_name,self.rows_present)
            else:
                self.stock_sheet_object.rewrite_data(self.columns, self.stock_sheet_object, self.tab_name,
                                                   self.rows_present)
        else:
            self.length_offers = len(self.OFFERS_DATA)
            self.number_of_times = self.length_offers/15000   
            self.output_no_times = math.modf(self.number_of_times)
            self.start = 0
            self.loop_end = round(self.number_of_times)
            self.loop_ending = self.loop_end
            if self.output_no_times[0] == 0.000:
                self.end = 15000
                self.increment = 15000
            if 0.00 < self.output_no_times[0] < 0.500:
                self.end = 15000
                self.increment = 15000
                self.loop_end = self.loop_end + 1
            if self.output_no_times[0] >= 0.50:
                self.end = 15000     
                self.increment = 15000 
            self.update.emit("Since the Data is greater than 15K, we will make multiple collections")
            
            for j in range(0, self.loop_end):
                number = j + 1
                self.update.emit("Collection Number: %s" %number)
                self.price_stock =[]
                self.price_stock = self.price[self.start:self.end]
                self.seller_name_stock = []
                self.seller_name_stock = self.seller_name[self.start:self.end]
                self.isfba_stock = []
                self.isfba_stock = self.isfba[self.start:self.end]
                self.condition_stock = []
                self.condition_stock = self.condition[self.start:self.end]
                self.buybox_winner_stock = []
                self.buybox_winner_stock = self.buyboxwinner[self.start:self.end]
                self.OFFERSDATA_chunk = []
                self.OFFERSDATA_chunk = self.OFFERS_DATA[self.start:self.end]
                self.length_offerdata = len(self.OFFERSDATA_chunk)
                self.ASINDATA_chunk = []
                self.ASINDATA_chunk = self.ASIN_DATA[self.start:self.end]
                self.length_asindata = len(self.ASINDATA_chunk)
                self.collection_id_stock = create_collection_stock.collection_creation()
                self.update.emit("Stock Estimation Collection Created.")
                self.update.emit("Stock's Collection ID is: %s" %self.collection_id_stock)
                self.progressbar.emit(60)
                try:
                    self.length_offers_stock = request_collection_stock.requesting_collection(self.collection_id_stock,
                                                                                          self.ASINDATA_chunk,self.OFFERSDATA_chunk)
                except Exception as d:
                    self.update.emit("%s" %d)
                    time.sleep(120)
                    self.length_offers_stock = request_collection_stock.requesting_collection(self.collection_id_stock,
                                                                                          self.ASINDATA_chunk,self.OFFERSDATA_chunk)
                self.update.emit("Stock Requested and Started.")
                try:
                    start_till_delect_collection.collection_started(self.collection_id_stock,self.length_offers_stock)
                except Exception as c:
                    self.update.emit("%s" %c)
                    time.sleep(120)
                    start_till_delect_collection.collection_started(self.collection_id_stock,self.length_offers_stock)
                self.progressbar.emit(70)
                self.update.emit("Finalizing Collection.")
                try:
                    start_till_delect_collection.stopping_collection(self.collection_id_stock)
                except Exception as b:
                    self.update.emit("%s" %b)
                    time.sleep(120)
                    start_till_delect_collection.stopping_collection(self.collection_id_stock)
                self.update.emit("Stock Estimation Collection Stopped.")
                try:
                    self.length_results, self.result_links = start_till_delect_collection.getting_results(self.collection_id_stock)
                except Exception as a:
                    self.update.emit("%s" %a)
                    time.sleep(120)
                    self.length_results, self.result_links = start_till_delect_collection.getting_results(self.collection_id_stock)
                # start_till_delect_collection.collection_deletion(self.collection_id_stock)
                self.update.emit("Stock Estimation Collection Completed.")
                self.progressbar.emit(80)
                self.no_of_rows = self.stock_sheet_object.read_data(self.stock_sheet_object, self.tab_name)
                self.no_of_rows = self.no_of_rows + 1
                self.dates = []
                self.stock_asin = []
                self.stock_offerid = []
                self.stock_level = []
                self.min_quantity = []
                self.availability_message = []
                self.message = []
                self.is_prime = []
                self.in_stock = []
                self.has_stock_estimation = []
                self.stockprice = []
                self.update.emit("Collecting Stock Estimation Data.")
                for i in range(0, self.length_results):
                    self.results_to_sheet = self.result_links[i]
                    print(self.results_to_sheet)
                    date, stockasin, stockofferid, stock_price, stocklevel, minquantity, \
                    availabilitymessage, Message, isprime, instock, \
                    hasstockestimation = stock_data.output_data(self.results_to_sheet)
                    self.dates.extend(date)
                    self.stock_asin.extend(stockasin)
                    self.stock_offerid.extend(stockofferid)
                    # self.stockprice.extend(stock_price)
                    self.stock_level.extend(stocklevel)
                    self.min_quantity.extend(minquantity)
                    self.availability_message.extend(availabilitymessage)
                    self.message.extend(Message)
                    self.is_prime.extend(isprime)
                    self.in_stock.extend(instock)
                    self.has_stock_estimation.extend(hasstockestimation)
                    
                seller = []
                isfba = []
                conditionofstock = []
                buybox = []
                pprice = []
                deliverydate = []
                for i in range(0,len(self.stock_offerid)):
                    index = self.OFFERS_DATA.index(self.stock_offerid[i])
                    seller.append(self.seller_name[index])
                    isfba.append(self.isfba[index])
                    conditionofstock.append(self.condition[index])
                    buybox.append(self.buyboxwinner[index])
                    pprice.append(self.price[index])
                    deliverydate.append(delivery_time[index])
                    
                self.columns["DATE"].extend(self.dates)
                self.columns["ASIN"].extend(self.stock_asin)
                self.columns["OFFER_ID"].extend(self.stock_offerid)
                self.columns["SELLER_NAME"].extend(seller)
                self.columns["PRICE"].extend(pprice)
                self.columns["IS_FBA"].extend(isfba)
                self.columns["CONDITION"].extend(conditionofstock)
                self.columns["BUYBOX_WINNER"].extend(buybox)
                self.columns["DELIVERY_DATE"].extend(deliverydate)
                self.columns["STOCK_LEVEL"].extend(self.stock_level)
                self.columns["MIN_QUANTITY"].extend(self.min_quantity)
                self.columns["AVAILABILITY_MESSAGE"].extend(self.availability_message)
                self.columns["MESSAGE"].extend(self.message)
                self.columns["IS_PRIME"].extend(self.is_prime)
                self.columns["IN_STOCK"].extend(self.in_stock)
                self.columns["HAS_STOCK_ESTIMATION"].extend(self.has_stock_estimation)
                self.progressbar.emit(90)
                
                df = DataFrame({'DATE': self.dates, 'ASIN': self.stock_asin , 'OFFER_ID': self.stock_offerid,
                        'PRICE': pprice, 'SELLER_NAME': seller,
                        'IS_FBA': isfba, 
                        'CONDITION': conditionofstock,'BUYBOX_WINNER': buybox, 'DELIVERY_DATE' : deliverydate,
                        'STOCK_LEVEL': self.stock_level,'MIN_QUANTITY': self.min_quantity,
                        'AVAILABILITY_MESSAGE': self.availability_message,'MESSAGE': self.message,
                        'IS_PRIME': self.is_prime,'IN_STOCK': self.in_stock,
                        'HAS_STOCK_ESTIMATION': self.has_stock_estimation})
                numdate= str(datetoday) + "_" + str(number)
                df.to_excel('stock_data_%s.xlsx' %numdate,sheet_name=self.tab_name, index=False)
                
                # if (self.no_of_rows == 1):
                #     self.stock_sheet_object.write_data(self.columns, self.stock_sheet_object, self.tab_name,
                #                                        self.no_of_rows)
                # else:
                #     self.stock_sheet_object.rewrite_data(self.columns, self.stock_sheet_object, self.tab_name,
                #                                          self.no_of_rows)
                self.start = self.end
                self.end = self.end + self.increment

                if 0.00 < self.output_no_times[0] < 0.500 and j == (self.loop_ending - 1):
                    self.end = self.end - self.increment
                    self.end = self.end + (self.length_offers - (self.loop_ending * 15000))

                if self.output_no_times[0] > 0.5000 and j == (self.loop_end - 2):
                    self.end = self.end - self.increment
                    self.end = self.end + (self.length_offers - ((self.loop_end - 1) * 15000)) 
            

            df = DataFrame({'DATE': self.columns['DATE'], 'ASIN': self.columns["ASIN"] , 
                        'OFFER_ID': self.columns["OFFER_ID"],
                        'PRICE': self.columns["PRICE"], 'SELLER_NAME': self.columns["SELLER_NAME"],
                        'IS_FBA': self.columns["IS_FBA"], 
                        'CONDITION': self.columns["CONDITION"],'BUYBOX_WINNER': self.columns["BUYBOX_WINNER"],
                        'DELIVERY_DATE' : self.columns["DELIVERY_DATE"],
                        'STOCK_LEVEL': self.columns["STOCK_LEVEL"],'MIN_QUANTITY': self.columns["MIN_QUANTITY"],
                        'AVAILABILITY_MESSAGE': self.columns["AVAILABILITY_MESSAGE"],'MESSAGE': self.columns["MESSAGE"],
                        'IS_PRIME': self.columns["IS_PRIME"],'IN_STOCK': self.columns["IN_STOCK"],
                        'HAS_STOCK_ESTIMATION': self.columns["HAS_STOCK_ESTIMATION"]})
            
            df.to_excel('stock_data_%s_final.xlsx'%datetoday,sheet_name=self.tab_name, index=False)
            
            try:
                if (self.no_of_rows == 1):
                        self.stock_sheet_object.write_data(self.columns, self.stock_sheet_object, self.tab_name,
                                                        self.no_of_rows)
                else:
                    self.stock_sheet_object.rewrite_data(self.columns, self.stock_sheet_object, self.tab_name,
                                                            self.no_of_rows)
            except Exception as e:
                self.update.emit('%s' %e)
                self.update.emit("CANNOT UPLOAD TO GOOGLE SHEET. AS GOOGLESHEET CRASHED OR REACHED TO MAX LIMIT")
                self.update.emit("DATA STORED IN EXCEL.")
                
        
        self.update.emit("Stock Estimation Data Uploaded to GoogleSheet..!!")
        self.progressbar.emit(100)
