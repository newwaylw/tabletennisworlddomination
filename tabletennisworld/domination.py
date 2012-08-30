import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import bordering

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
  is_open = db.BooleanProperty(required=True)
  date = db.DateTimeProperty(auto_now_add=True)
    
def get_salutation(email):
  """ Take a guess at how to address someone based on the first
  segment of their email address """
  return email.split("@")[0].replace(".", " ").title() 

'''sets an open challenge'''  
def setOpenChallenge(result):
  challenge = Challenges(result['invader'],result['countryOfInvader'], result['defender'] , result['countryOfdefender'] ,True, datetime.datetime.now() )  
  challenge.put()
   
'''should we remove once the challenge/invasion is finished/expired instead?'''
def closeChallenge(result):
  challenge = Challenges(result['invader'],result['countryOfInvader'], result['defender'] , result['countryOfdefender'] ,False, datetime.datetime.now() )  
  challenge.put()
  
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

  #update territory info
  t_record = Territory.get_by_key_name(countryOfdefender)
  t_record.occupier = invader
  t_record.put()  

  db.put([invasionHistory])

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



class Domination(webapp2.RequestHandler):
  def post(self):
      
'''      



class WorldView(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'user'        : "adam@swiftkey.net",
            'countries' : [["United Kingdom",1],["France",2]],
            'people'    : [[1, "Adam", "blue"],
                           [2, "Anita", "red"]]
            }
        self.response.out.write (bordering.allCountries())
        #self.response.out.write(template.render('store_template.html', template_values))
        
app = webapp2.WSGIApplication([('/', WorldView)],
                              debug=True)
      
      
def main():
    run_wsgi_app(app)
'''
if __name__ == "__main__":
    main()
