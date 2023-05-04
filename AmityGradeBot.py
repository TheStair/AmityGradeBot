# AmityGradeBot.py
# Version 5/3/2023
# Author TheStair
# ESV proverbs API request from the website
# Do not publicly share API Keys
# Do not add users without consent as it violates FERPA

import discord
import requests
import re
import random

intents = discord.Intents().all()
client = discord.Client()
msg = ''

# Canvas API URL
canvasURL = "https://canvas.instructure.com"

# Canvas API key dictionary
keys = {'User 1 Canvas API key': ['User 1', 'School/University'],
        'User 2 Key': ['User 2 Name', 'School/University'],

        }
# Course Number and Name Dictionary
courses = {999999: 'Public Speaking', 999999: 'Software Construction', 99999999: 'World Literature 1',
           }


def invoke(url, location, token, suffix=""):
    u = url + location + "?access_token=" + token
    print('invoking', u)
    data = requests.get(u).json()
    return data

# Fetches Grade data for each dictionary value
for key in keys.keys():
    avg = [0, 0]
    user = keys[key][0]
    prefix = keys[key][1]
    msg += '**' + user + "'s Grades**\n"
    url = 'https://' + prefix + '.instructure.com/api/v1/'
    data = invoke(url, 'users/self/enrollments', key)
    for course in data:
        if 'current_score' in course['grades']:
            score = course['grades']['current_score']
            id = course['course_id']
            if id in courses:
                msg += courses[id] + ": *" + str(score) + "*\n"
                if score != None:  # average calculation
                    avg[0] += score
                    avg[1] += 1
            else:
                print('cannot find course in dict:', course['course_id'], user, data)
    msg += '*Average: ' + str(int(avg[0] / avg[1])) + '*\n\n'

bibleAPI_KEY = 'ESV key'
bibleAPI_URL = 'https://api.esv.org/v3/passage/text/'

#From ESV Website
CHAPTER_LENGTHS = [
    33, 22, 35, 27, 23, 35, 27, 36, 18, 32,
    31, 28, 25, 35, 33, 33, 28, 24, 29, 30,
    31, 29, 35, 34, 28, 28, 27, 28, 27, 33,
    31
]

ROMANS_CHAPTER_LENGTHS = [
    32, 29, 31, 25, 21, 23, 25, 39, 33, 21,
    36, 21, 14, 23, 33, 27]

# From ESV Website
def get_passage():
    chapter = random.randrange(1, len(CHAPTER_LENGTHS))
    verse = random.randint(1, CHAPTER_LENGTHS[chapter])

    return 'Proverbs %s:%s' % (chapter, verse)


def get_romans_passage():
    chapter = random.randrange(1, len(ROMANS_CHAPTER_LENGTHS))
    verse = random.randint(1, ROMANS_CHAPTER_LENGTHS[chapter])

    return 'Romans %s:%s' % (chapter, verse)

# Define requests, from ESV Website
def get_esv_text(passage):
    params = {
        'q': passage,
        'indent-poetry': False,
        'include-headings': False,
        'include-footnotes': False,
        'include-verse-numbers': False,
        'include-short-copyright': False,
        'include-passage-references': False
    }

    headers = {
        'Authorization': 'Token %s' % bibleAPI_KEY
    }


    bibleData = requests.get(bibleAPI_URL, params=params, headers=headers).json()

    text = re.sub('\s+', ' ', bibleData['passages'][0]).strip()

    return '%s – %s' % (text, bibleData['canonical'])

# From ESV Website
def render_esv_text(data):
    text = re.sub('\s+', ' ', data['passages'][0]).strip()

    return '%s – %s' % (text, data['canonical'])


if __name__ == '__main__':
    msg += '**Proverb of the Day**\n' + get_esv_text(get_passage())
    msg += '\n\n**Romans Verse of the Day**\n' + get_esv_text(get_romans_passage())

# Sends the variable "msg" on connection to Discord
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == "ServerName":
            break
    channel = client.get_channel(Channel ID)
    await channel.send(msg)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


client.run("Discord Key")
