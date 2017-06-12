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
sheet=workbook.worksheet("TODAYS DEMOS")

data = sheet.get_all_values()

date=datetime.datetime.now()

todays_date=str("%s/%s/%s" % (date.month, date.day, date.year))

name=sheet.cell(6,1).value
demos_today_count=sheet.cell(4,1).value


#following section put in place to have you check the name(s) of the people it will send to
print name
print demos_today_count
one_message = 'Hey ' + name + ', ' + demos_today_count + ' person signed up for a demo today and it is your day to proctor. Check here https://goo.gl/3ALWHa to see the detials'
multi_message = 'Hey '+ name + ', ' + demos_today_count + ' people signed up for a demo today and it is your day to proctor. Check here https://goo.gl/3ALWHa to see the detials'
none_message = 'Hey ' + name + ', its your lucky day!!!! There are no Demos Scheduled for today'
channel='G052CAF9D'
#slack message that will be sent
try:
    if int(demos_today_count) == 0:
        slack_client.api_call('chat.postMessage', channel=channel, text=none_message, as_user=True)
    elif int(demos_today_count) >=2:
        slack_client.api_call('chat.postMessage', channel=channel, text=multi_message, as_user=True)
    else:
        slack_client.api_call('chat.postMessage', channel=channel, text=one_message, as_user=True)
except:
    slack_client.api_call('chat.postMessage', channel=channel, text="SOMETHING WENT WRONG!!! Check Lambda", as_user=True)
