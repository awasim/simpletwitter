import twitter, time, sys, os
from optparse import OptionParser
from threading import Thread, Lock
import tornado.ioloop
import tornado.web
from analyze import *
from convert import *
from savetwts import *

tweetstore = []
rtstore = []
queue = [] 
lock = Lock()
tcount = 0

class tweettray(Thread):
    tweets = []
    tweet_count = 0
    api = twitter.Api() 

    slist = []
    l_list = []
    ulist = []

    consumerkey = os.environ['CONSUMERKEY']
    consumersecret = os.environ['CONSUMERSECRET']
    accesstokenkey = os.environ['ACCESSTOKENKEY']
    accesstokensecret = os.environ['ACCESSTOKENSECRET']

    def append(self, item):
        lock.acquire()
        queue.append(item)
        self.tweet_count = self.tweet_count + 1
        lock.release()

    def numtweets(self):
        return self.tweet_count
    
    def num_lists(self):
        return len(self.l_list)

    def num_u_list(self):
        return len(self.ulist)

    def login(self):
        self.api = twitter.Api(consumer_key=self.consumerkey, consumer_secret=self.consumersecret, access_token_key=self.accesstokenkey, access_token_secret=self.accesstokensecret)
    
        print self.api.VerifyCredentials()

    def getHome(self):
        stime = 360 
    
        while 1:
            for i in self.api.GetHomeTimeline():
                print "User: " + i.user.GetName()
                #print "User Id: " + str(i['user']['id'])
                print "Text: " + i.text
            time.sleep(stime)

    def getLists(self, username):
        listids = self.api.GetLists(screen_name=username)
        for listi in listids:
            self.l_list.append((listi.GetId(), listi.GetFull_name()))
            #print listi.GetId()
            #print listi.GetFull_name()

    def getFriendIDs(self, username):
        print "Getting Friend IDs"
        self.ulist = self.api.GetFriendIDs(screen_name=username)
        print "Processing Friends IDs"
        #print self.ulist
        count = 0
        for num in self.ulist:
            self.slist.append(str(num))
            count = count + 1
        print "Added : " + str(count)

    def getListMembers(self, listid, text):
        print "Getting List members for list: %s" %(text)
        listm = self.api.GetListMembers(list_id=listid, slug=text)
        for listmi in listm:
            #print "Adding: " + str(listmi.GetId())
            self.slist.append(str(listmi.GetId()))
        return listm

    def streemProcess(self):
        print "Processing Stream start: "
        if (len(self.slist) == 0):
            print "No one to subscribe to"
            return 

        for i in self.api.GetStreamFilter(follow=self.slist):    
            if i.has_key('text'):
                self.append(i)

    def run(self):
        print "Starting producer thread"
        global queue
        global tweetstore
        self.streemProcess()

    def subscribeU(self, username):
        tw = tweettray()
        self.login()
        self.getFriendIDs(username)
        f = open('userlist.txt', 'w')
        f.write("Screen Name: %s\n" %(username))
        for i in self.ulist:
            f.write(str(i) + '\n')
        #self.streemProcess()
    
    def subscribeUnL(self, username):
        tw = tweettray()
        self.login()
        self.getFriendIDs(username)
        f = open('userlist.txt', 'w')
        f.write("Screen Name: %s\n" %(username))
        for i in self.ulist:
            f.write(str(i) + '\n')
        self.getLists(username)
        for item in self.l_list:
            self.getListMembers(item[0], item[1])
        #self.streemProcess()   

    def subscribeL(self, username):
        tw = tweettray()
        self.login()
        self.getLists(username)
        for item in self.l_list:
            self.getListMembers(item[0], item[1])
        #self.streemProcess()
    
class pTweets(Thread):
    def run(self):
        print "Starting consumer thread"
        a = analyze()
        global queue
        global tweetstore
        global rtstore
        block = ["insafediver", "MakeUseOf", "healthyworld24", "ISSAboveYou", "JoeGumby1", "Gumbletech"]
        blockterms = ["invest", "market", "nasa"]
        prefuser = ["davewiner", "scobleizer"]
        while True:
            lock.acquire()
            if not queue:
                #print "Nothing in queue: printer will try again"
                pass
            else:
                num = queue.pop()
                screen_name = ""
                text = ""
                if num.has_key('user'):
                    if num['user'].has_key('screen_name'):
                        screen_name = num['user']['screen_name'].encode('ascii', 'ignore')
                if num.has_key('text'):
                    text = num['text'].encode('ascii', 'ignore')
                if screen_name in prefuser:
