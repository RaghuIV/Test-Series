def reset_password_email_template(first_name, last_name, reset_link):
    """
    Generate HTML email content for password reset.

    :param first_name: First name of the user
    :param last_name: Last name of the user
    :param reset_link: Password reset URL to include in the email
    :return: HTML string for the password reset email content
    :rtype: str
    """
    return f"""
    <p>Hello, {first_name} {last_name}</p>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
    <p>This link will expire soon.</p>
    """
    
def otp_email_template(otp_code):
    return f"""
    <html>
        <body>
            <h2>Your One-Time Password</h2>
            <p>Use the following OTP to verify your account:</p>
            <h1 style="color: #2c3e50;">{otp_code}</h1>
            <p>This OTP is valid for 10 minutes.</p>
        </body>
    </html>
    """
