#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Import dependencies
#Let's call the dependencies
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from splinter import Browser


# In[2]:


# Nasa mars news

# URL of page to be scraped
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'lxml'
soup = BeautifulSoup(response.text, 'lxml')
#Extract the div tag with class slide
results = soup.find_all('div', class_='slide')

#Lets extract the title and the description paragraph, store it in a dictionaty and append the dict to a list
mars_news = []

for result in results:
    #Scrape for the title
    title = result.find("div", class_="content_title").a.text
    print(title)
    #Scrape for the paragraph text
    paragraph =result.find("div", class_="rollover_description_inner").text
    print(paragraph)
    print("--------")
    #Lets create a dictionary
    news={
        "news_title": title,
        "news_p": paragraph
    }
    #Lets append the dictionary
    mars_news.append(news)

    
#Lets call the dictionary
mars_news


# In[3]:


# JPL Mars space images

#Lets do the splinter, declare executable path
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
#url 
url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url_image)

#Measing part of the the url
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


# In[4]:


images_url


# In[7]:


# Mars weather

# URL of page to be scraped
url_mw = 'https://twitter.com/marswxreport?lang=en'

# Retrieve page with the requests module
response_mw = requests.get(url_mw)

# Create BeautifulSoup object; parse with 'lxml'
soup_mw = BeautifulSoup(response_mw.text, 'lxml')

#Extract mars weather
results_mw = soup_mw.find_all('span', class_='css-901oao r-1adg3ll r-1b2b6em r-q4m81j')

#see it
results_mw


# In[8]:


#Mars Facts

#Lets get the url
url_mt = 'https://space-facts.com/mars/'
#Lets get the tables
tables = pd.read_html(url_mt)
#Convert to a pandas df
df = tables[0]
df.columns = ['Mars fact', 'Value']
df.head()


# In[9]:


#Convert to an html table
html_table = df.to_html()
html_table


# In[10]:


#Mars hemispheres


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


#Create an empty list

hem_list=[]

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


# In[11]:


hem_list


# In[ ]:




