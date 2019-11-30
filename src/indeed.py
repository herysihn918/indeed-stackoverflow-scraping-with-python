# Scrap jobs which includes 'python' from indeed.com

import requests
from bs4 import BeautifulSoup

# this URL sends the list of jobs which includes 'python' and the limit is 50. Please check this URL and see the result page.
LIMIT = 50
INDEED_URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"

# the function to extract the last page of the pagination_group
def extract_last_page():

    # get the response of the url
    result =  requests.get(INDEED_URL)

    # make a BeautifulSoup code from raw html text data
    soup = BeautifulSoup(result.text, "html.parser")

    # get the <div> tag part with class="pagination" from html
    pagination = soup.find("div", {"class": "pagination"})

    # get all the <a> tags in pagination <div> tag as the python list
    links = pagination.find_all('a')

    # get all the page numbers which denotes the page numbers
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
        
    # get the last page number from the current page
    last_page = pages[-1]

    return last_page

# the function to extract the job title and posting company from "div" component
def extract_job(html):
    title = html.find("div", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    try:  
        if company.find("a", {"data-tn-element":"companyName"}) is not None:
            company = company.find("a", {"data-tn-element":"companyName"}).string
        else:
            company = company.string
        company = str(company).strip()
    except:
        company = None
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {"title": title, "company": company, "location": location, "link": f"https://www.indeed.com/viewjob?jk={job_id}"}

# the function to extract the whole jobs...
def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"scraping indeed.com page - {page}")
        print(f"{INDEED_URL}&start={page * LIMIT}")
        result = requests.get(f"{INDEED_URL}&start={page * LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
        
    return jobs
    
def get_jobs():
    last_page = extract_last_page()
    jobs = extract_indeed_jobs(last_page)

    return jobs    
