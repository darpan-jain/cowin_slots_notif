from datetime import datetime

from check_scheduler.utils.emails import Email
import check_scheduler.utils.loggers as lg

class Notifications:

	def __init__(self, conf):
		self.config = conf
		self.notif_gap = conf.notif_gap
		lg.app.info(f"Gap between slot notifications is {self.notif_gap} mins")
		self.last_notif = datetime.now()
		self.email = Email(self.config)

	def send_emails(self, centers_data, date, first=False):
		current_time_diff = self.get_time_diff()
		if  current_time_diff >= self.notif_gap or first:
			lg.app.info(f"Sending notification emails at {self.last_notif}")
			self.email.send_email(centers_data, date)
			self.last_notif = datetime.now()
		else:
			lg.app.info(f"Notification already sent {current_time_diff} mins ago, can't spam users!")

	def get_time_diff(self):
		return int(((datetime.now() - self.last_notif).seconds) / 60)

	# To add support for Whatsapp notification
	# def send_whatsapp_msg(self):
		# self.whatsapp.send_whatsapp_msg()