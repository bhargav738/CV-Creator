import streamlit as st
import pandas as pd
import datetime as dt
import re
from pathlib import Path
import textwrap

st.set_page_config(page_title="Job Application Copilot", layout="wide")

# Paths
DATA_DIR = Path("data")
OUT_DIR = Path("out")
DATA_DIR.mkdir(exist_ok=True, parents=True)
OUT_DIR.mkdir(exist_ok=True, parents=True)
TRACKER_PATH = DATA_DIR / "job_tracker.csv"

st.title("💼 Job Application Copilot (Power BI)")
st.caption("Generates tailored cover letters, tracks applications, and prepares bundles for quick apply.")

# --- Sidebar Profile
st.sidebar.header("Your Profile")
name = st.sidebar.text_input("Full Name", value="Bhargav Mallareddi")
email = st.sidebar.text_input("Email", value="bhargavmallareddi76@gmail.com")
phone = st.sidebar.text_input("Phone", value="9553558381")
linkedin = st.sidebar.text_input("LinkedIn", value="https://www.linkedin.com/in/bhargav-mallareddi/")
role_focus = st.sidebar.text_input("Target Role", value="Power BI Developer / Data Analyst")
years = st.sidebar.number_input("Years of Experience", 0.0, 20.0, 3.0, step=0.5)

# --- Cover Letter Templates
TEMPLATES = {
    "Big IT/Consulting": """Subject: Application for {role_title} at {company}

Dear {hiring_manager},

I am excited to apply for the {role_title} position at {company}. With {years}+ years of experience delivering enterprise-grade BI solutions at Aptean, 
I specialize in scalable data models, KPI dashboards, and Azure-based data pipelines.

Highlights:
• Centralized data warehouse reduced integration effort by 70% (cost savings).
• Automated API-driven reporting in Power BI, cutting manual effort by 80%.
• Delivered executive dashboards with RLS and advanced DAX.

I am drawn to {company}'s focus on transformation projects. I am confident my expertise in ETL optimization and stakeholder collaboration will add value.

Best regards,
{name}
{phone} | {email}
{linkedin}
""",
    "Product Company": """Subject: Application for {role_title} at {company}

Dear {hiring_manager},

I am writing to apply for the {role_title} role at {company}. I turn raw data into insights with Power BI, SQL, and Azure pipelines.

Recent work:
• Revenue dashboards with advanced DAX & drill-through.
• Azure Data Factory pipelines improving data consistency by 50%.
• API integrations eliminating manual uploads (80% faster refresh).

I admire {company}'s data-first culture and would love to contribute.

Regards,
{name}
{phone} | {email}
{linkedin}
""",
    "Startup/Mid-size": """Subject: Application for {role_title}

Dear {hiring_manager},

I'm excited to apply for {role_title} at {company}. I bring startup agility and full BI ownership—from ETL & modeling to dashboards & automation.

Highlights:
• KPI dashboards with drill-through & conditional formatting.
• Star/Snowflake models for performance.
• Python + Power Automate automation reduced recurring effort by 40%.

Sincerely,
{name}
{phone} | {email}
{linkedin}
"""
}

# --- Job Intake
st.subheader("➕ Add a Job")
with st.form("add_job"):
    company = st.text_input("Company")
    role_title = st.text_input("Role Title", value="Power BI Developer")
    category = st.selectbox("Company Type", list(TEMPLATES.keys()))
    hiring_manager = st.text_input("Hiring Manager", "Hiring Manager")
    jd = st.text_area("Paste Job Description (optional)")
    submitted = st.form_submit_button("Add Job")
    if submitted:
        if not TRACKER_PATH.exists():
            pd.DataFrame(columns=["added_on","company","role_title","category","hiring_manager","jd"]).to_csv(TRACKER_PATH, index=False)
        df = pd.read_csv(TRACKER_PATH)
        new = {"added_on": dt.date.today(), "company": company, "role_title": role_title,
               "category": category, "hiring_manager": hiring_manager, "jd": jd}
        df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
        df.to_csv(TRACKER_PATH, index=False)
        st.success(f"Added {role_title} @ {company} to tracker.")

# --- Tracker
st.subheader("📋 Job Tracker")
if TRACKER_PATH.exists():
    df = pd.read_csv(TRACKER_PATH)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No jobs yet.")

# --- Generate Cover Letter
st.subheader("✍️ Generate Cover Letter")
company_i = st.text_input("Company", "")
role_i = st.text_input("Role Title", role_focus)
category_i = st.selectbox("Template", list(TEMPLATES.keys()))
hiring_manager_i = st.text_input("Hiring Manager", "Hiring Manager")

if st.button("Generate Letter"):
    tpl = TEMPLATES[category_i]
    letter = tpl.format(
        role_title=role_i, company=company_i or "[Company]",
        hiring_manager=hiring_manager_i, years=int(years),
        name=name, phone=phone, email=email, linkedin=linkedin
    )
    st.text_area("Your Letter", letter, height=400)
