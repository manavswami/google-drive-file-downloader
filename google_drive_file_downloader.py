#!/usr/bin/env python
# coding: utf-8

# In[5]:

from __future__ import print_function
import pickle
import os.path
import io
import shutil
import requests
from mimetypes import MimeTypes
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload   
global SCOPES

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/drive']
# Variable self.creds will
# store the user access token.
# If no valid token found
# we will create one.
creds = None
# The file token.pickle stores the
# user's access and refresh tokens. It is
# created automatically when the authorization
# flow completes for the first time.
# Check if file token.pickle exists
if os.path.exists('token.pickle'):
    # Read the token from the file and
    # store it in the variable self.creds
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If no valid credentials are available,
# request the user to log in.
if not creds or not creds.valid:

    # If token is expired, it will be refreshed,
    # else, we will request a new one.
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'newkey.json', SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the access token in token.pickle
    # file for future usage
    with open('token.pickle', 'wb') as token:
        pickle.dump(self.creds, token)

# Connect to the API service
service = build('drive', 'v3', credentials=creds)

# request a list of first N files or
# folders with name and id from the API.
results = service.files().list(pageSize=100, fields="files(id, name)").execute()
items = results.get('files', [])

# print a list of files
print("Here's a list of files: \n")
print(*items, sep="\n", end="\n\n")

file_id = input("Enter file id: ")
request = service.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
Save_filename = input("save file as: ")
while done is False:
    status, done = downloader.next_chunk()
    print ("Download %d%%." % int(status.progress() * 100))
    fh.seek(0)
    
    with open(Save_filename, 'wb') as f:
        f.write(fh.read())
        f.close()
    print ("OK")
    
    
    
    
    
    





