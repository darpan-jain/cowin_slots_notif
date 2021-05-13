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
		self.lg.web.info(f"Adding data for {user_info['fname']} {user_info['lname']}")
		df = pd.read_csv(self.data_path)
		df.loc[len(df.index)] = [user_info['fname'],
		                         user_info['lname'],
		                         user_info['number'],
		                         user_info['email']]
		df.to_csv(self.data_path, index=False)
		if (len(df.index) % 10 == 0):
			self.lg.web.info("Num of registered users = ",len(df.index))
			self.upload_csv()

	def upload_csv(self):
		self.lg.web.info("Writing user db to csv file.")
		self.user_db.to_csv(self.data_path, index=False)
		self.s3_resource.Bucket(self.bucket_name).upload_file(Filename=self.data_path, Key=self.s3_data_file)
		self.lg.web.info("Uploaded file to S3!")

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