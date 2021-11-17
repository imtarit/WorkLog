import numpy as np
import pandas as pd
import datetime
import os

toDay = datetime.datetime.now()
# print(toDay)
# print(toDay.weekday())

# monDay = toDay - datetime.timedelta(toDay.weekday())

# print(monDay)

# print(toDay)
# print(datetime.datetime.strftime(toDay, '%d/%m/%Y'))

def createProject():
    projectName = str(input('Write project name: ') or 'None')
    return projectName

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds
td = datetime.timedelta(2, 7743, 12345)
hours, minutes, seconds = convert_timedelta(td)
print(str(minutes) + ':' + str(hours))


i = str(input('Working date in formate "dd/mm/yyyy": ') or datetime.datetime.strftime(toDay, '%d/%m/%Y'))
try:
    workDay = datetime.datetime.strptime(i, '%d/%m/%Y')
except ValueError:
    print("Incorrect format")

monDay = workDay - datetime.timedelta(workDay.weekday())

fileName = './' + datetime.datetime.strftime(monDay,'%Y_%m_%d') + '.csv'

if (os.path.isfile(fileName)):
    df = pd.read_csv(fileName, index_col=0)
    print("Exisitng table: ")
    print(df)
    print("Existing project list: ")
    uniqueProject = df['project'].unique()
    for index in range(uniqueProject.shape[0]):
        print(str(index+1) +' : ' + uniqueProject[index])
    i = int(input("Select one from above list by the number or enter for new: ") or 0)
    if (i!=0):
        try:
            projectName = uniqueProject[i-1]
        except ValueError:
            print('Invalid project id.')
    else:
        projectName = createProject()
else:
    print('File not found')
    df = pd.DataFrame(columns=['Date', 'project', 'StartHour', 'End Hour', 
    'Work Hour', 'Total week', 'Description'])
    projectName = createProject()

if len(df['Total week']) == 0:
    totalHour = 0
else:
    totalHour = df['Total week'][len(df['Total week'])-1]

i = str(input('Start hour in formate "hh:mm": '))
try:
    stHour = datetime.datetime.strptime(i, '%H:%M')
except ValueError:
    print("Incorrect format")
stHour = stHour.replace(year=workDay.year, day=workDay.day, month=workDay.month)

i = str(input('End hour in formate "hh:mm": ') or datetime.datetime.strftime(toDay, '%H:%M'))
try:
    enHour = datetime.datetime.strptime(i, '%H:%M')
except ValueError:
    print("Incorrect format")
enHour = enHour.replace(year=workDay.year, day=workDay.day, month=workDay.month)

enHour = enHour - datetime.timedelta(minutes=enHour.minute % 15, seconds=enHour.second, 
                             microseconds=enHour.microsecond)
stHour = stHour - datetime.timedelta(minutes=stHour.minute % 15, seconds=stHour.second, 
                             microseconds=stHour.microsecond)
workHour = enHour - stHour

wHours, wMinutes, wSeconds = convert_timedelta(workHour)

totalHour = totalHour + workHour.total_seconds()/3600

desCription = str(input('Write a description: ') or 'Nan')

rowToAdd = {'Date': datetime.datetime.strftime(workDay, '%d-%m-%Y'), 'project': projectName, 
'StartHour': datetime.datetime.strftime(stHour, '%H:%M'), 'End Hour': datetime.datetime.strftime(enHour, '%H:%M'), 
'Work Hour':str(wHours) + ':' + str(wMinutes),  'Total week': totalHour, 'Description': desCription}

df = df.append(rowToAdd, ignore_index = True)

print(df)

df.to_csv(fileName, index='false')
print("File writen")