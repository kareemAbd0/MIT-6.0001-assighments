# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
     def __init__(self,guid,title,description,link,pubdate):
         self.Guid = guid
         self.Title = title
         self.Description = description
         self.Link = link
         self.Pubdate = pubdate
     def get_guid(self):
         return self.Guid

     def get_title(self):
         return self.Title

     def get_description(self):
         return self.Description

     def get_link(self):
         return self.Link

     def get_pubdate(self):
         return self.Pubdate



#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """

        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS
class PhraseTriggers (Trigger):
    def __init__(self, phrase):
        self.Phrase = phrase


    def evaluate(self, story):
        flag = True
        for i in range (len (self.Phrase.lower())):
            if self.Phrase.lower ()[i] in string.punctuation:
                return False
        if '' in self.Phrase.split(" "):
            return False
        else:
            flag = True
            splited_phrase = self.Phrase.lower ().split ()
            splited_story = re.findall (r"[\w']+", story.lower ())
            if flag == True:
                if set (splited_phrase).issubset (set (splited_story)):
                    place_instory = splited_story.index (splited_phrase[0])
                    for x in range (len (splited_phrase)):
                        if splited_story.index (splited_phrase[0]) > splited_story.index (splited_phrase[x]):
                            return False
                        if splited_phrase[x] == splited_story[place_instory + x]:
                            flag = True
                        else:
                            flag = False
                else:
                    flag = False
            return flag


# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.Phrase = phrase.lower()
    def is_phrase_in(self,story):
        # flag = True
        # for i in range (len (self.Phrase.lower ())):
        #     if self.Phrase.lower ()[i] in string.punctuation:
        #         return False
        # if '' in self.Phrase.split (" "):
        #     return False
        # else:
        flag = True
        splited_phrase = self.Phrase.lower ().split ()
        splited_story =  re.findall(r"[\w']+", story.lower())
        if flag == True:
            if set (splited_phrase).issubset (set (splited_story)) :
                place_instory = splited_story.index (splited_phrase[0])
                for x in range (len (splited_phrase)):
                    if splited_story.index(splited_phrase[0])>splited_story.index(splited_phrase[x]):
                        return False
                    if splited_phrase[x] == splited_story[place_instory + x] :
                        flag = True
                    else:
                        flag = False
            else:
                flag = False
        return flag







# Problem 3

# TODO: TitleTrigger

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.Phrase = phrase.lower()

    def evaluate(self,story):

       return self.is_phrase_in(story.Title)



# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.Phrase = phrase.lower()

    def evaluate(self,story):

       return self.is_phrase_in(story.Description)


# TIME TRIGGERS




# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self,time):
        self.Time = (datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone("EST")))
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self,time):
       TimeTrigger.__init__(self,time)
    def evaluate(self,story):
        return self.Time> (story.Pubdate).replace(tzinfo=pytz.timezone("EST"))

class AfterTrigger(TimeTrigger):
    def __init__(self,time):
       TimeTrigger.__init__(self,time)
    def evaluate(self,story):
        return self.Time < (story.Pubdate).replace(tzinfo=pytz.timezone("EST"))

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self,noto):
        self.Not = noto
    def evaluate(self, story):
        return not self.Not.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self,and1,and2):
        self.And1 = and1
        self.And2 = and2

    def evaluate(self, story):
        return  self.And1.evaluate(story) and self.And2.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self,or1,or2):
        self.Or1 = or1
        self.Or2 = or2

    def evaluate(self, story):
        return  self.Or1.evaluate(story) or self.Or2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """

    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    z = 0
    final_stories = []
    for i in range(len(stories)):

         for x in range(len(triggerlist)):

            if triggerlist[x].evaluate((stories[i])):
                final_stories.append(stories[i])


    return final_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    decttr = {}
    triggers = {}
    trigger_list = []
    dect_for_classes = {'TITLE':TitleTrigger,'DESCRIPTION':DescriptionTrigger, 'AFTER':AfterTrigger,'BEFORE':BeforeTrigger,'AND':AndTrigger,'OR':OrTrigger,'NOT':NotTrigger}

    for xx in range(len(lines)):
        splited_def = lines[xx].split(",")
        decttr.update({splited_def[0]:splited_def[1]})



    counter = 0

    for nn in decttr.keys ():
        new_splited_def = lines[counter].split (",")

        if decttr[nn] == 'TITLE' or decttr[nn] == 'DESCRIPTION' or decttr[nn] == 'AFTER' or decttr[nn] == 'Before' or decttr[nn] == 'NOT':

             triggers.update({new_splited_def[0]:dect_for_classes[decttr[nn]](new_splited_def[2])})

        elif decttr[nn] == 'AND':
            triggers.update ({new_splited_def[0]: dect_for_classes[decttr[nn]] (triggers[new_splited_def[2]],triggers[new_splited_def[3]])})
        elif decttr[nn] == 'OR':
            triggers.update ({new_splited_def[0]: dect_for_classes[decttr[nn]] (triggers[new_splited_def[2]],triggers[new_splited_def[3]])})

        elif nn == 'ADD':

          for k in new_splited_def[1:] :
                trigger_list += [triggers[k]]



        counter += 1
    print (triggers)
    print (trigger_list)

    return trigger_list


    # for now, print it so you see what it contains!



SLEEPTIME = 5 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Biden")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line

        triggerlist = read_trigger_config('triggers.txt')
        print (triggerlist)

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

