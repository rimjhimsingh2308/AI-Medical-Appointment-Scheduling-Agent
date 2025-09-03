import streamlit as st
import datetime
from agents import lookup_patient
from utils import DOCTOR_CALENDLY_LINKS
from email_utils import send_email
from calendly_utils import get_scheduling_link

# ---------------------------
# Initialize session state
# ---------------------------
if "result" not in st.session_state:
    st.session_state.result = None
if "dob" not in st.session_state:
    st.session_state.dob = datetime.date.today()
if "appointment_confirmed" not in st.session_state:
    st.session_state.appointment_confirmed = False
if "insurance_filled" not in st.session_state:
    st.session_state.insurance_filled = False
if "form_sent" not in st.session_state:
    st.session_state.form_sent = False
if "reminder_1_sent" not in st.session_state:
    st.session_state.reminder_1_sent = False
if "reminder_2_sent" not in st.session_state:
    st.session_state.reminder_2_sent = False
if "reminder_3_sent" not in st.session_state:
    st.session_state.reminder_3_sent = False
if "appointment_cancelled" not in st.session_state:
    st.session_state.appointment_cancelled = False
if "cancellation_reason" not in st.session_state:
    st.session_state.cancellation_reason = ""

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="AI Scheduler", page_icon="🩺")
st.title("🩺 AI Medical Appointment Scheduler")

# ---------------------------
# Calendly Event Types Mapping
# ---------------------------
DOCTOR_EVENT_TYPES = {
    "Dr. Gupta": {
        30: "https://api.calendly.com/event_types/27d23997-e411-40cf-8469-e57ffa030314",
        60: "https://api.calendly.com/event_types/e856e2b7-ea1d-4f56-92dd-2d00f39292df"
    },
    "Dr. Patel": {
        30: "https://api.calendly.com/event_types/9a4cb6e9-ac5d-4d3a-b320-0512137df5a3",
        60: "https://api.calendly.com/event_types/6255a42a-5da3-46b3-8bd7-bdb9530ef815"
    },
    "Dr. Smith": {
        30: "https://api.calendly.com/event_types/9e510504-4b75-46d6-a6c0-77dfbcb8cfa1",
        60: "https://api.calendly.com/event_types/8e55bdb3-d75a-4d5b-b1c6-8a3a5586e421"
    }
}

# ---------------------------
# Step 1: Identify Patient
# ---------------------------
st.header("Step 1: Identify Yourself")

first_name = st.text_input("First Name")
last_name = st.text_input("Last Name")
st.session_state.dob = st.date_input("Date of Birth", value=st.session_state.dob)

if st.button("Lookup Patient"):
    if first_name and last_name and st.session_state.dob:
        result = lookup_patient(first_name, last_name, st.session_state.dob.strftime("%Y-%m-%d"))
        st.session_state.result = result
        st.session_state.first_name = first_name

        # Reset flow flags
        st.session_state.appointment_confirmed = False
        st.session_state.insurance_filled = False
        st.session_state.form_sent = False
        st.session_state.reminder_1_sent = False
        st.session_state.reminder_2_sent = False
        st.session_state.reminder_3_sent = False
        st.session_state.appointment_cancelled = False
        st.session_state.cancellation_reason = ""

        if result["status"] == "returning":
            st.success(f"Welcome back, {first_name}! You're a returning patient.")
        elif result["status"] == "new":
            st.info(f"Hi {first_name}, looks like you're new here. Let's get you registered.")
        else:
            st.error(result.get("message", "Unknown error occurred."))

        st.json(result["patient_data"])
    else:
        st.warning("Please fill in all fields to proceed.")

# ---------------------------
# Step 2: Schedule with Calendly
# ---------------------------
if st.session_state.result and not st.session_state.appointment_confirmed:
    result = st.session_state.result
    patient_info = result.get("patient_data")
    patient_type = result.get("status")

    st.header("Step 2: Schedule Appointment via Calendly")

    duration = 60 if patient_type == "new" else 30
    st.markdown(f"Appointment Duration: **{duration} minutes**")

    doctor_options = list(DOCTOR_EVENT_TYPES.keys())
    selected_doctor = st.selectbox("Choose Doctor", doctor_options)

    if selected_doctor:
        event_type_uri = DOCTOR_EVENT_TYPES[selected_doctor].get(duration)
        if event_type_uri:
            try:
                booking_url = get_scheduling_link(event_type_uri)
                st.success(f"Click below to schedule with {selected_doctor}:")
                st.markdown(f"📅 [Book on Calendly]({booking_url})")

                if st.button("✅ I have scheduled it on Calendly"):
                    st.session_state.appointment_confirmed = True
                    st.success("Appointment confirmed (via Calendly link).")
            except Exception as e:
                st.error(f"Calendly error: {e}")
        else:
            st.error("❌ No scheduling link found for this doctor and duration.")

