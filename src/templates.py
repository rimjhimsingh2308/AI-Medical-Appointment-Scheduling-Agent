"""
Structured templates for Emails & SMS messages
"""

def build_confirmation_email(patient_name, doctor, date, time):
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.5;">
      <h2 style="color: #2E86C1;">Appointment Confirmation</h2>
      <p>Dear {patient_name},</p>
      <p>Your appointment has been successfully booked:</p>
      <ul>
        <li><b>Doctor:</b> {doctor}</li>
        <li><b>Date:</b> {date}</li>
        <li><b>Time:</b> {time}</li>
      </ul>
      <p>Please complete your intake form before the visit.</p>
      <p style="margin-top: 20px;">Best regards,<br/>PeakPulse Medical Center</p>
    </body>
    </html>
    """

def build_reminder_email(patient_name, date, time, step=1):
    if step == 1:
        return f"""
        <html><body>
        <h3>Reminder: Upcoming Appointment</h3>
        <p>Hi {patient_name},</p>
        <p>This is a friendly reminder of your appointment:</p>
        <b>{date} at {time}</b>
        <p>We look forward to seeing you!</p>
        </body></html>
        """
    elif step == 2:
        return f"""
        <html><body>
        <h3>Reminder: Intake Form Pending</h3>
        <p>Hi {patient_name},</p>
        <p>Please ensure you have filled out the intake form before your appointment on <b>{date} at {time}</b>.</p>
        </body></html>
        """
    elif step == 3:
        return f"""
        <html><body>
        <h3>Final Confirmation</h3>
        <p>Hi {patient_name},</p>
        <p>Please confirm if you are attending your appointment on <b>{date} at {time}</b>.</p>
        </body></html>
        """

def build_cancellation_email(patient_name, doctor, date, time, reason):
    return f"""
    <html><body>
    <h3>Appointment Cancelled</h3>
    <p>Dear {patient_name},</p>
    <p>Your appointment with {doctor} on <b>{date} at {time}</b> has been cancelled.</p>
    <p><b>Reason:</b> {reason}</p>
    </body></html>
    """

# ---------------- SMS ----------------
def build_confirmation_sms(doctor, date, time):
    return f"""✅ Appointment confirmed with {doctor} 
📅 {date} ⏰ {time}
Check your email for details."""

def build_reminder_sms(step, date, time):
    if step == 1:
        return f"⏰ Reminder: Appointment on {date} at {time}. See you soon!"
    elif step == 2:
        return f"📋 Reminder: Please complete your intake form before {date} {time}."
    elif step == 3:
        return f"❓ Please confirm if you will attend your appointment on {date} {time}."

def build_cancellation_sms(doctor, date, time, reason):
    return f"""❌ Appointment with {doctor} on {date} {time} cancelled.
Reason: {reason}"""
