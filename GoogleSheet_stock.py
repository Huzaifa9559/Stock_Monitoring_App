import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


class GoogleSheet_SE:
    def __init__(self, credentials_file, sheet_key):
        self.credentials_file = credentials_file
        self.sheet_key = sheet_key

        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        self.sheet_object = self._get_sheet_object()

    def _get_sheet_object(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file, self.scope
        )
        client = gspread.authorize(credentials)
        return client.open_by_key(self.sheet_key)

    def create_tabs(self, obj_link, tab_name):
        worsheet_list = obj_link.sheet_object.worksheets()
        tab_name_list = []
        for single_tab in worsheet_list:
            tab_name_list.append(single_tab.title)

        if tab_name in tab_name_list:
            # print(tab_name," Tab already present")
            pass
        else:
            # print(tab_name," Tab not present")
            worksheet = obj_link.sheet_object.add_worksheet(title=tab_name, rows="10000", cols="50")
        return tab_name

    def read_data(self, obj_link, worksheet_name):
        previous_data = obj_link.sheet_object.worksheet(worksheet_name).get_all_values()
        if len(previous_data) == 0:
            # print(worksheet_name," Sheet is empty")
            rows_present = 0
            pass
        else:
            # print(worksheet_name, " Sheet is not empty")
            rows_present = len(previous_data)
            # print(rows_present, " rows are present")
            # Date_data1 = []
            # j = 0
            # print("Offers Sheet is not empty")
            # for i in range(1,len(previous_data)):
            #     Date_data1.append(previous_data[i][0])
            #     if 'DATE' in Date_data1:
            #         j += 1
            #         Date_data1.remove('DATE')
            # rows_present = len(Date_data1) +j + 2
            # Date_data2 = np.array(Date_data1)
            # unique_dates = np.unique(Date_data2)
            # length = len(unique_dates)
            # print("Uniques Dates are: ", unique_dates, "and Number of Uniques Dates are:",length)
            # if length == 1 or length == 2:
            #     print("You can Write Data")
            # else:
            #     obj_link.sheet_object.worksheet(worksheet_name).clear()
            #     print("Sheet cleared")
        return rows_present

    # def write_data(self,data,obj_link,tab_name,column,column_name,rows):
    #     data = pd.DataFrame(data,columns=[column_name])
    #     # data = pd.DataFrame(data)
    #     set_with_dataframe(obj_link.sheet_object.worksheet(tab_name), dataframe=data, row=rows, col=column)

    def write_data(self,data,obj_link,tab_name,rows):
        data = pd.DataFrame(data)
        # data = pd.DataFrame(data)
        set_with_dataframe(obj_link.sheet_object.worksheet(tab_name), dataframe=data, row=rows, col=1)
        obj_link.sheet_object.worksheet(tab_name).add_rows(rows=1)

    def rewrite_data(self,data,obj_link,tab_name,rows):
        data = pd.DataFrame(data)
        set_with_dataframe(obj_link.sheet_object.worksheet(tab_name), dataframe=data, include_column_header=False, row=rows, col=1)
        obj_link.sheet_object.worksheet(tab_name).add_rows(rows=1)

    def datatostore(self, obj_link, worksheet_name):
        previous_data = obj_link.sheet_object.worksheet(worksheet_name).get_all_values()
        return previous_data

    def cleardata(self, obj_link, worksheet_name):
        obj_link.sheet_object.worksheet(worksheet_name).clear()