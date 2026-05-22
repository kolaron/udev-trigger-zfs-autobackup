import smtplib
import yaml
from email.message import EmailMessage
from log_util import Logging
from config_reader import SmtpConfig

# Enclose the mail sending logic in a function
def send_email(subject, body, config: SmtpConfig, logger: Logging):

    # Create the plain-text email
    message = EmailMessage()
    message.set_content(body)  # Set email body
    message['Subject'] = subject  # Set email subject
    message['From'] = config.login  # Set email from

    # Send the email to all recipients
    message['To'] = config.recipients#['smtp']['recipients']  # Set current recipient
    # Send the email
    try:
        context = ssl.create_default_context()
        if config.port == 465:
            with smtplib.SMTP_SSL(config.server, config.port, context=context) as server:
                server.login(config.login, config.password)
                server.send_message(message)
        else:
            with smtplib.SMTP(config.server, config.port) as server:
                server.ehlo()
                server.starttls(context=context)
                server.ehlo()
                server.login(config.login, config.password)
                server.send_message(message)

        logger.log(f"Email sent successfully to {config.recipients}!")
    except Exception as e:
        logger.error(f"Error sending email to {config.recipients}: {e}")

def mail(message: str, config: SmtpConfig, logger: Logging):
    logger.log(message)
    if config is not None:
        send_email("ZFS-Autobackup with UDEV Trigger", message, config, logger)
    
def mail_error(message: str, config: SmtpConfig, logger: Logging):
    logger.error(message)
    if config is not None:
        send_email("ERROR: ZFS-Autobackup with UDEV Trigger", message, config, logger)

def mail_exception(message: str, config: SmtpConfig, logger: Logging):
    logger.exception(message)
    if config is not None:
        send_email("ERROR: ZFS-Autobackup with UDEV Trigger", message, config, logger)