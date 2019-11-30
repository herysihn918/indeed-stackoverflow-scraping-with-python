# Scrap jobs which includes 'python' from indeed.com

import requests
from bs4 import BeautifulSoup

# this URL sends the list of jobs which includes 'python' and the limit is 50. Please check this URL and see the result page.
STACKOVERFLOW_URL = f"https://stackoverflow.com/jobs?q=python&sort=i"

# the function to extract the last page of the pagination_group
def extract_last_page():

    # get the response of the url
    result =  requests.get(STACKOVERFLOW_URL)

    # make a BeautifulSoup code from raw html text data
    soup = BeautifulSoup(result.text, "html.parser")

    # get the <div> tag part with class="pagination" from html
    pagination = soup.find("div", {"class": "pagination"})

    # get all the <a> tags in pagination <div> tag as the python list
    links = pagination.find_all('a')

    # get the last page number
    last_page = links[-2].get_text(strip=True)
    
    return int(last_page)

# the function to extract the job title and posting company from "div" component
def extract_job(html):
    title = html.find("div", {"class": "-title"}).find("a")["title"]
    company, location = html.find("div", {"class": "-company"}).find_all("span", recursive=False)
    job_id = html["data-jobid"]
    return {"title": title, "company": company.get_text(strip=True), "location": location.get_text(strip=True).strip("-").strip(" \r").strip("\n"), "link": f"https://stackoverflow.com/jobs/{job_id}"}

# the function to extract the whole jobs...
def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"scraping stackoverflow.com page: {page + 1}")
        print(f"{STACKOVERFLOW_URL}&pg={page + 1}")
        result = requests.get(f"{STACKOVERFLOW_URL}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
        
    return jobs
    
def get_jobs():
    last_page = extract_last_page()
    jobs = []
    jobs = extract_jobs(last_page)

    return jobs    
