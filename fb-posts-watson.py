"""this code will read posts from facebook and calculate personality of that person;
provide your facebook access token ibm watson personality insights username and password"""
import facebook
import requests
import operator

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

def some_action(post):
    """ Here you might want to do something with each post. E.g. grab the
    post's message (post['message']) or the post's picture (post['picture']).
    In this implementation we just print the post's created time.
    """
    text = ""
    try:
		text+=post['story']
    except KeyError:
		a=1
    try:
        text+=post['message']
    except KeyError:
		a=2
    return text


# You'll need an access token here to do anything.  You can get a temporary one
# here: https://developers.facebook.com/tools/explorer/
access_token = 'facebook - developer - token here'

user = 'facebook user-id here'

graph = facebook.GraphAPI(access_token)
profile = graph.get_object(user)
posts = graph.get_connections(profile['id'], 'posts')
print(profile['name'])
# Wrap this block in a while loop so we can keep paginating requests until
# finished.
#print(posts)
text = ''
while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        for post in posts['data']:
            text+=some_action(post=post)
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break

from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

pi_username = 'watson personality insights app username here'
pi_password = 'waton personality insights app password here'

personality_insights = PersonalityInsights(username=pi_username, password=pi_password)
pi_result = personality_insights.profile(text)
p2 = flatten(pi_result)
#print(p2,type(p2))
sorted_result = sorted(p2.items(), key=operator.itemgetter(1),reverse=True)
for key,value in sorted_result[:10]:
	print key + "->" + str(value)
