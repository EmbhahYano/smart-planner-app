import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Study Timetable Generator", layout="centered")

st.title("📚 Study Timetable Generator (Custom Times Per Subject)")

# --- User Inputs ---
subjects = st.text_input("✏️ Enter subjects separated by commas (e.g. Math, English, Science)")
days = st.number_input("📆 How many days do you want to plan for?", min_value=1, max_value=30, format="%d")
hours_per_subject = st.number_input("⏱️ Study duration for each subject (in hours)", min_value=1, max_value=6, value=1)

# --- Handle subject-specific time inputs ---
subject_list = [s.strip() for s in subjects.split(",") if s.strip()]
subject_times = {}

if subject_list:
    st.subheader("🕒 Select Start Time for Each Subject")
    for subject in subject_list:
        subject_times[subject] = st.time_input(f"{subject} Start Time", value=datetime.strptime("09:00", "%H:%M").time(), key=subject)

# --- Session state to store timetable ---
if 'timetable_data' not in st.session_state:
    st.session_state.timetable_data = {}

# --- Generate Timetable ---
if st.button("✅ Generate Timetable"):
    if not subject_list:
        st.warning("🚨 Please enter at least one subject.")
    else:
        timetable_data = {}

        for day in range(1, days + 1):
            day_schedule = []
            for subject in subject_list:
                start = datetime.combine(datetime.today(), subject_times[subject])
                end = start + timedelta(hours=hours_per_subject)
                slot = f"{subject} ({start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')})"
                day_schedule.append(slot)
            timetable_data[f"Day {day}"] = day_schedule

        st.session_state.timetable_data = timetable_data

        df = pd.DataFrame(timetable_data, index=[f"Slot {i+1}" for i in range(len(subject_list))])
        st.write("### 📅 Your Custom Time-Based Study Timetable")
        st.dataframe(df)

        # Download as CSV
        csv = df.to_csv().encode("utf-8")
        st.download_button("📥 Download as CSV", data=csv, file_name="study_timetable_custom.csv", mime="text/csv")

        st.success("✅ Timetable created successfully!")
        st.markdown("---")