#                    print screen_name, text
                    tweetstore.append(num)
                elif text.startswith('RT'):
                    #rtstore.append(num)
                    pass
                elif (text.find('http') != -1):
                    if (screen_name not in block):
                        blck = True
                        for term in blockterms:
                            if text.lower().find(term) > 0:
                                blck = False

                        if (blck) and not (a.cleanstr(text).isupper()):
#                            print screen_name, text
                            tweetstore.append(num)
            lock.release()

class stats(tornado.web.RequestHandler):
    def get(self):
        header = """
        <html>
        <head>
        <title>Twitter Client</Title>
        <meta http-equiv="refresh" content="60" />
        </head>
        <body style="background:lightgray">
        """
        self.write(header)
        self.write("Tweetstore: " + str(len(tweetstore)))
        self.write("<br/>")
        self.write("Queue: " + str(len(queue)))
        self.write("<br/>")
        self.write("RTStore: " + str(len(rtstore)))
        self.write("<br/>")        
        self.write("</body></html>")

class RTHandler(tornado.web.RequestHandler):
    def get(self):
        a = analyze()
        header = """
        <html>
        <head>
        <title>Twitter Client</Title>
        <meta http-equiv="refresh" content="60" />
        </head>
        <body style="background:lightgray">
        """
        self.write(header)
        for tweet in rtstore:
            if tweet.has_key('text'):
                text = tweet['text'].encode('ascii', 'ignore')
                text = convertLinks(text)
            if tweet.has_key('screen_name'):
                screen_name = "@" + tweet['screen_name'].encode('ascii', 'ignore') + ": "
            elif tweet.has_key('user'):
                if tweet['user'].has_key('screen_name'):
                    screen_name = "@" + tweet['user']['screen_name'].encode('ascii', 'ignore') + ": "
            self.write("<p>")
            self.write(screen_name)
            self.write(text)
            self.write("</p>")
            self.write("</body></html>")
        
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        a = analyze()
        header = """
        <html>
        <head>
        <title>Twitter Client</Title>
        <meta http-equiv="refresh" content="60" />
        </head>
        <body style="background:lightgray">
        """
        self.write(header)
        for tweet in tweetstore:
            screen_name = ""
            text = ""
            if a.cleanstr(tweet['text']) == '':
                #print "Skipping: " + tweet['text']
                pass
            else:
                if tweet.has_key('text'):
                    text = tweet['text'].encode('ascii', 'ignore')
                    text = convertLinks(text)
                if tweet.has_key('screen_name'):
                    screen_name = "@" + tweet['screen_name'].encode('ascii', 'ignore') + ": "
                elif tweet.has_key('user'):
                    if tweet['user'].has_key('screen_name'):
                        screen_name = "@" + tweet['user']['screen_name'].encode('ascii', 'ignore') + ": "
                    if a.finduser(screen_name):
                        self.write("<p style='color: green'>")
                    elif a.findword(text) or a.findterm(text):
                        self.write("<p style='color: green'>")
                        txt = a.appendword(text)
                        if txt != "":
                            text = txt
                    else:
                        self.write("<p style='color: red'>")
                    self.write(screen_name)
                    self.write(text)
                    self.write("</p>")
        self.write("</body></html>")

class GreenHandler(tornado.web.RequestHandler):
    def get(self):
        a = analyze()
        header = """
        <html>
        <head>
        <title>Green Tweets</Title>
        </head>
        <body style="background:lightgray">
        """
        self.write(header)
        for tweet in tweetstore:
            screen_name = ""
            text = ""
            if a.cleanstr(tweet['text']) == '':
                #print "Skipping: " + tweet['text']
                pass
            else:
                if tweet.has_key('text'):
                    text = tweet['text'].encode('ascii', 'ignore')
                    text = convertLinks(text)
                if tweet.has_key('screen_name'):
                    screen_name = "@" + tweet['screen_name'].encode('ascii', 'ignore') + ": "
                elif tweet.has_key('user'):
                    if tweet['user'].has_key('screen_name'):
                        screen_name = "@" + tweet['user']['screen_name'].encode('ascii', 'ignore') + ": "
                    if a.finduser(screen_name) or (a.findword(text)) or (a.findterm(text)):
                        img_url = ""
                        if tweet['user'].has_key('profile_image_url'):
                            img_url = tweet['user']['profile_image_url']
                        self.write("<p style='background:white; color: green'>")
                        if img_url != "":
                            self.write("<img src='" + img_url + "' style='float:left'>")
                        self.write("<a href='http://twitter.com/" + screen_name[1:-2] + "' target='_blank'>" + screen_name + "</a>")
                        self.write("<br/>")
                        self.write(text)
                        if tweet.has_key('created_at'):
                            self.write("<br/>" + tweet['created_at'].encode('ascii', 'ignore'))
                        self.write("</p>")
        self.write("</body></html>")
                    
