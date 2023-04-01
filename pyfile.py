from bs4 import BeautifulSoup as bs
from article import Article_data 
import requests as req
import json 
import pandas
from datetime import date
import sqlite3 as sql




# requeting for the html script
step_a = req.get('https://www.theverge.com/') 

# initiating the beautifulsoup module using the in-build html parser
step_b = bs(step_a.text,'html.parser') 

0 # initiating a new integer variable for "id" argument
step_c = 0

# converting the data into json object
step_d = json.loads(step_b.find_all('script')[-1].string) 

#rooting down to the data
step_e= step_d['props']['pageProps']['hydration']['responses'][0]['data']['community']['frontPage']['placements'] 

# creating an new array to store the name of the article to prevent from creating an duplicate data
title_list = [] 


# connecting to the database-->
sqlite = sql.connect('new_article')
cursor = sqlite.cursor()

#ensuring the database is connected or not to further move on with the process-->
if sqlite:
    print('connected')
    
    # to check if the table is present or not by an indication of an 0 or 1
    table = cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ARTICLE_INFO'; ''').fetchall()[0][0]
    
    # To read the title's that are already in the table and saving it in a list to prevent from creating an duplicate data
    if table:
        title = cursor.execute('''SELECT TITLE FROM ARTICLE_INFO''')
        for i in title.fetchall():
            title_list.append(*i)
            
    try:
        for i in step_e:
            index = step_c # unique id for the article 
            title = i['placeable']['title']# title of the atricle
            author = i['placeable']['author']['fullName']  # author of the article
            published_link = i['placeable']['url'] # link of the article
            published_on = i['placeable']['publishDate'].partition('T')[0]  # publish date of the article
            step_c += 1
            
            article = Article_data(index,title,published_on,author,published_link)

            if table :
                if title not in title_list:
                    cursor.execute("INSERT INTO ARTICLE_INFO VALUES (?,?,?,?,?)",article.data())
                else:
                    print('data present')
                    continue
            else:
                print('creating....')
                cursor.execute("""CREATE TABLE ARTICLE_INFO(
                       ID INTEGER PRIMARY KEY,
                       TITLE TEXT NOT NULL,  
                       DATE  TEXT NOT NULL,  
                       AUTHOR TEXT NOT NULL,  
                       LINK TEXT NOT NULL)""")
                cursor.execute("INSERT INTO ARTICLE_INFO VALUES (?,?,?,?,?)",article.data())
                print('created......')
                table = 1


    except(TypeError):
        pass


    df = pandas.read_sql_query("SELECT TITLE,DATE,AUTHOR,LINK from ARTICLE_INFO", sqlite)
    df.index.name = 'ID'

    df.to_csv('{0}__verge.csv'.format(str(date.today()).replace('-','')))
    
    #this command is used to delete the table ,to check if any kind of error raises
    # sqlite.execute('DROP TABLE ARTICLE_INFO')

    sqlite.commit()

    sqlite.close()

    print('Completed the process')
else:
    print('Not connected')
    
    


