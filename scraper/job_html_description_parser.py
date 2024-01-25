import os
import json
from bs4 import BeautifulSoup

from JobDescription import JobDescription

RESOURCES_PATH = "../resources"
OUTPUT_PATH = "../output/job_descriptions.json"


def get_jobs():
    job_descriptions = []
    for file_name in os.listdir(RESOURCES_PATH):
        if ".html" not in file_name:
            continue
        job_id = file_name.strip(".html").split("/")[-1]

        with open(os.path.join(RESOURCES_PATH, file_name), 'r', encoding='utf-8') as file:
            file_content = file.read()
            soup = BeautifulSoup(file_content, "html.parser")
            headline = soup.find('div', class_="posting-headline")
            role = headline.find("h2").text
            headline_categories_section = headline.find("div", class_="posting-categories")
            headline_categories = headline_categories_section.find_all("div")
            location = headline_categories[0].text
            secondary_location = headline_categories_section.find("span")
            if secondary_location:
                location += secondary_location.text
            department = headline_categories[1].text
            work_type = headline_categories[2].text
            location_type = headline_categories[3].text
            job_description_section = soup.find("div", attrs={"data-qa": "job-description"})
            job_description_divs = job_description_section.find_all("div")
            job_description_parts = [job_description_part.text for job_description_part in job_description_divs]
            non_empty_divs = list(filter(lambda x: x.strip() != "", job_description_parts))
            job_description = '\n'.join(non_empty_divs)
            sections = soup.find_all("div", class_="section")
            typical_day_section = sections[2]
            print(job_id)
            typical_day_header = typical_day_section.find("h3")
            if typical_day_header:
                job_description += typical_day_header.text
                typical_day_tasks = [typical_day_task.text.replace("::marker", "•") for typical_day_task in
                                     typical_day_section.find_all("li")]
                job_description += '\n'.join(typical_day_tasks)
            potential_fit_section = sections[3]
            potential_fit_header = potential_fit_section.find("h3")
            if potential_fit_header:
                job_description += potential_fit_header.text
                potential_fit_reasons = [potential_fit_reason.text.replace("::marker", "•") for potential_fit_reason in
                                         potential_fit_section.find_all("li")]
                job_description += '\n'.join(potential_fit_reasons)
            job = JobDescription(job_id, role, department, location, work_type, location_type, job_description)
            job_descriptions.append(job)
    return job_descriptions


def save_job_descriptions(job_descriptions):
    json_jobs = [job.to_dict() for job in job_descriptions]
    with open(OUTPUT_PATH, "w") as json_file:
        json.dump(json_jobs, json_file)


if __name__ == "__main__":
    jobs = get_jobs()
    print(jobs)
    save_job_descriptions(jobs)
