import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@expensetracker.com")

# Debug logging
print(f"[EMAIL CONFIG] SendGrid API Key configured: {bool(SENDGRID_API_KEY)}")
print(f"[EMAIL CONFIG] From Email: {FROM_EMAIL}")

def send_password_reset_email(to_email: str, reset_key: str):
    """Send password reset email with the reset key"""
    
    message = Mail(
        from_email=('Expense Team', FROM_EMAIL),
        to_emails=to_email,
        subject='Password Reset Request - Expense Tracker',
        html_content=f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #667eea;">Password Reset Request</h2>
            <p>You have requested to reset your password for your Expense Tracker account.</p>
            <p>Please use the following reset key to complete the password reset process:</p>
            <div style="background-color: #f7fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <h3 style="margin: 0; color: #2d3748; font-size: 24px; letter-spacing: 2px; text-align: center;">
                    {reset_key}
                </h3>
            </div>
            <p>This reset key will expire in 1 hour.</p>
            <p>If you did not request this password reset, please ignore this email.</p>
            <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 30px 0;">
            <p style="color: #718096; font-size: 12px;">
                This is an automated email from Expense Tracker. Please do not reply to this email.
            </p>
        </div>
        '''
    )
    
    try:
        if not SENDGRID_API_KEY:
            # For development/testing without SendGrid
            print(f"[DEV MODE] Password reset key for {to_email}: {reset_key}")
            return True
            
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"[EMAIL] Sent to {to_email} - Status: {response.status_code}")
        return response.status_code == 202
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send to {to_email}")
        print(f"[EMAIL ERROR] Error type: {type(e).__name__}")
        print(f"[EMAIL ERROR] Error message: {str(e)}")
        print(f"[EMAIL ERROR] This usually means the sender email ({FROM_EMAIL}) is not verified in SendGrid")
        print(f"[EMAIL ERROR] Please verify your sender at: https://app.sendgrid.com/settings/sender_auth")
        # Print the reset key so user can still reset password
        print(f"[FALLBACK] Password reset key for {to_email}: {reset_key}")
        # Return True to allow the flow to continue (key is still saved in DB)
        return True
