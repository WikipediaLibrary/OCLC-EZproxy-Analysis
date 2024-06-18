from html.parser import HTMLParser

class LogListParser(HTMLParser):
    def __init__(self):
        self.link = ''
        super().__init__()

    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == 'a':
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, return it.
               if name == 'href':
                   self.link = value
