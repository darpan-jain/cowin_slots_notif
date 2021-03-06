import os

import boto3
import pandas as pd

class HandleData:

	def __init__(self, lg, config):
		self.lg = lg
		self.config = config
		self.path = "check_scheduler/utils/data/"
		self.data_file_name = "data.csv"
		self.s3_data_file = self.config.s3_file_name
		self.data_path = self.path+self.data_file_name
		self.session = boto3.Session(
			aws_access_key_id=self.config.aws_access_key,
			aws_secret_access_key=self.config.aws_secret_key,
		)
		self.s3_resource = self.session.resource('s3')
		self.bucket_name = self.config.bucket_name
		self.users_count = 0

	def add_user(self, user_info):
		if (user_info['email'] not in set(self.user_db['Email'])):
			self.user_db.loc[len(self.user_db.index)] = [user_info['fname'],
			                         user_info['lname'],
			                         user_info['number'],
			                         user_info['email']]
			self.lg.web.info(f"Adding data for {user_info['fname']} {user_info['lname']}")
			self.user_db.to_csv(self.data_path, index=False)
			self.users_count = self.user_db.shape[0]
			self.lg.web.info(f"Users count = {self.users_count}")
			if (len(self.user_db.index) % 10 == 0):
				self.lg.web.info("Users count = ", self.users_count)
				self.upload_csv()
			return True
		else:
			self.lg.web.info(f"User {user_info['fname']} {user_info['lname']} already exists!")
			return False

	def upload_csv(self):
		self.lg.web.info("Writing user db to csv file.")
		self.user_db.to_csv(self.data_path, index=False)
		self.s3_resource.Bucket(self.bucket_name).upload_file(Filename=self.data_path, Key=self.s3_data_file)
		self.lg.web.info("Uploaded file to S3!")

	def shutdown_upload(self):
		s3 = self.session.client('s3')
		obj = s3.get_object(Bucket=self.bucket_name, Key=self.s3_data_file)
		s3_db = pd.read_csv(obj['Body'])
		local_db = pd.read_csv(self.data_path, index_col=False)
		if (local_db.shape[0] > s3_db.shape[0]):
			self.lg.web.info(f"Local db users {local_db.shape[0]} > {s3_db.shape[0]} S3 db users")
			self.lg.web.info(f"Uploading data to S3 as {self.s3_data_file}.csv ...")
			self.upload_csv()
		else:
			self.lg.web.info(f"Local db users {local_db.shape[0]} <= {s3_db.shape[0]} S3 db users")
			self.lg.web.info("Skipping data upload to S3!")

	def download_csv(self):
		if not(os.path.exists(self.path)):
			os.mkdir(self.path)
			self.lg.web.info(f"{self.path} directory created!")
		self.s3_resource.Bucket(self.bucket_name).download_file(self.s3_data_file, self.data_path)
		self.lg.web.info("Downloaded file from S3!")
		self.user_db = pd.read_csv(self.data_path, index_col=False)
		self.users_count = self.user_db.shape[0]
		self.lg.web.info(f"Downloaded database with {self.users_count} details")

	@staticmethod
	def validate_input(user_info):
		num = str(user_info['number'])
		return (user_info['fname'].isalpha()) and (user_info['lname'].isalpha()) and num.isdigit() and len(num) == 10