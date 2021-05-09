import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import pandas as pd
import check_scheduler.utils.loggers as lg

COLS_TO_USE = ['center_id',
               'name',
               'address',
               'pincode',
               'district_name',
               'date',
               'min_age_limit',
               'available_capacity',
               'vaccine',
               'slots',
               'fee_type']


class Email:

	def __init__(self, conf):
		self.conf = conf

	def send_email(self, centers_data, date):
		# Set incoming centers data to class variable
		self.centers = centers_data
		self.date = date

		# Create Email prequisities
		self.create_email()

		# Email contents
		email = MIMEMultipart()
		email['From'] = self.sender_address
		email['Subject'] = 'Vaccination Slots Update'
		email.attach(MIMEText(self.html, 'html'))

		# Start SMTP session and send email
		lg.app.info(f"Sending emails to {self.users_count} email IDs...")
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.starttls()  # enable security
		session.login(self.sender_address, self.sender_pass)
		session.sendmail(self.sender_address, self.recipients, email.as_string())
		session.quit()
		lg.app.info(f"Email sent to subscribed users!")

	def create_email(self):
		# Get updated list of subscribers
		subscribers = self.get_subscriber_list()
		recipients = subscribers["Email"]

		self.sender_address = self.conf.sender_email
		self.sender_pass = self.conf.sender_pass
		self.recipients = [elem.strip().split(',') for elem in recipients][0]
		self.users_count = len(recipients)
		self.html = self.create_html_content()

	def get_subscriber_list(self):
		return pd.read_csv("utils/data/data.csv")

	def create_html_content(self):
		centers_df = pd.DataFrame(self.centers, columns=COLS_TO_USE)
		return \
			f'''
			<html>
			    <body>
			        <h2 style="text-align: left;">
			            <strong>
			                <span style="color: #008000;">
			                    UNDER 45 VACCINATION SLOTS AVAILABLE!
			                </span>
			            </strong>
			        </h2>
			        <hr>
					
					<h3>Date: <span style="color: #FF8C00;">{datetime.strptime(self.date, '%d-%m-%Y').strftime('%d, %b, %Y')}</span>
				    <h3>Found <span style="color: #FF8C00;">{len(self.centers)}</span> centers with slots available!\n</h3>
				    <p>\n{centers_df.to_html(index=False, justify='center')}</p>
				
				    <h3>Please log on to https://selfregistration.cowin.gov.in <href="https://selfregistration.cowin.gov.in"> at the earliest to book the slots</h3>
			    </body>
			</html>
			'''
