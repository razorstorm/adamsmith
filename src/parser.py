import time
from dateutil.parser import parse
import json
from Queue import PriorityQueue

from lxml import etree

NAME_BLACK_LIST = {'facebook user'}


class Message(object):
    def __init__(self, time_stamp, friend_index, friend_display_name, message=None):
        self.time_stamp = time_stamp
        self.friend_index = friend_index
        self.friend_name = friend_display_name.lower()
        self.friend_display_name = friend_display_name
        self.message = message

    def __cmp__(self, other):
        return self.time_stamp - other.time_stamp


def process_messages():
    data = open('fb/html/messages.htm', 'r').read()
    doc = etree.HTML(data)

    elements = doc.xpath("//body/div[@class='contents']")
    element = elements[0]

    user_name = element.getchildren()[0].text
    divs = element.getchildren()[1:]

    friends = {}
    events = PriorityQueue()

    i = 0
    for div in divs:
        print 'Processing', i, 'out of', len(divs)
        i += 1
        for thread in div.getchildren():
            participants_label = thread.text
            if not participants_label:
                continue
            participants = participants_label.split(',')
            if len(participants) != 2:
                # For now let's only worry about 1 on 1 chats
                continue
            friend_name = [name for name in participants if name.lower() != user_name][0]
            if friend_name.lower() in NAME_BLACK_LIST:
                continue
            if friend_name.lower() not in friends:
                friends[friend_name.lower()] = {
                    'display_name': friend_name,
                    'chats': PriorityQueue()
                }
            thread_children = thread.getchildren()
            meta = True
            curr_time_stamp = None
            curr_friend_index = None  # 0 is you, 1 is the friend

            for child in thread_children:
                if meta:
                    if len(child.getchildren()) < 1:
                        continue
                    name_divs = child.xpath('div/span[@class="user"]')
                    if len(name_divs) != 1:
                        continue
                    name = name_divs[0].text
                    if not name:
                        continue
                    if name.lower() == user_name:
                        curr_friend_index = 0
                    else:
                        curr_friend_index = 1

                    time_divs = child.xpath('div/span[@class="meta"]')
                    if len(time_divs) != 1:
                        continue
                    time_str = time_divs[0].text
                    dt = parse(time_str)
                    curr_time_stamp = time.mktime(dt.timetuple())
                else:
                    # We don't do any analysis on the actual message yet, maybe v2
                    message = child.text
                    if message:
                        message_event = Message(curr_time_stamp, curr_friend_index, friend_name, message)
                        events.put(message_event)
                        friends[friend_name.lower()]['chats'].put(message_event)

                meta = not meta

    formatted_events = []

    prev = None
    while not events.empty():
        m = events.get()
        t = m.time_stamp
        if prev:
            if t < prev:
                print prev, t, 'BAD!'
        prev = t
        formatted_events.append(m.__dict__)

    events_json = json.dumps(formatted_events)

    with open('output/messages.json', 'w') as fh:
        fh.write(events_json)


process_messages()
