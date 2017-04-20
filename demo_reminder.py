import os
import gspread
import datetime
import time
from oauth2client.service_account import ServiceAccountCredentials
from slackclient import SlackClient
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# need to set this locally
slack_client = SlackClient(SLACK_BOT_TOKEN)


# access a spreadsheet

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
workbook = client.open("BAP Demo Sign Ups (Responses) - New")
sheet=workbook.worksheet("Master Sheet")

data = sheet.get_all_values()

date=datetime.datetime.now()

todays_date=str("%s/%s/%s" % (date.month, date.day, date.year))


proctors=[]
for line in data:
    if line==data[0]: #skips the first row
        continue
    else:
        if line[0]=='':#stops this loop once we reach the end of the spreadsheet
            break
        else:
            if line[5]==todays_date:#finds the proctors name and adds that person to the list of todays proctors
                proctor_name=line[6]
                proctors.append(proctor_name)

#following section put in place to have you check the name(s) of the people it will send to
print proctors
confirmation_of_list=raw_input("Does this list look right? (y or n)")
correct_answer=set(['yes','y'])
if confirmation_of_list not in correct_answer:
    print "Check the doc, something is wrong. Then try again"
    quit()

#slack message that will be sent
message = 'Hey someone signed up for a demo and today is your day to proctor. Check here https://goo.gl/BpsZNq to see the detials'
sent_to=[]


count=0
response = slack_client.api_call('users.list') #pulls full list of users in slack
users = response['members']
for user in users:
    realname = user['profile']['real_name'] #pulls the users full name
    for proctor in proctors:
        if realname.startswith(proctor): #found a match with a proctor based on full name
            sent_to.append(proctor) #adds proctors to the send to list
            user_id = user['id'] #gets their id
            slack_client.api_call('chat.postMessage', channel=user_id, text=message, as_user=True) #sends the messag
            count+=1
            time.sleep(1.5)
            if count >=2: #making sure im not sending a message to the whole company on accident. should only go to 1 MAYBE 2 people max.
                print 'Caught the bot sending to more then 2 people. Shutting Down.....'
                quit()

not_sent_to = [x for x in proctors if x not in sent_to]

# prints back a message about what it did

if len(not_sent_to) == 0:
    print "Successfully sent to {} proctor!".format(len(proctors))
else:
    print "Successfully sent to {} proctor(s)!".format(len(sent_to))
    print "Did Not Send To", not_sent_to
