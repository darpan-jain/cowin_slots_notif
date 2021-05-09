from datetime import datetime
import sched, time

from check_scheduler.utils.check_slots import CheckForSlots
from check_scheduler.utils.send_notifs import Notifications
import check_scheduler.utils.loggers as lg

class Scheduler:

	def __init__(self, conf):
		self.s = sched.scheduler(time.time, time.sleep)
		self.config = conf
		self.freq = conf.repeat_freq * 60
		self.first_notif = True

	def periodic_check(self, error_count, check, notifs, freq):
		today = datetime.today().date().strftime("%d-%m-%Y")
		# # For searching slots for future days
		# days_in_future = read_cfg().getint("PARAMS", "num days")
		# dates_list = [today+timedelta(days=x) for x in range(days_in_future)]

		try:
			valid_centers = check.check_availability(today, 363, 411037)
			if not valid_centers.empty:
				notifs.send_emails(valid_centers, today, first=self.first_notif)
				self.first_notif = False

		except Exception as e:
			lg.app.error(f"Error encountered while running checks: {e}", exc_info=True)
			error_count += 1
			if error_count > 5:
				lg.app.warning(f"Error count of {error_count} exceeded limit. Exiting process!")
				exit(-1)

		self.s.enter(freq, 1, self.periodic_check, (error_count, check, notifs, freq,))

	def run(self):
		check = CheckForSlots(self.config)
		notifs = Notifications(self.config)
		error_count = 0
		lg.app.info("STARTING SCHEDULER FOR SLOTS...")
		lg.app.info(f"Wait time between checks is {self.freq / 60} mins")
		self.s.enter(self.freq, 1, self.periodic_check, (error_count, check, notifs, self.freq, ))
		self.s.run()
