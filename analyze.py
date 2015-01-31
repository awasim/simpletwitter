import re, string

class analyze:
    user = ["davewiner", "scobleizer", "techcrunch", "lifehacker", "tutsplus", "phoronix", "newsycbot", "lobsternews", "r_netsec", "io9", "javascriptdaily", "techmeme", "wiredfeed"]
    words = ["linux", "kernel", "geek", "java", "javascript", "python", "c++", "nasa", "mozilla", "facebook", "google", "microsoft", "windows", "win10", "astronomy", "science", "touchscreen", "chromebook", "pfsense", "openbsd", "freebsd", "skype", "whatsapp", "space", "sci-fi", "scifi", "starship", "node.js", "nodejs", "apple", "tablet","wordpress", "script", "api", "data", "servers", "protocols", "ecmascript", "webgl", "nvidia", "chromium", "emberjs", "jquery", "angularjs", "perl", "ruby", "unix", "regex", "macbook", "yosemite", "typeface", "interface", "fedora", "redhat", "debian", "ubuntu", "archlinux", "gentoo", "mac os x", "imac", "shell", "programming", "curiosity", "source control", "revision control", "git", "curl", "wget", "algorithm", "1080p", "webdev", "startups", "lisp", "erlang", "haskell", "monad", "closure", "clojure", "internet", "firefox", "safari", "opera", "scientist", "laptop", "textanalytics", "textual", "codec", "asteriod", "spyware", "antivirus", "warez", "adware", "comet", "twitter", "technology", "drone", "universe", "planet", "reorg", "layoff", "nosql", "database", "mysql", "mariadb", "lambda", "scalabililty", "mongodb", "driver", "bash", "tcsh", "realtime", "postgres", "UI",  "c#", "infosec", "starships", "astronaut", "html5", "css", "ember", "ember.js", "backbone", "backbone.js", "meteor", "meteor.js", "opensource", "debugging", "io.js", "iojs", "algorithmic", "svg", "developer", "dell", "ios", "github", "couchdb", "animation", "lego", "safari", "firefox"]
    terms = ["star trek", "star wars", "design tool", "time dilation", "data compression", "text analytics", "desktop computers", "web performance", "computer science", "web development", "data science", "to develop", "job queue", "data streams", "transaction processing", "request prioritization", "mars rover", "joss whedon", "dev tools", "ip address", "ip addresses", "quantum computing", "intelligence tools"]

    def finduser(self, text):
        if text[1:-2].lower() in self.user:
            return True
        else:
            return False

    def findword(self, text):
        for word in self.words:
            wordlist = self.removepunc(text.lower()).split(" ")
            for aword in wordlist:
                if aword.find("#") > -1:
                    wordlist.append(aword.replace("#", ""))
            if word in wordlist:
                return True
        return False

    def findterm(self, text):
        for word in self.terms:
            if text.lower().find(word) > 0:
                return True

    def appendword(self, text):
        for word in self.words:
            if text.lower().find(word) > 0:
               return text + " -- " + word
        for word in self.terms:
            if text.lower().find(word) > 0:
                return text + " -- " + word
        return "" 

    def removeat(self, text):
           return re.sub('@\w+', '', text)

    def removehash(self, text):
           return re.sub('#\w+', '', text)

    def removewspace(self, text):
           return re.sub('(?:\s+)', '', text)

    def removelinks(self, text):
           _link = re.compile(r'(?:(http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)
           _link_s = re.compile(r'(?:(https://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)
           text = _link.sub('', text)
           text = _link_s.sub('', text)
           return text

    def removepunc(self,text):
        punc = re.compile('[%s]' % re.escape(string.punctuation))
        return punc.sub('', text)
    
    def cleanstr(self, text):
        text = analyze.removeat(self, text)
        text = analyze.removehash(self, text)
        text = analyze.removepunc(self, text)
        text = analyze.removelinks(self, text)
        return analyze.removewspace(self,text)
        
