#!env python
import pickle
import os
import os.path as path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

# If read only mode is desired, uncomment this:
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

CREDS_FILE = __file__.replace(path.basename(__file__), "credentials.json")
PICKLE_FILE = __file__.replace(path.basename(__file__), "token.pickle")

services = []

def get_service():
    if len(services) > 0:
        return services[0]

    creds = None
    if os.path.exists(PICKLE_FILE):
        with open(PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    services.append(service)
    return service

def get_twilight_mail():
    service = get_service()
    query_ts = 'from:playdekgames.com subject:"Twilight Struggle Game" is:unread"'

    results = service.users().messages().list(userId='me', q=query_ts).execute()

    number = results['resultSizeEstimate']
    messages = results.get("messages", [])

    mail_service = service.users().messages()

    return messages

def get_counts():
    messages = get_twilight_mail()
    mail_service = get_service().users().messages()
    if len(messages) == 0:
        return 0, {}, {}

    gameIds = {}
    playerCounts = {}
    for m in messages:
        message = mail_service.get(userId='me', id=m['id'], format="metadata").execute()
        for header in message['payload']['headers']:
            if header['name'].lower() == "subject":
                subject = header['value']
                break
        gameid = subject.split(" ")[-1]
        snippet = message['snippet']
        oppo = snippet.split(" ")[-1].replace("!", "")
        gameIds[gameid] = gameIds.get(gameid, 0) + 1
        playerCounts[oppo] = playerCounts.get(oppo, 0) + 1

    return len(messages), gameIds, playerCounts

def markread():
    messages = get_twilight_mail()
    if len(messages) == 0:
        return
    mail_service = get_service().users().messages()

    body = {}
    ids = [m['id'] for m in messages]
    body['ids'] = ids
    body['removeLabelIds'] = ["UNREAD"]
    mail_service.batchModify(userId='me', body=body).execute()

