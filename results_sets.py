import requests
import json

def collection_result_sets(id):
    params = {
      'api_key': '86E4DDAC37A940799F93131032482B7D'
    }

    api_result = requests.get('https://api.rainforestapi.com/collections/%s/results' % id, params)

    api_response = api_result.json()

    # print("List Of Result Sets: ", json.dumps(api_response))
    return api_response