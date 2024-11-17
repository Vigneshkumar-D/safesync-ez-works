import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import BackgroundTasks

SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587
EMAIL_ADDRESS = "example@gmail.com"  
EMAIL_PASSWORD = "app password"

def send_verification_email(email: str, encrypted_url: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(_send_email, email, encrypted_url)

def _send_email(email: str, encrypted_url: str):
    try:
        # Set up the email content
        subject = "Email Verification for Secure File Sharing"
        body = f"""
        Hi,
        <br>
        Thank you for signing up for our service. Please verify your email by clicking on the link below:
        <br>
        <br>
        <a href="http://localhost:8000/verify-email?token={encrypted_url}">Verify Email</a>
        <br>
        <br>
        If you did not sign up, please ignore this email.
        <br>
        <br>
        Regards,
        <br>
        Secure File Sharing Team
        """
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, email, msg.as_string())
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