# ---------------------------
# Step 3: Insurance Info
# ---------------------------
if st.session_state.appointment_confirmed and not st.session_state.insurance_filled:
    st.header("Step 3: Enter Insurance Details")

    insurance_carrier = st.text_input("Insurance Carrier")
    member_id = st.text_input("Member ID")
    group_number = st.text_input("Group Number")

    if insurance_carrier and member_id and group_number:
        st.success("✅ Insurance details received.")
        st.session_state.insurance_filled = True
    else:
        st.warning("Please complete all insurance fields.")

# ---------------------------
# Step 4: Intake Form
# ---------------------------
if st.session_state.insurance_filled:
    st.header("Step 4: Intake Form")

    if not st.session_state.form_sent:
        if st.button("Send Intake Form"):
            patient_email = st.session_state.result["patient_data"].get("email")
            send_email(
                to_email=patient_email,
                subject="Your Intake Form - PeakPulse",
                content="Dear patient, please find your intake form attached.",
                attachment_path="forms/New_Patient_Intake_Form.pdf"
            )
            st.success(f"✅ Intake form sent to {patient_email}")
            st.session_state.form_sent = True

    if st.session_state.form_sent:
        st.download_button(
            label="⬇️ Download Intake Form (PDF)",
            data=open("forms/New_Patient_Intake_Form.pdf", "rb").read(),
            file_name="New_Patient_Intake_Form.pdf",
            mime="application/pdf"
        )

# ---------------------------
# Step 5: Reminder System
# ---------------------------
if st.session_state.form_sent:
    st.header("Step 5: Reminder System (with email)")

    patient_email = st.session_state.result["patient_data"].get("email")

    if not st.session_state.reminder_1_sent:
        if st.button("📩 Send Reminder 1"):
            send_email(
                to_email=patient_email,
                subject="Reminder 1: Upcoming Appointment",
                content="Hi! Just a reminder that your appointment is coming up soon."
            )
            st.session_state.reminder_1_sent = True
            st.success("📬 Reminder 1 sent via email.")

    if st.session_state.reminder_1_sent and not st.session_state.reminder_2_sent:
        st.markdown("📝 **Reminder 2: Have you filled out the intake form?**")
        if st.button("✅ Yes, I have filled it"):
            send_email(
                to_email=patient_email,
                subject="Reminder 2: Intake Form Filled?",
                content="Thanks for confirming you've filled the intake form!"
            )
            st.session_state.reminder_2_sent = True
            st.success("📬 Reminder 2 sent via email.")
        elif st.button("❌ Not yet"):
            send_email(
                to_email=patient_email,
                subject="Reminder 2: Please Fill Intake Form",
                content="Please complete your intake form before the appointment."
            )
            st.session_state.reminder_2_sent = True
            st.warning("Reminder sent asking user to fill form.")

    if st.session_state.reminder_2_sent and not st.session_state.reminder_3_sent:
        st.markdown("📢 **Reminder 3: Are you still attending the appointment?**")
        if st.button("✅ Yes, I will attend"):
            send_email(
                to_email=patient_email,
                subject="Reminder 3: Confirmation",
                content="Thanks for confirming your appointment attendance."
            )
            st.session_state.reminder_3_sent = True
            st.success("📬 Confirmation sent.")
        elif st.button("❌ No, I want to cancel"):
            reason = st.text_input("Please tell us why you're cancelling:")
            if reason:
                send_email(
                    to_email=patient_email,
                    subject="Appointment Cancellation Received",
                    content=f"Your appointment was cancelled. Reason: {reason}"
                )
                st.session_state.appointment_cancelled = True
                st.session_state.cancellation_reason = reason
                st.session_state.reminder_3_sent = True
                st.error(f"Appointment cancelled. Reason: {reason}")
            else:
                st.warning("Please provide a reason to cancel.")
