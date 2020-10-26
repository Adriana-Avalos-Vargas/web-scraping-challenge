#Import dependencies
from flask import Flask, render_template, Response, request, redirect, url_for
import pymongo
from scrape_mars import scrape

#############################
#Create an instance of our flask app
app = Flask(__name__)

#Create a connectio variable
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)



#Set the route
@app.route('/')
def index():
    #@i DONT KNOW :(
        #Connect to mongo database and collections
        db = client.mar_db
        news = db.news  
        mars_info = list(news.find())
        print(mars_info)
        print(len(mars_info[0]))



        # render an index.html template and pass it the data you retrieved from the database
        return render_template("index.html", mars_info=mars_info)


@app.route('/scrape/')
def scrape():
    #Connect to mongo database and collections
    db = client.mar_db
    news = db.news
    mars_info = list(news.find())
    print(mars_info)
    print(len(mars_info[0]))
    #render an index.html template and pass it the data you retrieved from the database
    print ('I got clicked!')
    return render_template("index.html", mars_info=mars_info)
    



if __name__ == "__main__":
    app.run(debug=True)
