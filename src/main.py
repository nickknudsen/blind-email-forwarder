from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    label_ids = ['UNREAD']

    results = service.users().messages().list(userId='me', labelIds=label_ids).execute()
    messages = []

    if 'messages' in results:
        messages.extend(results['messages'])
    while 'nextPageToken' in results:
        page_token = results['nextPageToken']
        results = service.users().messages().list(userId='me', labelIds=label_ids).execute()

        messages.extend(results[messages])

    if not messages:
        print('No unread messages found.')
    else:
        print('Message Ids:')
        for messageId in messages:
            print(messageId['id'])

if __name__ == '__main__':
    main()
