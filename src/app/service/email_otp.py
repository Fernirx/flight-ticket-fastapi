# xử lý OTP gữi về email bằng SMTP
import smtplib
import random
from email.message import EmailMessage

# Cấu hình SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "khanhduy030204@gmail.com"
EMAIL_PASSWORD = "wkei bkoh dakd gmwn"  

def generate_otp():
    """Tạo mã OTP ngẫu nhiên gồm 6 chữ số"""
    return str(random.randint(100000, 999999))

def send_otp_email(recipient_email, otp):
    """Gửi mã OTP qua email"""
    try:
        msg = EmailMessage()
        msg.set_content(f"Mã OTP của bạn là: {otp}")
        msg["Subject"] = "Xác thực OTP"
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient_email

        # Kết nối với SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ OTP đã được gửi tới {recipient_email}")
        return True
    except Exception as e:
        print(f"❌ Lỗi gửi email: {e}")
        return False
