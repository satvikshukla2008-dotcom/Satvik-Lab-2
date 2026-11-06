# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import csv
import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

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

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        category = category_input.strip().title()
        value_text = value_input.strip()

        if category == "" or not value_text.isdigit():
            st.error("Please enter a player name and a whole number of matches (like 6).")
        else:
            file_exists = os.path.exists('data.csv') and os.path.getsize('data.csv') > 0

            # If the file doesn't end with a newline, add one so rows don't merge.
            needs_newline = False
            if file_exists:
                with open('data.csv', 'rb') as f:
                    f.seek(-1, 2)
                    needs_newline = f.read(1) not in (b"\n", b"\r")

            # Open in append mode ('a') and write the new row.
            with open('data.csv', 'a', newline='', encoding='utf-8') as f:
                if needs_newline:
                    f.write("\n")
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["category", "value"])  # header for a new/empty file
                writer.writerow([category, value_text])

            st.success("Your data has been submitted!")
            st.write(f"You entered: **Category:** {category}, **Value:** {value_text}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    current_data_df = pd.read_csv('data.csv')
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
