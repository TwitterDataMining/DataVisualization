import pandas as pd
import csv
import sys
import pymongo
from models import UserData
from dataVisualization import mongodb



csv.field_size_limit(sys.maxsize)
COLORS =[
        "FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", "00FFFF", "000000",
        "800000", "008000", "000080", "808000", "800080", "008080", "808080",
        "C00000", "00C000", "0000C0", "C0C000", "C000C0", "00C0C0", "C0C0C0",
        "400000", "004000", "000040", "404000", "400040", "004040", "404040",
        "200000", "002000", "000020", "202000", "200020", "002020", "202020",
        "600000", "006000", "000060", "606000", "600060", "006060", "606060",
        "A00000", "00A000", "0000A0", "A0A000", "A000A0", "00A0A0", "A0A0A0",
        "E00000", "00E000", "0000E0", "E0E000", "E000E0", "00E0E0", "E0E0E0",
        ]

class ProcessData:

    def __init__(self):
        self.file_path = "/media/Store/Fall2017/dataVisualization/data/ThisIsUs_new_username.csv"
        self.topic_file = "//media/Store/Fall2017/dataVisualization/data/top_words.csv"
        self.topics, self.topic_dict = self.create_topic_dict()


        pass

    def create_topic_dict(self):
        topic_dict = {}
        topics = []
        for line in open(self.topic_file, 'r').readlines():
            topic, words = line.split(':')
            topics.append(topic)
            topic_dict[topic.strip()] = map(str.strip, words.split())

        return topics, topic_dict

    def create_data(self):
        with open(self.file_path, "rb") as f:
            reader = csv.reader(f)
            for user,text in reader:
                u_data = UserData(user_id= user, tweets= text)
                u_data.save()


    def get_users(self, limit=10, offset=0):
        coll = mongodb.db.UserData
        starting_id = coll.find().sort('_id', pymongo.ASCENDING)
        last_id = starting_id[offset]['_id']

        users = coll.find(
            {'_id': {'$gte' : last_id}},
            {'user_id' : 1}

        ).limit(limit=limit)
        return users

    def get_user_tweets(self, id):
        coll = mongodb.db.UserData
        tweets = coll.find(
            {'user_id': str(id)},
            {'tweets': 1}
        )

        return tweets

    def get_topics(self):
        return self.topics

    def get_colors(self):

        return ['#'+ color for color in COLORS]

    def get_top_words(self):
        return self.topic_dict





