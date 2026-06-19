import streamlit as st
import pandas as pd
import google.generativeai as genai

# =====================================
# GEMINI CONFIGURATION
# =====================================

API_KEY = "YOUR_GEMINI_API_KEY"

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# =====================================
# LOAD DATASET
# =====================================

df = pd.read_excel("cleaned_data_final.xlsx")

# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="ADAS Salary Intelligence Assistant",
    page_icon="🤖"
)

st.title("🤖 ADAS Salary Intelligence Assistant")

st.success("Dataset Loaded Successfully!")

st.write(f"Total Records: {len(df)}")

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
                f"🏆 Highest paying role: "
                f"{highest['standard_role']}"
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
                f"📉 Lowest paying role: "
                f"{lowest['standard_role']}"
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
                f"📍 Highest paying location: "
                f"{top_location}"
            )

            st.write(
                f"💰 Average Salary: "
                f"₹{location_salary.iloc[0]:,.0f}"
            )

        # ---------------------------------
        # TOTAL RECORDS
        # ---------------------------------
        elif "total records" in q:

            st.success("Answer")

            st.write(
                f"📊 Total records in dataset: {len(df)}"
            )

        # ---------------------------------
        # AVERAGE SALARY
        # ---------------------------------
        elif "average salary" in q:

            avg_salary = df["salary_avg"].mean()

            st.success("Answer")

            st.write(
                f"💰 Overall Average Salary: "
                f"₹{avg_salary:,.0f}"
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

Use ONLY the dataset below.

Dataset:
{dataset_summary}

Question:
{question}

Provide a clear and professional answer.
"""

            response = model.generate_content(
                prompt
            )

            st.success("Gemini Analysis")

            st.write(response.text)

    except Exception as e:

        st.error(f"Error: {e}")