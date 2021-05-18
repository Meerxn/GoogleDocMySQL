from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1vSckSVKBuVbFeeZ5LKPiuaotavrdjLayPXSpxay0XPo'

def read_paragraph_element(element):
    """Returns the text in the given ParagraphElement.

        Args:
            element: a ParagraphElement from a Google Doc.
    """
    
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')

def met(element):
    text = ''
    for val in element:
        if "paragraph" in val:
            elements = val.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in val:
            # The text in table cells are in nested Structural Elements and tables may be
            # nested.
            table = val.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += met(cell.get('content'))
        elif 'tableOfContents' in val:
            # The text in the TOC is also in a Structural Element.
            toc = val.get('tableOfContents')
            text += met(toc.get('content'))
    return text


def main():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()
    #print(document.get('body').get('content'))

    print('The Content of the document is: {}'.format(met(document.get('body').get('content'))))


if __name__ == '__main__':
    main()