import requests
from bs4 import BeautifulSoup

def get_last_page(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")

    last_pages = pages[-2].get_text(strip=True)
   
    return int(last_pages)  #get_text는 string, int로 변환해줌


def extract_jobs(last_page, url):
    jobs = []

    for page in range(
            last_page):  #range는 string을 accept안함. 그래서 int(last_pages)를 했던것
        print(f"Scrapping SO : Page - {page+1}")
        result = requests.get(f"{url}&pg={page+1}")
        
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for job_result in results:
            
            job = find_jobs(job_result)
            jobs.append(job)
    return jobs


def find_jobs(html):  #find title
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]

    try:
        company, location = html.find("h3", {
            "class": "mb4"
        }).find_all("span", resursive=False)
        
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        job_id = html["data-jobid"]

    except ValueError: 
        company, location, _ = html.find("h3", {
            "class": "mb4"
        }).find_all("span", resursive=False)
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        _ = _.get_text(strip=True)  
        job_id = html["data-jobid"]


    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def get_SO_jobs(word):  
  url = f"https://stackoverflow.com/jobs?q={word}" 

  last_page = get_last_page(url)  #returns last_pages
  jobs = extract_jobs(last_page, url)

  return jobs


