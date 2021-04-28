#!/usr/bin/env python3
import requests
import json
import datetime
import time

URLPR = "https://api.github.com/repos/grafana/grafana/pulls"
URLORG = "https://api.github.com/orgs/grafana/members"

userfinished = False
userindex = 0
users = set()

while(not userfinished):
  time.sleep(5) 
  PARAMS = {'per_page': 100, 'page': userindex}
  userindex = userindex + 1
  resp = requests.get(url = URLORG, params = PARAMS)
  resultusers= resp.json()
  if len(resultusers) == 0:
    userfinished = True 
  for resultuser in resultusers:
    if "login" in resultuser:
      users.add(resultuser["login"])
      print(resultuser["login"])


prfinished = False
index = 0
count = 0
starttime = datetime.datetime.strptime("2020-03-28T00:00:00Z", '%Y-%m-%dT%H:%M:%SZ')
endtime = datetime.datetime.strptime("2020-06-02T23:59:59Z", '%Y-%m-%dT%H:%M:%SZ')
while(not prfinished):
  time.sleep(5) 
  PARAMS = {'per_page': 100, 'page': index, 'state': 'all'}
  index = index + 1
  resp = requests.get(url = URLPR, params = PARAMS)
  pullrequests = resp.json()
  print("the count is: ", count)
  if len(pullrequests) < 100:
    prfinished = True
  print("the current date is: ", pullrequests[0]["created_at"])
  theDate = datetime.datetime.strptime(pullrequests[0]["created_at"], '%Y-%m-%dT%H:%M:%SZ')
  if theDate < starttime:
    prfinished = True
    break
  for pullrequest in pullrequests:
    if "user" in pullrequest and ("login" in pullrequest["user"]):
      if (pullrequest["user"]["login"] not in users):
        atime = datetime.datetime.strptime(pullrequest["created_at"], '%Y-%m-%dT%H:%M:%SZ')
        if atime > starttime and atime < endtime:
          count = count + 1

print("the total count is: ", count)
