from Trie import TrieNode
import pickle
import os
import sys
from random import choice
import string

maxrec = 1_000_000_000
datamap = "./data/search_video"
jsonfile = "./data/video-list.json"

sys.setrecursionlimit(maxrec)
IGNORE = [
    "whose",
    "when",
    "whom",
    "whould",
    "should",
    "could",
    "what",
    "wasnt",
    "ahn",
]


def to_time(string):
    part = string.split(".")
    bigger = part[0]
    lower = part[1]
    number = int(lower)
    parts = bigger.split(":")
    partial = 1000
    while parts:
        current = parts.pop()
        number += int(current) * partial
        partial *= 60
    return number


def extract_text(text):
    answer = []
    lines = text.split("\n")
    last_time = 0
    for line in lines:
        line = line.replace("</c>", "")
        part = line.split("<c> ")
        if len(part) > 1:
            for subdiv in part:
                subdiv = subdiv.replace(">", "")
                subpart = subdiv.split("<")
                word = subpart[0]

                if len(subpart) == 2:
                    time = to_time(subpart[1])
                    last_time = time

                else:
                    time = last_time + 300

                if len(word) > 3 and word not in IGNORE:
                    answer.append({"text": word.lower(), "time": time})
    return answer


class VideoDetails:
    def __init__(self, channel, uploaddate, duration, viewcount):
        self.channel = channel
        self.uploaddate = uploaddate
        self.duration = duration
        self.views = viewcount


class Answer:
    def __init__(self, video, time):
        self.video = video
        self.time = time

class BaseData:
    def __init__(self):
        self.origins = []
        self.start = self.get_data()
        self.pointer = self.start
        self.videolist = self.video_list()
        self.video = 0

    def video_details(self, video):
        for channel in self.videolist:
            if video in self.videolist[channel]:
                print(self.videolist[channel][video])

                return self.videolist[channel][video]

        return {}

    def video_list(self):
        if os.path.isfile(jsonfile):
            try:
                with open(jsonfile, "rb") as file:
                    vlist = pickle.load(file)

            except Exception as e:
                print(e)

        else:
            vlist = {}
        return vlist

    def get_data(self):
        if os.path.isfile(f"{datamap}.jls"):
            try:
                with open(f"{datamap}.jls", "rb") as file:
                    trie = pickle.load(file)

            except Exception as e:
                print(e)

        else:
            trie = TrieNode()
        return trie

    def save_data(self):
        print(f"::::    {self.video}    ::::")
        self.video += 1
        try:
            if self.video % 25 == 0:
                with open(f"{datamap}.jls", "wb") as file:
                    pickle.dump(self.start, file)
                print("save data")

        except Exception as e:
            print(e)

    def save_list(self):
        try:
            print("save list")
            with open(jsonfile, "wb") as file:
                pickle.dump(self.videolist, file)

        except Exception as e:
            print(e)

    def add_text(self, text, url, channel, uploaddate, duration, viewcount):
        details = VideoDetails(channel, uploaddate, duration, viewcount)
        if channel not in self.origins:
            self.origins.append(channel)

        if channel not in self.videolist:
            self.videolist[channel] = {}

        else:
            if url not in self.videolist[channel]:
                try:
                    self.videolist[channel][url] = details
                    self.save_list()
                except Exception as e:
                    print("ERROR SAVING LIST AT ADD_TEXT")
                    print(e)

        words = reversed(extract_text(text))
        try:
            for word in words:
                self.pointer = self.start
                lowerword = word["text"]
                lowerword = lowerword.replace('"', "")
                lowerword = lowerword.replace("'", "")
                lowerword = lowerword.replace("-", "")
                for char in lowerword:
                    if char.isalpha():
                        if char in self.pointer.children:
                            self.pointer = self.pointer.children[char]

                        else:
                            self.pointer.children[char] = TrieNode()
                            self.pointer = self.pointer.children[char]
                            self.pointer.char = char

                answer = Answer(url, int(word["time"]))
                self.pointer.answer.append(answer)
                self.pointer.word = word["text"]
            self.save_data()

        except Exception as e:
            print("EXCEPTION AT ADDING WORD TO TRIE")
            print(e)

    def find_word(self, word):
        if len(word) > 3 and word not in IGNORE:
            word = word.replace('"', "")
            word = word.replace("'", "")
            word = word.lower()
            self.pointer = self.start

            for char in word:                    
                if char in self.pointer.children:
                    self.pointer = self.pointer.children[char]

                else:
                    return []
            return self.pointer.answer

        else:
            return []

    def add(self, answer, word, second):
        for element in second:
            video = element.video
            if video in answer:
                if word in answer[video]:
                    if element.time not in answer[video][word]:
                        answer[video][word].append(element.time)

                else:
                    answer[video][word] = [element.time]

            else:
                answer[video] = {}
                answer[video][word] = [element.time]
        return answer

    def subtract(self, answer, second):
        for element in second:
            video = element.video
            if video in answer:
                del answer[video]
        return answer

    def match(self, answer, word, second):
        new_answer = {}
        for element in second:
            video = element.video
            if video in answer:
                new_answer[video] = answer[video]
                if word in answer[video]:
                    if element.time not in answer[video][word]:
                        new_answer[video][word].append(element.time)

                else:
                    new_answer[video][word] = [element.time]
        return new_answer
    
    # def find_sentence(self, query):
    #     words = query.split(" ")
    #     listdict = {}
    #     size = len(words)
    #     for word in words:
    #         answers = self.find_word(word)
    #         if not first:
    #             first = answers
    #         for answer in answers:
    #             listdict[answer.code] = answer
    
    #     answers = []
    #     for answer in first:
    #         current = answer
    #         count = 1
    #         while current in listdict:
    #             current = listdict[current]
    #             count += 1
    #         if count == size:
    #             answers.append(answer)

    #     print(answers)

    #     return answers

    def search(self, query):
        self.pointer = self.start
        answer = {}
        # if '"' in query:
        #     part = query.split('"')
        #     answer = self.add(answer, part[1], self.find_sentence(part[1]))
            
        #     query = part[0]
        #     if len(part) > 2:
        #         query = f"{query}{part[2]}"
            
        #     print("query")
        #     print(query)

        words = query.split(" ")
        for index in range(len(words)):
            word = words[index]
            if len(word) > 3:
                if index == 0:
                    part = self.find_word(word)
                    self.add(answer, word, part)

                else:
                    if word[0] == "-":
                        word = word[1:]
                        part = self.find_word(word)
                        answer = self.subtract(answer, part)

                    elif word[0] == "&":
                        word = word[1:]
                        part = self.find_word(word)
                        answer = self.add(answer, word, part)

                    else:
                        part = self.find_word(word)
                        answer = self.match(answer, word, part)
        return answer
