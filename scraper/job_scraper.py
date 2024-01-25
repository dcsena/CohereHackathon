import requests
from bs4 import BeautifulSoup

BASE_URL = "https://jobs.lever.co/cohere"
TITLE_CLASS_NAME = "posting-title"


def get_job_links():
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    links = soup.find_all('a', class_=TITLE_CLASS_NAME)
    return [link.get('href') for link in links if link.get('href')]


def save_all_jobs():
    job_links = get_job_links()
    for job_link in job_links:
        page = requests.get(job_link)
        job_id = job_link.split("/")[-1]
        page_url = "resources/{}.html".format(job_id)
        with open(page_url, 'w', encoding='utf-8') as file:
            file.write(str(page.content))


if __name__ == "__main__":
    save_all_jobs()
