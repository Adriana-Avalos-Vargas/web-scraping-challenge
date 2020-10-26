#Import dependencies
from flask import Flask, render_template
import pymongo

#############################
#Create an instance of our flask app
app = Flask(__name__)

#Create a connectio variable
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

#Connect to mongo database and collections
db = client.mar_db
news = db.news

#Set the route
@app.route('/')
def index():
    #@i DONT KNOW :(
        mars_info = list(news.find())
        print(mars_info)
        print(len(mars_info[0]))



        # render an index.html template and pass it the data you retrieved from the database
        return render_template("index.html", mars_info=mars_info)


if __name__ == "__main__":
    app.run(debug=True)
