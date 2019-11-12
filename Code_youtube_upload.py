import os
import time
import xlrd
import random
import httplib2
import http.client
import googleapiclient
import google_auth_oauthlib
import googleapiclient.errors
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError,
  http.client.IncompleteRead, http.client.ImproperConnectionState,
  http.client.CannotSendRequest, http.client.CannotSendHeader,
  http.client.ResponseNotReady, http.client.BadStatusLine)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

scopes = ["https://www.googleapis.com/auth/youtube.upload"]


class upload:
    def __init__(self):
        self.video1_file_path = ""
        self.title_of_video = ""
        self.video_description = ""
        self.video_tags = ""
        self.category_id = int
        self.privacy_status = ""
        self.file_path_thumbnail = ""
        self.channel_id = ""
        self.file_name = ""
        print("ENTER PATH OF FILE")
        self.path = input()
        self.open_excel_file(1)
#        print(self.path)


    def open_excel_file(self,start):
        loc = str(self.path)
        self.start=start
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        column = sheet.ncols
        rows = sheet.nrows
        print(rows,column)
        youtube = self.authorization()
        for i in range(start,rows):
            for j in range(0,column):
                self.video1_file_path = sheet.cell_value(i,0)
                self.title_of_video = sheet.cell_value(i,1)
                self.video_description = sheet.cell_value(i,2)
                self.video_tags = sheet.cell_value(i,3)
                self.category_id =int(sheet.cell_value(i,4))
                self.privacy_status = sheet.cell_value(i,5)
                self.file_path_thumbnail = sheet.cell_value(i,6)
                self.channel_id = sheet.cell_value(i,7)
                self.file_name = sheet.cell_value(i,8)
                #print(sheet.cell_value(i,j))
            self.initialize_upload(youtube)
        #    self.resumable_upload(self.insert_request)
        if i<rows:
            open_excel_file(i)
        else :
            print('uploaded')

    def authorization(self) :
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = r"C:\Users\Devhuti\Desktop\client_credentials3.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
        credentials = flow.run_console()
        return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    def initialize_upload(self,youtube):
        self.body=dict(
        snippet = dict(
        title=self.title_of_video,
        description=self.video_description,
        tags=self.video_tags,
        categoryId=self.category_id,
        file = self.video1_file_path,
        channelid = self.channel_id,
        ),
        status=dict(
        privacyStatus=self.privacy_status
        ),
        fileDetails=dict(
        fileName = self.file_name)
        )
        self.insert_request = youtube.videos().insert(part=",".join(self.body.keys()),
        body=self.body,
        media_body=MediaFileUpload(self.video1_file_path,chunksize=-1, resumable=True))
        #media_body.
        self.insert_request.execute()
        

    
ud = upload()

