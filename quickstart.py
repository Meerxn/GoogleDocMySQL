import mysql.connector
#from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
infoDict = {}
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = 'YOUR GOOGLE DOC ID HERE'

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
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="presentations"
    ) 
    mycursor = mydb.cursor()
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
    texter = (met(document.get('body').get('content')))
    texter = texter.replace("\n", "$")
    res = texter.split("$")
    ans = []
    found = 0 # Flag to see if we found where to start scraping from.
    # Sort out different size of ' '
    for i in range(len(res)):
        if res[i] == 'Language skills':
            break
        if res[i] != '' and found == 1:
            ans.append(res[i].replace("\t","").strip(" "))
        # Check in document to start scraping the data from
        if res[i] == 'Listed among the 6 UW-Madison CALS specialists having the greatest reach through media in 2020.':
            found = 1
    yearStart = 2008
    for i in range (15):
        infoDict[str(yearStart)] = ""
        yearStart+=1    
    start_scrape = False
    currIndex = 0 
    while currIndex < len(ans):
        tempIndex = 0

        if ans[currIndex] in infoDict.keys():
            tempIndex = currIndex + 1
            temp = []
            curryear = ans[currIndex]
            while ans[tempIndex] not in infoDict.keys() and tempIndex < len(ans) - 1:
                if "/" in  ans[tempIndex] and len(ans[tempIndex]) <= 11:
                    entry  = {}
                    entry ["date"] = ans[tempIndex]
                    entry["event"] = ans[tempIndex+1]
                    temp.append(entry)
                tempIndex +=1
            infoDict[curryear] = temp 
        currIndex +=1
    for k in infoDict:
      if k != "2020":
        for i in range (len(infoDict[k])):
          print(infoDict[k][i]['event'])
          sql = "INSERT INTO tester_presentation (year,date,event) VALUES (%s,%s, %s)"
          val = (k,infoDict[k][i]['date'],infoDict[k][i]['event'])
          mycursor.execute(sql, val)

    mydb.commit()
    #change
    #hdjdj


     
    
if __name__ == '__main__':
    main()



