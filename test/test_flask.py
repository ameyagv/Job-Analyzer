from src.app import app, add, mongodb_client
import pandas as pd

db = mongodb_client.db


def test_home_page():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b"Get Job Postings" in response.data


def test_search_page():
    response = app.test_client().get('/search')
    assert response.status_code == 200
    assert b"Job Title" in response.data
    assert b"Location" in response.data
    assert b"Company Name" in response.data
    assert b"Technical skills" in response.data
    assert b"Job Type" in response.data


def test_search_page_submit():
    add_sample_data()
    response = app.test_client().post("/search", data={
        "title": "",
        "type": "",
        "location": "",
        "companyName": "",
        "skills": "",
    })
    assert response.status_code == 200


def test_search_page_submit_zero_results():
    response = app.test_client().post("/search", data={
        "title": "zzzzzzzzzzz",
        "type": "yyyyyyyyyyy",
        "location": "xxxxxxx",
        "companyName": "wwwwwwww",
        "skills": "vvvvvvvvv",
    })
    assert response.status_code == 200


def test_add_db():

    add_sample_data()


def add_sample_data():
    df = pd.DataFrame()

    job_dict = {
        "Job Title": "Software Engineer, New Grad",
        "Company Name": "IXL Learning",
        "Location": "Raleigh, NC",
        "Date Posted": "2 days ago",
        "Total Applicants": "Over 200 applicants",
        "Job Description": "IXL Learning, a leading edtech company with products used by 13 millio…",
        "Job Link": "https://www.linkedin.com/jobs/view/externalApply/3200864048?url=https%…",
        "Seniority level": "Not Applicable",
        "Employment type": "Full-time",
        "Job function": "Engineering and Information Technology",
        "Industries": "E-Learning Providers",
        "skills": "linux,react,ui,scala,sql,python,java"
    }
    df = df.append(job_dict, ignore_index=True)
    add(db, df)
