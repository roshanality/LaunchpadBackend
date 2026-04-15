import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
FROM_NAME = os.environ.get("FROM_NAME", "KGP Launchpad")

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")


def send_admin_otp(otp: str) -> bool:
    """
    Send a 6-digit OTP to the hardcoded admin email address.
    Returns True on success, False on failure.
    """
    if not SMTP_USER or not SMTP_PASS:
        # SMTP not configured — log OTP for local dev
        print(f"[DEV] Admin OTP: {otp}  (SMTP not configured)")
        return True

    subject = "KGP Launchpad — Admin Login OTP"
    html_body = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto;">
        <h2 style="color: #1e3a5f;">KGP Launchpad Admin Login</h2>
        <p>Your one-time password (OTP) for admin login is:</p>
        <div style="font-size: 36px; font-weight: bold; letter-spacing: 8px;
                    background: #f0f4ff; padding: 16px 24px; border-radius: 8px;
                    text-align: center; color: #1e3a5f; margin: 16px 0;">
            {otp}
        </div>
        <p style="color: #666;">This OTP is valid for <strong>5 minutes</strong>.</p>
        <p style="color: #666;">If you did not attempt to log in, please ignore this email.</p>
        <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
        <p style="color: #aaa; font-size: 12px;">KGP Launchpad &mdash; IIT Kharagpur</p>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{FROM_NAME} <{SMTP_USER}>"
    msg["To"] = ADMIN_EMAIL
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, ADMIN_EMAIL, msg.as_string())
        return True
    except Exception as e:
        print(f"[SMTP ERROR] Failed to send OTP email: {e}")
        return False
