import re, string, nltk
from text_proc import plural

class analyze:
    user = ["davewiner", "scobleizer", "techcrunch", "lifehacker", "tutsplus", "phoronix", "newsycbot", "lobsternews", "r_netsec", "io9", "javascriptdaily", "techmeme", "wiredfeed", "tomshardware"]
    words = ["linux", "kernel", "geek", "java", "javascript", "python", "c++", "nasa", "mozilla", "facebook", "google", "microsoft", "windows", "win10", "astronomy", "science", "touchscreen", "chromebook", "pfsense", "openbsd", "freebsd", "skype", "whatsapp", "space", "sci-fi", "scifi", "starship", "node.js", "nodejs", "apple", "tablet","wordpress", "script", "api", "data", "servers", "protocol", "ecmascript", "webgl", "nvidia", "chromium", "emberjs", "jquery", "angularjs", "perl", "ruby", "unix", "regex", "macbook", "yosemite", "typeface", "interface", "fedora", "redhat", "debian", "ubuntu", "archlinux", "gentoo", "imac", "shell", "programming", "curiosity", "git", "curl", "wget", "algorithm", "1080p", "webdev", "startups", "lisp", "erlang", "haskell", "monad", "closure", "clojure", "internet", "firefox", "safari", "opera", "scientist", "laptop", "textanalytics", "textual", "codec", "asteriod", "spyware", "antivirus", "warez", "adware", "comet", "twitter", "technology", "drone", "universe", "planet", "reorg", "layoff", "nosql", "database", "mysql", "mariadb", "lambda", "scalabililty", "mongodb", "driver", "bash", "tcsh", "realtime", "postgres", "UI",  "c#", "infosec", "starships", "astronaut", "html5", "css", "ember", "ember.js", "backbone", "backbone.js", "meteor", "meteor.js", "opensource", "debugging", "io.js", "iojs", "algorithmic", "svg", "developer", "dell", "ios", "github", "couchdb", "animation", "lego", "safari", "firefox", "openstack", "qemu", "toshiba", "gameplay", "3d", "hologram", "botnets", "rust", "c#", "malware", "yahoo", "vpn", "tor", "researchers", "pip", "virtualenv", "netflix", "hackers", "seagate", "gb/s", "shellcode", "machinelearning", "skylake", "intel", "multitouch", "typescript", "ionic", "viruses", "webrtc", "tech", "galaxy", "supernova", "ide", "disk", "tcp/ip", "netbios", "socket", "cybersecurity", "iot", "wifi", "bugzilla", "docker", "ethernet", "pattern", "encryption", "crypto", "bluetooth", "keyboard", "gnome", "http", "cache", "firmware", "router", "kde", "lmdb", "xfce", "sqlite", "emacs", "vim", "usb", "ssh", "openssh", "openssl", "e3", "sxsw", "vmware", "hp", "oracle", "canonical", "ddos", "apache", "nginx", "rdbms", "graphdb", "reactjs", "bigdata", "unity", "virtual-reality", "npm", "angular2", "itjobs", "saas", "paas", "cassandra", "bower", "browserify", "playstation", "xbox", "cyberspace", "voyager", "mars", "segfault", "bsod", "gitlab", "password", "nuget", "screenshot", "struct", "operator()", "url", "webkit", "firewall", "daemon", "bitcoin", "ethereum", "blockchain"]
    terms = ["star trek", "star wars", "design tool", "time dilation", "data compression", "text analytics", "desktop computers", "web performance", "computer science", "web development", "data science", "to develop", "job queue", "data streams", "transaction processing", "request prioritization", "mars rover", "joss whedon", "dev tools", "ip address", "ip addresses", "quantum computing", "intelligence tools", "virtual reality", "gaming machine", "cloud computing", "machine learning", "deep learning", "web 2.0", "net neutrality", "oculus rift", "htc vive", "js bin", "no mans sky", "far cry", "dota 2", "league of legends", "game design", "mac os x", "os x", "open source", "revision control", "source control", "real time", "no man's sky", "unreal engine", "domain name", "artificial intelligence", "cognitive computing", "video game development", "surf the web", "web application"]

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
            if ((word in wordlist) or (plural(word) in wordlist)):
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
        
