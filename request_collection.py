import requests
import json
import pandas as pd
import math


def requesting_collection(id,data):
  def asins(asin_list, body, start, end):
    print(len(asin_list[start:end]))
    for i in range(start, end):
      asin = asin_list[i]
      dictionary = {
        "type": "offers",
        "amazon_domain": "amazon.com",
        "asin": asin,
        # "max_page": '5',
        # 'offers_condition_new': 'true',
        "custom_id": "BI_025"}
      body['requests'].append(dictionary)
    return body,start,end
  print("Length of data in request: " , len(data))
  data_frame = pd.DataFrame(data)
  asin_list = data_frame['ASIN'].tolist()
  length_asin = len(asin_list)
  print("ASINS" , length_asin)
  if length_asin > 15000:
    length_asin = 15000
    # print("Your ASINS are more than 15000 only 15000 will be processed")

  number_of_times = (length_asin / 1000)
  output_no_times = math.modf(number_of_times)
  start = 0
  loop_end = round(number_of_times)
  loop_ending = loop_end

  if length_asin < 1000:
    end = length_asin
    loop_end = 1
    increment = 0

  if output_no_times[0] == 0.000 and length_asin > 1000:
    end = 1000
    increment = 1000


  if 0.00 < output_no_times[0] < 0.500 and length_asin > 1000:
    end = 1000
    increment = 1000
    loop_end = loop_end + 1
  if output_no_times[0] >= 0.5000 and length_asin > 1000:
    end = 1000
    increment = 1000


  for j in range(0, loop_end):
    body = {"requests": []}
    params,start,end = asins(asin_list, body, start, end)
    start = end
    end = end + increment

    if 0.00 < output_no_times[0] < 0.500 and j == (loop_ending - 1):
      end = end - increment
      end = end + (length_asin - loop_ending * 1000)

    if output_no_times[0] >= 0.5000 and j == (loop_end - 2):
      end = end - increment
      end = end + (length_asin - ((loop_end - 1) * 1000))

    # print(end, " Requests")

    parameter_requuest_length = len(params['requests'])

    if parameter_requuest_length <= 1000:
      api_result = requests.put('https://api.rainforestapi.com/collections/%s?api_key=86E4DDAC37A940799F93131032482B7D' % id, json=params)
      api_response = api_result.json()
      # print("Collection [",j + 1,"] Requested: ", json.dumps(api_response))

  return length_asin



