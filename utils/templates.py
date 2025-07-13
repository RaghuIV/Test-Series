def reset_password_email_template(first_name, last_name, reset_link):
    return f"""
    <p>Hello, {first_name} {last_name}</p>
    <p>Click the link below to reset your password:</p>
    <a href="{reset_link}">Reset Password</a>
    <p>This link will expire soon.</p>
    """