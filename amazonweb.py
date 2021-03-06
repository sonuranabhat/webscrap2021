import csv     #import and export format for spreadsheets and databases
from bs4 import BeautifulSoup
#from selenium.webdriver import Chrome
from selenium import webdriver

#getting the next page with the help of query
def get_url(search_term):
    template='https://www.amazon.com/s?k={}&ref=nb_sb_noss_2'  #when certain item is serched the url was copied from amazon and the searched item was replaced with {}
    search_term=search_term.replace(' ','+')

    url=template.format(search_term)
    url+='&page{}'
    
    return url
    
def extract_record(item):
    #extract and return data from a single record
    atag=item.h2.a
    description=atag.text.strip()
    url='https://www.amazon.com'+ atag.get('href')

    try:
        price_parent=item.find('span','a-price')
        price=price_parent.find('span','a-offscreen').text
    except AttributeError:
        price_parent=''
        price=''
#error handling for empty string for price and rating
    try:
        rating=item.i.text
        review_count=item.find('span',{'class':'a-size-base','dir':'auto'}).text
    except AttributeError:
        rating=''
        review_count=''

    result=(description,price,rating,review_count,url)

    return result

def main(search_term):
    #start web driver
    PATH="C:\Program Files (x86)\chromedriver.exe"
    driver=webdriver.Chrome(PATH)

    records=[]
    url=get_url(search_term)

    for page in range(1,21):
        driver.get(url.format(page))
        soup=BeautifulSoup(driver.page_source,'html.parser')
        results=soup.find_all('div',{'data-component-type':'s-search-result'})

        for item in results:
            record=extract_record(item)
            if record:
                records.append(record)
    driver.close()

    #save data in csv 
    with open('results.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['Description','Price','Rating','ReviewCount','Url'])
        writer.writerows(records)

main('ultrawide monitor')