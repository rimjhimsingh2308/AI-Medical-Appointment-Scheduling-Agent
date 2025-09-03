import pandas as pd
import random
from faker import Faker
import os

fake = Faker()

def generate_synthetic_patients(num_patients=50, path="data/patients.csv"):
    genders = ["Male", "Female", "Other"]
    data = []

    for _ in range(num_patients):
        full_name = fake.name()
        first, last = full_name.split()[0], full_name.split()[-1]
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')
        email = fake.email()
        phone = fake.phone_number()
        city = fake.city()
        state = fake.state()
        zip_code = fake.zipcode()
        status = random.choice(["new", "returning"])

        data.append([first, last, dob, email, phone, city, state, zip_code, status])

    df = pd.DataFrame(data, columns=[
        "first_name", "last_name", "dob", "email", "phone",
        "city", "state", "zip_code", "status"
    ])

    df.to_csv(path, index=False)
    print(f"✅ Generated {num_patients} patients to {path}")


def generate_doctor_schedule(path="data/doctor_schedule.xlsx"):
    doctors = ["Dr. Smith", "Dr. Patel", "Dr. Gupta"]
    days = pd.date_range(start="2025-09-04", periods=14).tolist()
    rows = []

    for doc in doctors:
        for day in days:
            for hour in range(9, 17):  # 9 AM to 4 PM
                for minute in [0, 30]:  # 30-min slots
                    rows.append([doc, day.strftime("%Y-%m-%d"), f"{hour}:{minute:02d}", "available"])

    df = pd.DataFrame(rows, columns=["doctor", "date", "time", "status"])
    df.to_excel(path, index=False)
    print(f"✅ Generated doctor schedule to {path}")


def get_available_slots(duration_minutes, path="data/doctor_schedule.xlsx"):
    df = pd.read_excel(path)
    available = df[df['status'] == 'available']
    return available


def log_appointment(patient, doctor, date, time, duration, insurance=None, status="confirmed", cancellation_reason="", path="output/appointment_log.xlsx"):
    import pandas as pd

    record = pd.DataFrame([{
        "appointment_id": f"{patient['first_name'][:2].upper()}{patient['last_name'][:2].upper()}_{doctor.split()[1]}_{date.replace('-', '')}_{time.replace(':', '')}",
        "first_name": patient['first_name'],
        "last_name": patient['last_name'],
        "dob": patient['dob'],
        "doctor": doctor,
        "date": date,
        "time": time,
        "duration_min": duration,
        "insurance_carrier": insurance.get("carrier") if insurance else "",
        "insurance_member_id": insurance.get("member_id") if insurance else "",
        "insurance_group": insurance.get("group") if insurance else "",
        "status": status,
        "cancellation_reason": cancellation_reason
    }])

    if not os.path.exists(path):
        record.to_excel(path, index=False)
    else:
        existing = pd.read_excel(path)
        updated = pd.concat([existing, record], ignore_index=True)
        updated.to_excel(path, index=False)

    print(f"✅ Appointment logged to {path}")


def mark_slot_as_booked(doctor, slot_label, path="data/doctor_schedule.xlsx"):
    import pandas as pd

    date, time = slot_label.split(" at ")

    df = pd.read_excel(path)
    idx = df[
        (df["doctor"] == doctor) &
        (df["date"] == date) &
        (df["time"] == time)
    ].index

    if not idx.empty:
        df.at[idx[0], "status"] = "booked"
        df.to_excel(path, index=False)
        print(f"✅ Slot {slot_label} for {doctor} marked as booked.")


def send_sms(to_number, message, path="output/sms_log.txt"):
    """Simulated SMS sender – logs message to file"""
    with open(path, "a") as f:
        f.write(f"To: {to_number} | Msg: {message}\n")
    print(f"📱 SMS simulated to {to_number}: {message}")


# -----------------------------
# Calendly simulation links
# -----------------------------
DOCTOR_CALENDLY_LINKS = {
    "Dr. Patel": {
        30: "https://calendly.com/dr-patel/30min",
        60: "https://calendly.com/dr-patel/60min"
    },
    "Dr. Smith": {
        30: "https://calendly.com/dr-smith/30min",
        60: "https://calendly.com/dr-smith/60min"
    },
    "Dr. Gupta": {
        30: "https://calendly.com/dr-gupta/30min",
        60: "https://calendly.com/dr-gupta/60min"
    }
}
