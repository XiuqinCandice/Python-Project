#Xiuqin Gao Homework7

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pandas as pd
import os
#Allows user enters another tag/filter except from 'networking' to get target event info.
print('This little application is to facilate your networking events searching process')
choicesList = ['', 'Career', 'Real+estate','Startups', 'Finance', 'Job fair']
print('Choose a tag from', choicesList)
def getChoices(a, b):
    while True:
        if a in b:
            break
        else:
            a = input('That is incorrect, please try again:\n>>')
choice = input('Please enter a tag from the abvoe line that you wanna add:\n>>')
getChoices(choice, choicesList)

#get event info including title, location, time, each event url and put them into list separately.
titleList = []
locationList = []
timeList = []
eventUrlList = []
url = 'https://www.eventbrite.com/d/ny--new-york/networking/?page=1&tags='+choice
urlOpen = urlopen(url)
soup = bs(urlOpen,'html.parser')

#get event title
for a in soup.find_all('div', {'class':'card-text--truncated__three'}):
    title=a.get_text() 
    titleList.append(title)
#get event location    
for b in soup.find_all('div', {'class':'card-text--truncated__one'}):
    location =b.get_text()
    locationList.append(location)    
#get time    
for c in soup.find_all('div', {'class':'eds-media-card-content__sub-content'}):
    time = c.find('div', {'class': 'eds-text-bs--fixed eds-text-color--grey-600 eds-l-mar-top-1'}).get_text()     
    timeList.append(time)      
#get event url#if interested in that, click in url and get more information 
for d in soup.find_all('div', {'class':'eds-media-card-content__primary-content'}):
    eventLink=d.find(tabindex="0")['href']    
    eventUrlList.append(eventLink)

#Merge/pair the above four lists into an arranged frame.
eventList = []
eventList = list(zip(titleList, locationList, timeList, eventUrlList))
for e in eventList:
    #print(e)
    df = pd.DataFrame(eventList)
print('\n')
#Handle permission error, this error happens when user doesn't run the program as administrator.
try:
    df.to_csv('C:/Users/michael.deamer/Desktop/Python IO/networkingEvent.csv')
    print('The networkingEvent.csv is created successfully.')
except PermissionError:
    print('Permission denied: \'C:/Users/michael.deamer/Desktop/Python IO/networkingEvent.csv\', you should run this application as administrator')
#Make the column name meaningful by changing the original column name(0,1,2,3,4) into (No., Title, Location, Time, Url)
fileName = 'C:/Users/michael.deamer/Desktop/Python IO/networkingEvent.csv'
tempFileName = 'C:/Users/michael.deamer/Desktop/Python IO/networkingEvent_temp.csv'
with open(fileName, 'r', encoding = 'utf-8') as file, open(tempFileName, 'a', encoding = 'utf-8') as tempFile:
    #write header to temp file
    headerRow = 'No.,Title,Location,Time,Url,\n'
    tempFile.write(headerRow)
    #write content of old file to temp file
    line = file.readline()
    line = file.readline()
    while line!='':
        tempFile.write(line)
        line = file.readline()
os.remove('C:/Users/michael.deamer/Desktop/Python IO/networkingEvent.csv')
os.rename('C:/Users/michael.deamer/Desktop/Python IO/networkingEvent_temp.csv',
          'C:/Users/michael.deamer/Desktop/Python IO/networkingEvent.csv')
#obtain event description

#User select target event info by only provide the No. of the event in the csv file
print('\n')
print('Check the file \'networkingEvent.csv\'created in your computer.')
eventNoList = []
while 1==1:
    number = input('Enter the event No. you are satisfied with, like \'1\' or press \'n\' to exit:\n>>')
    if number == 'n':
        break
    i = int(number)
    eventNoList.append(i)
eventFrame=pd.read_csv(fileName)
eventFrame = eventFrame[['No.','Title','Location', 'Time', 'Url']]
for i in eventNoList:  
    print(eventFrame.iloc[i])
    

    
