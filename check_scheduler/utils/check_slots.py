import time
import requests
import pandas as pd
import check_scheduler.utils.loggers as lg
from collections import Counter

class CheckForSlots:

	def __init__(self, conf):
		self.max_retries = conf.max_retries
		self.status_codes = []

	def check_availability(self, date, district_id, pincode=None):
		self.date = date
		find_by_district = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict" \
		           f"?district_id={district_id}" \
		           f"&date={date}"
		centers = self.get_response(find_by_district)

		# if (pincode):
		# 	find_by_pin = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin" \
		# 	              f"?pincode={pincode}" \
		# 	              f"&date={date}"
		# 	resp_pincode = requests.get(find_by_pin)
		# 	print("By Pincode:\n",self.check_response(resp_pincode),"\n")

		return centers

	def get_response(self, url, retry_count=0):
		headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
		if (retry_count < self.max_retries):
			resp = requests.get(url, headers=headers, timeout=5.0)
			valid_centers = pd.DataFrame()
			self.status_codes.append((resp.status_code))
			lg.app.debug(f"Response received with status code {resp.status_code}")

			if (resp.status_code == 200):
				sessions = resp.json()['sessions']
				if (len(sessions) > 0):
					lg.app.info(f"Found {len(sessions)} sessions to query...")
					filter_age = filter(lambda x: x['min_age_limit'] < 45, sessions)
					filter_cap = filter(lambda x: x['available_capacity'] > 0, filter_age)
					lg.app.debug('Filtering for sessions done.')

					for index, center in enumerate(filter_cap):
						lg.app.info(f"{center['center_id']}:{center['name']} with {center['available_capacity']} available slots for min age of {center['min_age_limit']}")
						valid_centers =	valid_centers.append(center, ignore_index=True)

			elif resp.status_code == 403:
				lg.app.debug(f"API {resp.url} returned non-200 status code {resp.status_code}")
				lg.app.debug(f"Retrying times {retry_count}")
				time.sleep(3)  # Wait for 3 secs before retrying
				self.get_response(url, retry_count+1)

			else:
				lg.app.info("Not retry worthy status code: ", resp.status_code)
				lg.app.info("Skipping checks for this iteration.")

			self.status_codes = []
			lg.app.info(f"Response from {url} filtered and checked. Found {len(valid_centers)} valid centers!")
			return valid_centers

		else:
			lg.app.info(f"Retry count exceeded: {retry_count} for {url}")
			lg.app.info(f"Status codes for {self.date}: {dict(Counter(self.status_codes))}")
			self.status_codes = []

### Response Schema Sample
'''
{
  "sessions": 
  [
    {
      "center_id": 662889,
      "name": "Lonavala UPHC",
      "address": "Lonavala Nagar Parishad Hospital Near Nilkamal Theater",
      "state_name": "Maharashtra",
      "district_name": "Pune",
      "block_name": "Maval",
      "pincode": 410401,
      "from": "09:00:00",
      "to": "18:00:00",
      "lat": 18,
      "long": 73,
      "fee_type": "Free",
      "session_id": "456c7a8e-ea19-4e51-a109-654ad02d3e66",
      "date": "07-05-2021",
      "available_capacity": 22,
      "fee": "300",
      "min_age_limit": 45,
      "vaccine": "COVISHIELD",
      "slots": [
        "09:00AM-11:00AM",
        "11:00AM-01:00PM",
        "01:00PM-03:00PM",
        "03:00PM-06:00PM"
      ]
    },
    {
      "center_id": 592517,
      "name": "Primary Health Centre Karla",
      "address": "Primary Health Centre Karla",
      "state_name": "Maharashtra",
      "district_name": "Pune",
      "block_name": "Maval",
      "pincode": 410405,
      "from": "09:00:00",
      "to": "18:00:00",
      "lat": 18,
      "long": 73,
      "fee_type": "Free",
      "session_id": "6090d26d-6106-4625-8266-c90bf3304c8a",
      "date": "07-05-2021",
      "available_capacity": 1,
      "fee": "0",
      "min_age_limit": 45,
      "vaccine": "COVISHIELD",
      "slots": [
        "09:00AM-11:00AM",
        "11:00AM-01:00PM",
        "01:00PM-03:00PM",
        "03:00PM-06:00PM"
      ]
    }
	]
}
'''