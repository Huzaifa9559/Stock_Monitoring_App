import requests
import json
import datetime
import random


def collection_creation():
  e = datetime.datetime.now()
  date1 = e.strftime("%d/%m/%Y")
  date2 = date1.replace("/", "_")
  date = date2 
  # + "_" + str(random.randint(0, 10))
  body = {
    "name": "Stock_Collection_%s" %date,
    "enabled": True,
    "schedule_type": "manual",
    "priority": "highest",
    "requests_type": "stock_estimation",
    "notification_as_csv": True,
    "notification_as_json": True
  }

  api_result = requests.post('https://api.rainforestapi.com/collections?api_key=86E4DDAC37A940799F93131032482B7D', json=body)

  api_response = api_result.json()

  # print ("Collection Created: ", json.dumps(api_response))

  id = api_response['collection']['id']

  # print("Collection ID is: ", id)
  return id


