import requests
import results_sets
import json
import time

def collection_started(id,length_asin):
  params = {
    'api_key': '86E4DDAC37A940799F93131032482B7D'
  }

  api_result1 = requests.get('https://api.rainforestapi.com/collections/%s/start' % id, params)

  api_response1 = api_result1.json()
  
  def status(id):
    api_result = requests.get('https://api.rainforestapi.com/collections/%s'% id, params)
    api_response = api_result.json()
    return api_response
  api_response2 = status(id)
  
  while api_response2['collection']['status'] == 'idle':
    api_response2 = status(id)
  while api_response2['collection']['status'] == 'queued':
    print('Collection is Queued')
    time.sleep(2)
    api_response2 = status(id)
  while api_response2['collection']['status'] == 'running':
    print("Collection is Running")
    api_response2 = status(id)
    time.sleep(5)
  # time.sleep(20)
  print("********* D O N E ***********")
  
def stopping_collection(id):
    params = {
      'api_key': '86E4DDAC37A940799F93131032482B7D'
    }

    api_result = requests.get('https://api.rainforestapi.com/collections/%s/stop' % id, params)

    api_response = api_result.json()

    # print("Collection stopped.")



def getting_results(id):
    params = {'api_key': '86E4DDAC37A940799F93131032482B7D'}

    api_result = requests.get('https://api.rainforestapi.com/collections/%s/results/1' %id, params)

    api_response = api_result.json()
    #
    # print("Results Got: ",json.dumps(api_response))
    #
    # print("Click on this link to download JSON file zip of page: ")
    #
    # print(api_response['result']['download_links']['all_pages'])

    length_results = len(api_response['result']['download_links']['pages'])

    result_links = api_response['result']['download_links']['pages']

    return length_results, result_links

def collection_deletion(id):
    api_result = requests.delete('https://api.rainforestapi.com/collections/%s?api_key=86E4DDAC37A940799F93131032482B7D' % id)

