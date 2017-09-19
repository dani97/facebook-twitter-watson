import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

def analyze(handle):
  statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
  text= ""
  for status in statuses:
    if status.lang=='en':
      text += status.text.encode('utf-8')
  personality_insights = PersonalityInsights(username=pi_username, password=pi_password)
  pi_result = personality_insights.profile(text)
  return pi_result

def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data
  
def compare(dict1, dict2):
	print(dict1==dict2)
	compared_data = {}
	for keys in dict1:
		print keys
		if dict1[keys] != dict2[keys]:
			compared_data[keys]=abs(dict1[keys] - dict2[keys])
  	return compared_data


twitter_consumer_key = 'twitter - consumer - key here'
twitter_consumer_secret = 'twitter - consumer - secret here'
twitter_access_token = 'twitter access token here'
twitter_access_secret = 'twitter access secret here'

twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)

handle = '@coltondixon'
statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)
text= ""
for status in statuses:
  if status.lang=='en':
    text += status.text.encode('utf-8')

#The IBM Bluemix credentials for Personality Insights!
pi_username = 'personality insights username'
pi_password = 'personality insights password'
