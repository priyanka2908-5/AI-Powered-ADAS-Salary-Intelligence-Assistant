import streamlit as st
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
import os

# =====================================
# LOAD ENV FILE
# =====================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("Gemini API Key not found. Please add it to your .env file.")
    st.stop()

# =====================================
# GEMINI CONFIGURATION
# =====================================

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# =====================================
# LOAD DATASET
# =====================================

try:
    df = pd.read_excel("cleaned_data_final.xlsx")
except Exception as e:
    st.error(f"Dataset Loading Error: {e}")
    st.stop()

# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="ADAS Salary Intelligence Assistant",
    page_icon="🤖"
)

st.title("🤖 ADAS Salary Intelligence Assistant")

st.success("Dataset Loaded Successfully!")

st.write(f"📊 Total Records: {len(df)}")

# =====================================
# USER INPUT
# =====================================

question = st.text_input(
    "Ask a question about ADAS salaries"
)

# =====================================
# HYBRID CHATBOT
# =====================================

if question:

    q = question.lower()

    try:

        # ---------------------------------
        # HIGHEST SALARY ROLE
        # ---------------------------------
        if "highest salary" in q or "highest average salary" in q:

            highest = df.loc[df["salary_avg"].idxmax()]

            st.success("Answer")

            st.write(
                f"🏆 Highest Paying Role: {highest['standard_role']}"
            )

            st.write(
                f"💰 Average Salary: ₹{highest['salary_avg']:,.0f}"
            )

        # ---------------------------------
        # LOWEST SALARY ROLE
        # ---------------------------------
        elif "lowest salary" in q:

            lowest = df.loc[df["salary_avg"].idxmin()]

            st.success("Answer")

            st.write(
                f"📉 Lowest Paying Role: {lowest['standard_role']}"
            )

            st.write(
                f"💰 Average Salary: ₹{lowest['salary_avg']:,.0f}"
            )

        # ---------------------------------
        # HIGHEST PAYING LOCATION
        # ---------------------------------
        elif "location" in q and "highest" in q:

            location_salary = (
                df.groupby("location")["salary_avg"]
                .mean()
                .sort_values(ascending=False)
            )

            top_location = location_salary.index[0]

            st.success("Answer")

            st.write(
                f"📍 Highest Paying Location: {top_location}"
            )

            st.write(
                f"💰 Average Salary: ₹{location_salary.iloc[0]:,.0f}"
            )

        # ---------------------------------
        # TOTAL RECORDS
        # ---------------------------------
        elif "total records" in q:

            st.success("Answer")

            st.write(
                f"📊 Total Records in Dataset: {len(df)}"
            )

        # ---------------------------------
        # OVERALL AVERAGE SALARY
        # ---------------------------------
        elif "average salary" in q:

            avg_salary = df["salary_avg"].mean()

            st.success("Answer")

            st.write(
                f"💰 Overall Average Salary: ₹{avg_salary:,.0f}"
            )

        # ---------------------------------
        # GEMINI FALLBACK
        # ---------------------------------
        else:

            dataset_summary = df[
                [
                    "standard_role",
                    "location",
                    "salary_avg",
                    "skills",
                    "seniority"
                ]
            ].to_string(index=False)

            prompt = f"""
You are an ADAS Salary Intelligence Assistant.

Use ONLY the dataset provided below to answer the question.

Dataset:
{dataset_summary}

Question:
{question}

Instructions:
- Answer clearly and professionally.
- Use only dataset information.
- Do not make assumptions.
- If data is unavailable, say so.
"""

            response = model.generate_content(prompt)

            st.success("Gemini Analysis")

            st.write(response.text)

    except Exception as e:

        st.error(f"Error: {e}")
