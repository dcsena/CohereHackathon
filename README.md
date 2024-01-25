# About
This repo uses Cohere's embedding API and Streamlit to build a job recommendation based on user inputs resume.
The database used is Cohere's job postings, scraped and parsed and stored in this repo. Scrape was done at 1/24/2024.
# Environment Setup

```commandline
python3 -m venv venv/
pip install -r requirements.txt
```

# Dataset Setup
Run the job scraper:
```commandline
python3 scraper/job_scraper.py
```
Next, run the description parser
```commandline
python3 job_html_description_parser.py
```

# Running App
```commandline
CO_API_KEY={REDACTED} CO_MODEL_NAME="embed-english-v2.0" streamlit run main.py
```
# Future Improvements
- Only supports text-based resumes. Run your PDF resume through an online PDF to text converter and then make touch-ups as needed.
- Filtering based on other criteria (location, remote, etc.)