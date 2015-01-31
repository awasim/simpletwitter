import re

_link = re.compile(r'(?:(http://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)
_link_s = re.compile(r'(?:(https://)|(www\.))(\S+\b/?)([!"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]*)(\s|$)', re.I)

def convertLinks(text):
    def replace(match):
        groups = match.groups()
        protocol = groups[0] or ''  # may be None
        www_lead = groups[1] or ''  # may be None
        return '<a href="http://{1}{2}" rel="nofollow" target="_blank">{0}{1}{2}</a>{3}{4}'.format(protocol, www_lead, *groups[2:])
    ctext = _link.sub(replace, text)
    return _link_s.sub(replace, ctext)
