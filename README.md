# 🩺 AI Medical Appointment Scheduler

An AI-powered scheduling agent that automates patient booking, reduces no-shows, and streamlines clinic operations.  
Built as part of a healthcare AI case study.

---

## 🚀 Features
- Patient lookup (new vs returning) from EMR (CSV)
- Smart scheduling with real **Calendly API integration**
- Insurance information collection
- Automated intake form distribution (PDF via email)
- Appointment logging to Excel
- Email reminders (via Brevo API)
- Cancellation flow with reason tracking

---

## 🛠️ Tech Stack
- **Frontend:** Streamlit
- **Backend:** Python
- **Scheduling:** Calendly API
- **Email:** Brevo API
- **Data:** Pandas, Excel, CSV
- **Mock Data:** Faker
- **Hosting:** Local / Streamlit Cloud (optional)

---

## 📂 Project Structure

│
├── data/ # Synthetic patient + doctor data
├── forms/ # Intake form templates
├── src/ # Source code (Streamlit app + utils)
├── output/ # Appointment logs
├── requirements.txt
├── README.md