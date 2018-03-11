
# coding: utf-8

# In[10]:


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests 
import sys




# In[11]:


# From this we must first import all the player names. 
# The name list will contain the names of all the players 
# The Categories list will contain the titles for Name, Date started in NBA etc. )

# For the sake of testing we will use Short as the variable in place of alphabet to save time 


short = ['a','b']
alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','z']
url_list = []
name_list = []

for letter in short :
    url1 = 'https://www.basketball-reference.com/players/{}/'.format(letter)
    url_list.append(url1)

sample_url = url_list[0]

html = urlopen(sample_url)
soup = BeautifulSoup(html, 'lxml')
categories = [th.getText() for th in soup.findAll('tr')[0].findAll('th')]

categories 







    
    


# In[12]:


# The following cell creates the list of all NBA player names that are valid as inputs 

for url in url_list:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    data_rows = soup.findAll('tr')
    info = [[td.getText() for td in data_rows[i].findAll('th')]
                  for i in range(len(data_rows))]
    for i in info:
        if i != categories:
            name_list.append(i[0])
print(name_list)
len(name_list)
    

    
   


# In[13]:


# Now that we have all the players names in our list, when someone enters a playername, we can now take 
# to the page that contains all of the players statistics. 


# In[14]:


# We want a program that can extract a players data and display it as a Pandas DB.

def dataextract(url):
    html = urlopen(url)
    soup = BeautifulSoup(html,'lxml')
    headers = [th.getText() for th in soup.findAll('tr')[0].findAll('th')]
    data_rows = soup.findAll('tr')[1:]
    statistics = [[td.getText() for td in data_rows[i].findAll('td')]
              for i in range(len(data_rows))]
    seasons = [[a.getText() for a in data_rows[i].findAll('a')]
            for i in range(len(data_rows))]
    for i in range (len(seasons)-1):
        if (seasons[i]) == []:
            statistics[i].insert(0,'NA')
        else:
            statistics[i].insert(0,(seasons[i])[0])
    df =  pd.DataFrame(statistics, columns = headers)
    print(df)
    
    


# In[15]:


# This Program will take the name of the player given, and convert the string the form "5 letters of last name"
# + 2 letter of first name + 01. Then it will return the url that we want to access. 

# String(Playername) -> String(site page for player)

def stringclean(x):
    wholename = x.split()
    firstname = wholename[0]
    lastname = wholename[1]
    firstletter = (str(lastname)[:1]).lower()
    strname = (str(lastname)[:5]).lower() + (str(firstname[:2])).lower() + '01'
    playerpage = 'https://www.basketball-reference.com/players/{}/{}.html'.format(firstletter, strname)
    return playerpage 
    



# In[16]:


# From the above list of players names, we will now go through the website and take their data, storing it in a Pandas Dataframe. 


# In[18]:


# This module will allow us a user to type in a players name and display statistics accordingly. 
# The function that we run will first ask for a players name, after verifying that it is a real player, 
# the console will prompt the user into taking an action. 


def func():
    x = input("Give a name")
    if x == "Quit" or x == "quit":
        sys.exit()  
    if x in name_list:
        y = input("What would you like to do")
        if y == "Display Stats":
            playerpage = stringclean(x)
            dataextract(playerpage)
        if y == "Plot":
            #Unfinished
        else:
            func()
    else:
        func()
    
    
func() 

