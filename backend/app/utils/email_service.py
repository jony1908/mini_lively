import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional
from .auth import TokenUtils
from ..config.settings import settings



class EmailService:
    @staticmethod
    def send_email(to_email: str, subject: str, html_content: str, text_content: Optional[str] = None):
        """Send an email using SMTP configuration."""
        if not all([settings.SMTP_USERNAME, settings.SMTP_PASSWORD, settings.FROM_EMAIL]):
            raise ValueError("Email configuration is incomplete. Check environment variables.")

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>"
        msg['To'] = to_email

        # Add text content if provided
        if text_content:
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)

        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send email
        try:
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    @staticmethod
    def create_verification_token(user_id: int) -> str:
        """Create a verification token for email verification."""
        from jose import jwt
        from ..config.settings import settings
        
        expire = datetime.utcnow() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)
        token_data = {
            "sub": str(user_id),
            "exp": expire,
            "type": "email_verification"
        }
        return jwt.encode(token_data, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_email_token(token: str) -> Optional[int]:
        """Verify an email verification token and return user ID."""
        payload = TokenUtils.verify_token(token, "email_verification")
        if payload:
            return int(payload.get("sub"))
        return None

    @staticmethod
    def send_verification_email(user_email: str, user_name: str, user_id: int) -> bool:
        """Send email verification email to user."""
        verification_token = EmailService.create_verification_token(user_id)
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"

        subject = "Verify Your Email - Mini Lively"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email</title>
            <style>
                body {{ font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif; margin: 0; padding: 0; background-color: #f8f9fc; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                .header {{ background-color: #2071f3; padding: 40px 20px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; font-size: 24px; font-weight: bold; }}
                .content {{ padding: 40px 20px; }}
                .content h2 {{ color: #0d131c; font-size: 20px; margin-bottom: 20px; }}
                .content p {{ color: #49699c; line-height: 1.6; margin-bottom: 20px; }}
                .button {{ display: inline-block; background-color: #2071f3; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
                .footer {{ background-color: #f8f9fc; padding: 20px; text-align: center; color: #49699c; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Mini Lively</h1>
                </div>
                <div class="content">
                    <h2>Welcome to Mini Lively, {user_name}!</h2>
                    <p>Thank you for creating your account. To get started with tracking your family's activities, please verify your email address by clicking the button below:</p>
                    <p style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </p>
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #2071f3;">{verification_url}</p>
                    <p><strong>This verification link will expire in {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} hours.</strong></p>
                    <p>If you didn't create an account with Mini Lively, you can safely ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2024 Mini Lively. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        text_content = f"""
        Welcome to Mini Lively, {user_name}!

        Thank you for creating your account. To get started with tracking your family's activities, please verify your email address by visiting this link:

        {verification_url}

        This verification link will expire in {settings.EMAIL_VERIFICATION_EXPIRE_HOURS} hours.

        If you didn't create an account with Mini Lively, you can safely ignore this email.

        © 2024 Mini Lively. All rights reserved.
        """

        return EmailService.send_email(user_email, subject, html_content, text_content)

    @staticmethod
    def send_welcome_email(user_email: str, user_name: str) -> bool:
        """Send welcome email after successful verification."""
        subject = "Welcome to Mini Lively!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to Mini Lively</title>
            <style>
                body {{ font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif; margin: 0; padding: 0; background-color: #f8f9fc; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                .header {{ background-color: #2071f3; padding: 40px 20px; text-align: center; }}
                .header h1 {{ color: white; margin: 0; font-size: 24px; font-weight: bold; }}
                .content {{ padding: 40px 20px; }}
                .content h2 {{ color: #0d131c; font-size: 20px; margin-bottom: 20px; }}
                .content p {{ color: #49699c; line-height: 1.6; margin-bottom: 20px; }}
                .button {{ display: inline-block; background-color: #2071f3; color: white; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; margin: 20px 0; }}
                .footer {{ background-color: #f8f9fc; padding: 20px; text-align: center; color: #49699c; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Mini Lively</h1>
                </div>
                <div class="content">
                    <h2>🎉 Your email has been verified!</h2>
                    <p>Hi {user_name},</p>
                    <p>Congratulations! Your email address has been successfully verified. You now have full access to all Mini Lively features:</p>
                    <ul style="color: #49699c; line-height: 1.8;">
                        <li>Track your children's activities</li>
                        <li>Manage recurring schedules (hockey, art, soccer)</li>
                        <li>Organize special events and birthday parties</li>
                        <li>Monitor attendance and progress</li>
                    </ul>
                    <p style="text-align: center;">
                        <a href="{settings.FRONTEND_URL}/dashboard" class="button">Get Started</a>
                    </p>
                    <p>If you have any questions or need help getting started, don't hesitate to reach out to our support team.</p>
                </div>
                <div class="footer">
                    <p>© 2024 Mini Lively. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        return EmailService.send_email(user_email, subject, html_content)