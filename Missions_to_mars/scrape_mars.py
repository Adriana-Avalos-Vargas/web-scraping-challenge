#####################################################################################################
#################### Scraping Mars' Web Pages #######################################################
#################### Adriana Avalos Vargas    #######################################################
#####################################################################################################


#Lets create a function

#def scrape( parameters ):
    #Aqui empieza a hacer el scraping
#Let's import the dependencies to do the scraping
#Basic dependencies
import pymongo
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time

#Dependencies to navigate with chrome driver
from splinter import Browser
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

##Dependencies to navigate with gecko driver
#Try with gecko driver
from selenium import webdriver
#Create the driver
driver = webdriver.Firefox()

#Create a dictionary to store dictionaries
mars_dict= {}

####################################################################################################################
#Nasa Mars News
#In this section the latest news anout Mars mission program is going to be scraped.
# Retrieve page with the requests module
# URL of page to be scraped
url_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

# Retrieve page with the requests module
response_news = requests.get(url_news)

# Create BeautifulSoup object; parse with 'lxml'
soup_news = BeautifulSoup(response_news.text, 'lxml')

#Extract the div tag with class slide
results_news = soup_news.find_all('div', class_='slide')

#Lets extract the title and the description paragraph, store it in a dictionaty and append the dict to a list
mars_news = []

for result in results_news:
    #Scrape for the title
    title = result.find("div", class_="content_title").a.get_text(strip=True)
    print(title)
    #Scrape for the paragraph text
    paragraph =result.find("div", class_="rollover_description_inner").get_text(strip=True)
    print(paragraph)
    print("--------")
    #Lets create a dictionary
    news={
        "news_title": title,
        "news_p": paragraph
    }
    #Lets append the dictionary
    mars_news.append(news)
       
#Let's extract the first dictionary values in the first item of the list
#Lets extract the first one
#Variable that stores the title of the first news
news_title = list(mars_news[0].values())[0]
#Variable that stores the paragraph text of the first news
news_p = list(mars_news[0].values())[1]

#adding variables to the mars_dict
dict_news = {'news_title':title, 'news_p':news_p}  
mars_dict.update(dict_news) 
#Print them
print("- - - - - - - - - - - - - - - - - - - - ")
print(f"Some mars news: {news_title} , {news_p}")

####################################################################################################################
#JPL Mars Space Images - Featured image
#In this section the web page of the NASA's Jet Propusion Laboratory is scraped to find the featured image.
#Save the url
url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
#Navigate  through chrome driver the website
browser.visit(url_image)

#Create a string with the Measing part of the the url
first_url ="https://www.jpl.nasa.gov"

#Create an empty list to store the url
images_url = []

#Iterate throug all the pages
for x in range(2):
    #Html object
    html= browser.html
    #Parse HTML  beautiful soup
    soup_image = BeautifulSoup(html, 'html.parser')
    #Retrieve all elements that contain image information
    results_image = soup_image.find_all('li', class_="slide")
    #Use beautiful soup's find method to navigate and retrieve attributes
    #title and URL
    for result in results_image:
        try:
            anchor = result.find('a', class_="fancybox")["data-fancybox-href"]
            c_url = f"{first_url}{anchor}"
            print(anchor)
            print("----")
            images_url.append(c_url)
        except:
            print("NO URL")
      
 #Click the next button
    try:
        browser.click_link_by_partial_text('MORE')
    except:
        print("Scraping complete")
          

#Extraxt the first image
featured_image_url = images_url[0]

#adding variables to the mars_dict
dict_image = {'image_url':featured_image_url}  
mars_dict.update(dict_image)

#PRINT IT
print(f"The final url is {featured_image_url}")


####################################################################################################################
#Mars weather
#In this section it is scraped the Mars Weather twitter account in order to find the latest Mars weather tweet from the page. We save the tweet text for the weather report as a variable called mars_weather.

#Stablish the twitter url
url_weather ='https://twitter.com/marswxreport?lang=en'
#Navigate throug the web page with gecko driver
driver.get(url_weather)
#find the weathet twit by class name
time.sleep(3)
content = driver.find_element_by_class_name('css-1dbjc4n')
time.sleep(3)

#extract the position of the word "InSight" from the last query
start = content.text.find("InSight")
#extract the position of the word "hPa" from the last query
end = content.text.find("hPa")
#Convert to text the query
result_weather = content.text
#Save the result in mars weather
mars_weather=result_weather[start:end+3]

weather_dict ={'weather':mars_weather}
mars_dict.update(weather_dict)
#Lets print the final result
print(mars_weather)

####################################################################################################################
#Mars Facts
# In this section a table that contains some facts about Mars is done. This table is converted into an html table with pandas.

#Lets get the url
url_mt = 'https://space-facts.com/mars/'
#Make pandas read the tables in the web page
tables = pd.read_html(url_mt)
#Add the column names
df = tables[0]
df.columns = ['Mars fact', 'Value']
print(df)
#Convert into a html table
html_table = df.to_html()
html_table

#Add the table to the dictionary
table_dict = {'table': html_table}

mars_dict.update(table_dict)


####################################################################################################################
# Mars hemispheres
# In this section it is done the web scraping of the USGS Atrogeology webpage. This is done in order to find high resolution images for each of Mar's hemispheres.

# URL of page to be scraped
url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# Retrieve page with the requests module
response_hem = requests.get(url_hem)

# Create BeautifulSoup object; parse with 'lxml'
soup_hem = BeautifulSoup(response_hem.text, 'lxml')

#Lets extrac the div tag with class item 
results_hem = soup_hem.find_all('a', class_="itemLink product-item")

principal_url = []
first_hem = "https://astrogeology.usgs.gov"

#Lets extract the url
for result in results_hem:
    anchor_hem = result["href"]
    hem_url = f"{first_hem}{anchor_hem}"
    print(anchor)
    print(hem_url)
    print("----")
    principal_url.append(hem_url)
        

#lets do the splinter inside a for loop
#Create an empty list

hem_list=[]
hem_name = []
hem_url = []

for addres in principal_url:
    aux_url = addres
    print(aux_url)
    # Retrieve page with the requests module
    aux_response = requests.get(aux_url)
    # Create BeautifulSoup object; parse with 'lxml'
    aux_soup = BeautifulSoup(aux_response.text, 'lxml')
    #Lets extract the title
    header = aux_soup.find_all('h2', class_="title")
    title = header[0].text
    #Lets extract the url
    downloads = aux_soup.find_all('div',class_= 'downloads')
    link = downloads[0].a['href']
    #Create a dictionary
    hem_dict = {"title": title, "img_url":link}
    #Add to the list
    hem_list.append(hem_dict)
    hem_name.append(title)
    hem_url.append(link)


print(hem_list)

#Add to the dictionary
hem_dict = {'hem_img':hem_list}
hem_urld ={'hem_url': hem_url}
hem_named={'hem_name': hem_name}
mars_dict.update(hem_dict)
mars_dict.update(hem_urld)
mars_dict.update(hem_named)
print(mars_dict)


#######################################################################
#MONGO DB PART
#Set up the connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
#Conect to mongo dg and collection
db = client.mar_db
news = db.news

news.insert_one(mars_dict)