class RedHandler(tornado.web.RequestHandler):
    def get(self):
        a = analyze()
        header = """
        <html>
        <head>
        <title>Red Tweets</Title>
        </head>
        <body style="background:lightgray">
        """
        self.write(header)
        for tweet in tweetstore:
            screen_name = ""
            text = ""
            if a.cleanstr(tweet['text']) == '':
                #print "Skipping: " + tweet['text']
                pass
            else:
                if tweet.has_key('text'):
                    text = tweet['text'].encode('ascii', 'ignore')
                    text = convertLinks(text)
                if tweet.has_key('screen_name'):
                    screen_name = "@" + tweet['screen_name'].encode('ascii', 'ignore') + ": "
                elif tweet.has_key('user'):
                    if tweet['user'].has_key('screen_name'):
                        screen_name = "@" + tweet['user']['screen_name'].encode('ascii', 'ignore') + ": "
                    if a.finduser(screen_name) or (a.findword(text)) or a.findterm(text):
                        pass
                    else:
                        img_url = ""
                        if tweet['user'].has_key('profile_image_url'):
                            img_url = tweet['user']['profile_image_url']
                        self.write("<p style='background:white; color: red'>")
                        if img_url != "":
                            self.write("<img src='" + img_url + "' style='float:left'>")
                        self.write("<a href='http://twitter.com/" + screen_name[1:-2] + "' target='_blank'>" + screen_name + "</a>")
                        self.write("<br/>")
                        self.write(text)
                        self.write("</p>")
        self.write("</body></html>")        

class GreenJson(tornado.web.RequestHandler):
    def get(self):
        a = analyze()
        header = """
        <html>
        <head>
        <title>Green Tweets</Title>
        """
        self.write(header)
        for tweet in tweetstore:
            screen_name = ""
            text = ""
            if a.cleanstr(tweet['text']) == '':
                #print "Skipping: " + tweet['text']
                pass
            else:
                if tweet.has_key('text'):
                    text = tweet['text'].encode('ascii', 'ignore')
                    text = convertLinks(text)
                if tweet.has_key('screen_name'):
                    screen_name = "@" + tweet['screen_name'].encode('ascii', 'ignore') + ": "
                elif tweet.has_key('user'):
                    if tweet['user'].has_key('screen_name'):
                        screen_name = "@" + tweet['user']['screen_name'].encode('ascii', 'ignore') + ": "
                    if a.finduser(screen_name) or (a.findword(text)) or a.findterm(text):
                        self.write(tweet)
                        self.write("\n")
        finhdr = """
        </head>
        <body style="background:lightgray">
        """
        self.write("</body></html>")

        
def startwebserver(port):
    print "Starting Webserver on port: " + port
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/green", GreenHandler),
        (r"/red", RedHandler),
        (r"/gjson", GreenJson),
        (r"/stats", stats),
        (r"/rt", RTHandler),
        ])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    try:
        parser = OptionParser()
        parser.add_option("-u", "--username", dest="user", help=" a username is needed", default='awasim')
        parser.add_option("-a", "--all", dest="all", help=" Subscribe to user and lists", action="store_true")
        parser.add_option("-l", "--list", dest="list", help=" Subcribe only to user lists", action="store_true")
        parser.add_option("-p", "--port", dest="port", help=" Port to run webserver on", default="8888")
        tweetstore = loadtwts()
        tw = tweettray()
        pT = pTweets()
#        pT2 = pTweets()
#        pT3 = pTweets()
        (options, args) = parser.parse_args()
        if (options.all): 
            tw.subscribeUnL(options.user)
        elif (options.list):
            tw.subscribeL(options.user)
        else:
            tw.subscribeU(options.user)
        tw.daemon = True
        pT.daemon = True
#        pT2.daemon = True
#        pT3.daemon = True
        tw.start()
        pT.start()
#        pT2.start()
#        pT3.start()
        if (options.port):
            startwebserver(options.port)
        else:
            startwebserver(8888)
    except KeyboardInterrupt:
        print "Key Pressed"
        dumptwts(tweetstore)
        sys.exit(0)
