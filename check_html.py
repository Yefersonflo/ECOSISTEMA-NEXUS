from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.tags = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            return
        self.depth += 1
        self.tags.append((tag, self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag in ('area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'):
            return
        
        while self.tags:
            last_tag, line = self.tags.pop()
            self.depth -= 1
            if last_tag == tag:
                return
            else:
                self.errors.append(f"Mismatched tag: Expected </{last_tag}> (from line {line}), got </{tag}> at line {self.getpos()[0]}")
                # Don't return, keep popping to recover
                continue
                
parser = MyHTMLParser()
path = "trd/templates/trd/editar_trd.html"
with open(path, "r", encoding="utf-8") as f:
    parser.feed(f.read())

for e in parser.errors[:20]:
    print(e)
