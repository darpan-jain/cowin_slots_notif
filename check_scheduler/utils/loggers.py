from check_scheduler.utils.logging_setup import setup_logger
import os

if not os.path.exists('logs'):
	os.mkdir('logs')

app = setup_logger('app', 'logs/app.log')
web = setup_logger('web', 'logs/web.log')