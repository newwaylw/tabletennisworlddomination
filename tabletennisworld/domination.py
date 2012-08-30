import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
#from google.appengine.ext.webapp.util import run_wsgi_app

class InvasionHistory(db.Model):
    '''records an invasion '''
    #id = db.IntegerProperty()
    invader = db.StringProperty(required=True) #login detail ?
    countryOfInvader = db.StringProperty(required=True) 
    defender = db.StringProperty(required=True) #login detail ?
    countryOfdefender = db.StringProperty(required=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Territory(db.Model):
    '''records the country and who occupies it'''
    countryName = db.StringProperty(required=True)
    '''current person'''
    occupier = db.StringProperty() 
    
class Challenges(db.Model):
  '''a list of open challenges'''
  invader = db.StringProperty(required=True)
  defender = db.StringProperty(required=True)
  countryOfdefender = db.StringProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)
    
def get_salutation(email):
  """ Take a guess at how to address someone based on the first
  segment of their email address """
  return email.split("@")[0].replace(".", " ").title() 

def everybodys_name():
  """ Get a list of everybody's names for reverse name matching """
  return Territory.all();
    
def update_result(result):
  """ Takes a series of parameters representing a match and commits the result,
  changing rankings and news feeds where necessary """
  invader = result['invader'] 
  countryOfInvader       = result['countryOfInvader'] 
  defender          = result['defender'] 
  countryOfdefender        = result['countryOfdefender'] 
  invasionHistory = InvasionHistory(
          invader         ,
          countryOfInvader,
          defender,
          countryOfdefender,
          datetime.datetime.now() )

  #
  t_record = Territory.get_by_key_name(countryOfdefender)
  t_record.occupier = invader
  Territory.put(t_record)  
  #update territory info

  db.put([invasionHistory,])
'''    
class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
'''

'''
def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')
'''

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    guestbook_name=self.request.get('guestbook_name')

    # Ancestor Queries, as shown here, are strongly consistent with the High
    # Replication Datastore. Queries that span entity groups are eventually
    # consistent. If we omitted the ancestor from this query there would be a
    # slight chance that Greeting that had just been written would not show up
    # in a query.
    greetings = db.GqlQuery("SELECT * "
                            "FROM Greeting "
                            "WHERE ANCESTOR IS :1 "
                            "ORDER BY date DESC LIMIT 10",
                            guestbook_key(guestbook_name))

    for greeting in greetings:
      if greeting.author:
        self.response.out.write(
            '<b>%s</b> wrote:' % greeting.author)
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))

    self.response.out.write("""
          <form action="/sign?%s" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
          <hr>
          <form>Guestbook name: <input value="%s" name="guestbook_name">
          <input type="submit" value="switch"></form>
        </body>
      </html>""" % (urllib.urlencode({'guestbook_name': guestbook_name}),
                          cgi.escape(guestbook_name)))


class AppPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')
        countries = db.GqlQuery("SELECT * "
                                 "FROM Invation "
                                 #"WHERE ANCESTOR IS :1 "
                                 #"ORDER BY date DESC LIMIT 10"
                                 )
        
        
'''
class Guestbook(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name')
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user().nickname()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook)],
                              debug=True)


class Domination(webapp2.RequestHandler):
  def post(self):
      
'''      
      
      
def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()