# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import csv
import streamlit as st
import pandas as pd
import os

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
with st.form("survey_form"):
    category_input = st.text_input("Who is your favorite Chelsea player?")
    value_input = st.text_input("How many Chelsea matches do you watch per month? (a whole number)")

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        category = category_input.strip().title()
        value_text = value_input.strip()

        if category == "" or not value_text.isdigit():
            st.error("Please enter a player name and a whole number of matches (like 6).")
        else:
            file_exists = os.path.exists('data.csv') and os.path.getsize('data.csv') > 0

            needs_newline = False
            if file_exists:
                with open('data.csv', 'rb') as f:
                    f.seek(-1, 2)
                    needs_newline = f.read(1) not in (b"\n", b"\r")

            with open('data.csv', 'a', newline='', encoding='utf-8') as f:
                if needs_newline:
                    f.write("\n")
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["category", "value"])
                writer.writerow([category, value_text])

            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category}, **Value:** {value_text}")


# DATA DISPLAY
st.divider()
st.header("Current Data in CSV")

if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    current_data_df = pd.read_csv('data.csv')
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
