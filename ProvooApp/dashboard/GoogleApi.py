import os
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from apiclient import errors
import base64
import email
from django.core.files.storage import FileSystemStorage
import cStringIO

# ----Variables para utilizar la Api Stand Alone------
# try:
#     import argparse
#     flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
#     print(flags)
# except ImportError:
#     flags = None
#
# # If modifying these scopes, delete your previously saved credentials
# # at ~/.credentials/gmail-python-quickstart.json
# SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
# #CLIENT_SECRET_FILE = os.path.join(os.path.dirname(__file__), '..', 'static/client_secret.json')
# APPLICATION_NAME = 'ProvoFact'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(
            userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])
        return messages
    except errors.HttpError, error:
        print 'An error occurred: %s' % error


def GetAttachments(service, user_id, msg_id):

    """Get and store attachment from Message with given id.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    prefix: prefix which is added to the attachment filename on saving
    """
    file_return = {}
    try:
        message = service.users().messages().get(
            userId=user_id, id=msg_id).execute()
        for part in message['payload']['parts']:
            newvar = part['body']
            if 'attachmentId' in newvar:
                att_id = newvar['attachmentId']
                att = service.users().messages().attachments().get(
                    userId=user_id, messageId=msg_id, id=att_id).execute()
                data = att['data']
                if part['filename']:
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    print("estes esle archivo: %s" % (part['filename']))
                    file_return['name'] = part['filename']
                    file_return['data'] = file_data
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

    return file_return

# ----- Stand Alone Exexcution Gmail API -----
# def main():
#     """Shows basic usage of the Gmail API.
#
#     Creates a Gmail API service object and outputs a list of label names
#     of the user's Gmail account.
#     """
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('gmail', 'v1', http=http)
#     results = service.users().labels().list(userId='me').execute()
#     labels = results.get('labels', [])
#
#     if not labels:
#         print('No labels found.')
#     else:
#         print('Labels:')
#         for label in labels:
#             print(label['name'])
#
#         print(listemails)
#
#
# if __name__ == '__main__':
#     main()
