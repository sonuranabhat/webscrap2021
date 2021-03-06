import re
import csv
import json
from time import sleep
from bs4 import BeautifulSoup
import requests

def extract_salary_info(job_title,job_city):
    template='https://www.salary.com/research/salary/alternate/{}-salary/{}'
    
    url=template.format(job_title,job_city)
    
    try:
        response=requests.get(url)
        if response.status_code!=200:
            return None
    except requests.exceptions.ConnectionError:
        return None
    
    soup=BeautifulSoup(response.text,'html.parser')
    pattern=re.compile(r'Occupation')
    script=soup.find('script',{'type':'application/ld+json'},text=pattern)
    json_raw=script.contents[0]
    json_data=json.loads(json_raw)
    
    job_title=json_data['name']
    location=json_data['occupationLocation'][0]['name']
    description=json_data['description']

    ntile_10=json_data['estimatedSalary'][0]['percentile10']
    ntile_25=json_data['estimatedSalary'][0]['percentile25']
    ntile_50=json_data['estimatedSalary'][0]['median']
    ntile_75=json_data['estimatedSalary'][0]['percentile75']
    ntile_90=json_data['estimatedSalary'][0]['percentile90']

    salary_data=(job_title,location,description,ntile_10,ntile_25,ntile_50,ntile_75,ntile_90)
    return salary_data
    

def main(job_title):
    with open('largest_cities.csv',newline='')as f:
        reader=csv.reader(f)
        cities=[city for row in reader for city in row]
    
    #extract salary data from each city
    salary_data=[]
    for city in cities:
        result=extract_salary_info('senior-accountant',city)
        if result:
            salary_data.append(result)
            sleep(0.5)
    #save data to file
    with open('salary-results.csv','w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['Tilte','Location','Description','nTile10','nTile25','nTile50','nTile75','nTile90'])
        writer.writerows(salary_data)
        
    #return salary data
    return salary_data  