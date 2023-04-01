class Article_data():
    def __init__(self,uid,title,publish_date,author,link):
        self.uuid = uid
        self.title = title
        self.publish_date = publish_date
        self.author = author
        self.link = link
    
        
    @property   
    def date(self):
        return self.publish_date
    
    @property   
    def auth_name(self):
        return self.author
    
    @property   
    def article_link(self):
        return self.link
    
    @property   
    def name(self):
        return self.title
        

    def complete(self):
        return f'{self.title} published on {self.publish_date} by {self.author}'
    
    def data(self):
        return (self.uuid,self.title,self.publish_date, self.author,self.link)       
    
