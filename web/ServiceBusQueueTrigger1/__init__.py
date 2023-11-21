import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)
    
    conn = psycopg2.connect(host = "canltn-db-server.postgres.database.azure.com",
                            port="5432",
                            user = "canltn@canltn-db-server",
                            password = "Can12345678",
                            dbname = "techconfdb")
    
    cursor = conn.cursor()

    try:
        get_notification_query = "SELECT message, subject FROM notification WHERE ID = %s;"
        cursor.execute(get_notification_query, (notification_id,))
        notification_data = cursor.fetchone()

        get_attendees_query = "SELECT COUNT(*) FROM attendee;"
        cursor.execute(get_attendees_query)
        attendee_data = cursor.fetchall()
        attendee_count = len(attendee_data)

        update_notification_query = "UPDATE notification SET completed_date = %s, status = %s WHERE ID = %s;"
        cursor.execute(update_notification_query,(datetime.utcnow(), 'Notified {} attendees'.format(attendee_count), notification_id))

        # Cleanup
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
       if 'conn' in locals() and conn is not None:
            cursor.close()
            conn.close()

def send_email(email, subject, body):
    message = Mail(
        from_email=os.environ.get('ADMIN_EMAIL_ADDRESS'),
        to_emails=email,
        subject=subject,
        plain_text_content=body)

    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    sg.send(message)