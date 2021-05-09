from pydantic import BaseSettings

class Settings(BaseSettings):
    max_retries: int = 5 # allow 5 retries
    repeat_freq: float = 30 # in mins
    notif_gap: int = 10 # in mins
    sender_email: str = "<sender_email>"
    sender_pass: str = "<gmail token>"
    aws_access_key: str = "<aws user access key>"
    aws_secret_key: str = "<aws user secret key>"
    bucket_name: str = "<s3 bucket name>"

settings = Settings()