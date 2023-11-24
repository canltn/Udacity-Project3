import logging
import os
from datetime import datetime
import psycopg2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import azure.functions as func
import config


def main(msg: func.ServiceBusMessage):
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info(
        'Python ServiceBus queue trigger processed message: %s', notification_id)

    # TODO: Get connection to database
    try:
        db_connection = psycopg2.connect(host = "canltn-db-server.postgres.database.azure.com",
                            port="5432",
                            user = "canltn@canltn-db-server",
                            password = "Can12345678",
                            dbname = "techconfdb")
        logging.info(f'Connection to the {db_connection} is successful')

        with db_connection.cursor() as cursor:
            # TODO: Get notification message and subject from database using the notification_id
            cursor.execute(
                "SELECT message, subject FROM notification WHERE id=%s", (notification_id,))
            logging.info(
                f"NotificationID {notification_id}: Get message and subject")

            row = cursor.fetchone()
            if row:
                message, subject = row
            else:
                raise Exception(
                    f"ID {notification_id}: Notification not found")

            if not message:
                raise Exception(f"ID {notification_id}: Message field empty")

            if not subject:
                raise Exception(f"ID {notification_id}: Subject field empty")

            logging.info(f"ID {notification_id}: {message}, {subject}")

            # TODO: Get attendees email and name
            cursor.execute("SELECT first_name, last_name, email FROM attendee")
            count = 0

            # TODO: Loop through each attendee and send an email with a personalized subject
            for row in cursor.fetchall():
                first_name, last_name, email = row
                logging.info(
                    f"ID {notification_id}: First Name: {first_name}, Last Name: {last_name}, E-mail: {email}")

                email_from = os.environ['ADMIN_EMAIL_ADDRESS']
                email_to = email
                email_subject = f"Hello, {first_name}"
                email_body = message

                mail = Mail(email_from, email_to, email_subject, email_body)
                send_grid = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])

                try:
                    send_grid.send(mail)
                except Exception as e:
                    logging.error(f"Error sending email to {email}: {e}")

                count += 1

            # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
            status = f"Notified {count} Attendees"
            logging.info(f"ID {notification_id}: {status} @ {datetime.now()}")

            update_command = "UPDATE notification SET status=%s, completed_date=%s WHERE id=%s"
            cursor.execute(
                update_command, (status, datetime.now(), notification_id))
            db_connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.exception(error)
    finally:
        # TODO: Close connection
        if db_connection:
            db_connection.close()
