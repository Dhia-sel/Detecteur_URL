from urllib.parse import urlparse,urlunparse,unquote

class URLNormalizer:
    def __init__(self,url):
        self.url=url
        self.parsed=urlparse(url)

    def isSpecial(self):
        return self.parsed.scheme in ['data','mailto','tel']
    
    def decode(self):
        return (unquote(self.url))
    
    def normalizePath(self):
        path=self.parsed.path
        while '/./' in path :
            path=path.replace('/./','/')
        parts=path.split('/')
        stack=[]
        for part in parts:
            if part=='..':
                if stack:
                    stack.pop()
            elif part!='' :
                stack.append(part)
        return '/' + '/'.join(stack)

        

    def normalize_url(self):
        if self.isSpecial():
            return self.decode()
        path=self.normalizePath()
        normalized=urlunparse((
            self.parsed.scheme,
            self.parsed.netloc,
            path,
            self.parsed.params,
            self.parsed.query,
            self.parsed.fragment
        ))
        return normalized



