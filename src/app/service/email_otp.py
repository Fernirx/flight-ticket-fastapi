# Xử lý OTP gửi về email bằng SMTP
import smtplib
import secrets
import re
from email.message import EmailMessage
from app.config.settings import settings
import logging
from email_validator import validate_email, EmailNotValidError

# Cấu hình logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cấu hình SMTP
SMTP_SERVER = settings.SMTP_SERVER
SMTP_PORT = settings.SMTP_PORT
EMAIL_SENDER = settings.EMAIL_SENDER
EMAIL_PASSWORD = settings.EMAIL_PASSWORD

def generate_otp():
    """Tạo mã OTP ngẫu nhiên"""
    return ''.join(secrets.choice("0123456789") for _ in range(6))

def is_valid_email(email):
    """Kiểm tra định dạng email hợp lệ bằng thư viện email_validator"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        logger.error("Email không hợp lệ: %s", e)
        return False

def send_otp_email(recipient_email, otp):
    """Gửi mã OTP qua email"""
    if not is_valid_email(recipient_email):
        logger.error("Email không hợp lệ: %s", recipient_email)
        return False

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

        logger.info("✅ Email đã được gửi thành công tới: %s", recipient_email)
        return True

    except smtplib.SMTPException as e:
        logger.error("❌ Lỗi SMTP khi gửi email: %s", e)
        return False

    except Exception as e:
        logger.error("❌ Lỗi không xác định khi gửi email: %s", e)
        return False
