# xử lý OTP gửi về email bằng SMTP
import smtplib
import random
from email.message import EmailMessage
from app.config import settings

# Cấu hình SMTP
SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
EMAIL_SENDER = settings.EMAIL_SENDER
EMAIL_PASSWORD = settings.EMAIL_PASSWORD

def generate_otp():
    """Tạo mã OTP ngẫu nhiên"""
    return str(random.randint(100000, 999999))

def send_otp_email(recipient_email, otp):
    """Gửi mã OTP qua email"""  
    try:
        msg = EmailMessage()
        msg.set_content(
            f"Xin chào,\n\n"
            f"Đây là mã xác thực OTP (One-Time Password) của bạn: {otp}\n"
            "Vui lòng nhập mã này để hoàn tất quá trình xác thực.\n"
            "Mã OTP này có hiệu lực trong một khoảng thời gian giới hạn.\n\n"
            "Xin cảm ơn.\n"
            "Trân trọng,\n"
            "Đội ngũ CNPMNHOM3"
        )
        msg["Subject"] = "[CNPMNHOM3] - Mã xác thực OTP"
        msg["From"] = EMAIL_SENDER
        msg["To"] = recipient_email

        # Kết nối với SMTP server và tự động đóng sau khi gửi
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("✅ Email đã được gửi thành công.")
        return True

    except Exception as e:
        print(f"❌ Lỗi khi gửi email: {e}")
        return False
