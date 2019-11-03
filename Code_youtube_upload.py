import sqlite3
import xlrd
import requests
import googleapiclient
import google_auth_oauthlib
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors



scopes = ["https://www.googleapis.com/auth/youtube.upload"]



class upload:
    def __init__(self):
        self.video1_file_path = ""
        self.title_of_video = ""
        self.video_description = ""
        self.video_tags = ""
        self.category_id = ""
        self.privacy_status = ""
        self.file_path_thumbnail = ""
        self.channel_id = ""
        print("ENTER PATH OF FILE")
        self.path = input()
        self.open_excel_file()
        print(self.path)


    def open_excel_file(self):
        loc = str(self.path)
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)
        column = sheet.ncols
        rows = sheet.nrows
        youtube = self.authorization()
        for j in range(0,column):
            for i in range(1,rows):
                self.video1_file_path = sheet.cell_value(i,0)
                self.title_of_video = sheet.cell_value(i,1)
                self.video_description = sheet.cell_value(i,2)
                self.video_tags = sheet.cell_value(i,3)
                self.category_id = sheet.cell_value(i,4)
                self.privacy_status = sheet.cell_value(i,5)
                self.file_path_thumbnail = sheet.cell_value(i,6)
                self.channel_id = sheet.cell_value(i,7)
                print(sheet.cell_value(i,j))
                self.initialize_upload(youtube)

    def authorization(self) :
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_credentials.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
        credentials = flow.run_console()
        return googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    def initialize_upload(self,youtube):
        body=dict(
        snippet = dict(
        title=self.title_of_video,
        description=self.video_description,
        tags=self.video_tags,
        categoryId=self.category_id,
        file1 = self.video1_file_path,
        channelid = self.channel_id
        ),
        status=dict(
        privacyStatus=self.privacy_status
        )
        )
        insert_request = youtube.videos().insert(part=",".join(body.keys()),
            body=body,
        media_body=MediaFileUpload(self.video1_file_path,chunksize=-1, resumable=True))


ud = upload()
