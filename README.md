# Vaccine Slots Notifactions

## Register here
 https://cowin-slots-notif.herokuapp.com/

---

### Introduction
This repository contains the code for creating a web server to send updates about vaccine slots availability to register users. 

---

### Repository Structure

```
├── app
│ ├── configs
│ │   └── sample_config.py
│ └── main.py
├── check_scheduler
│ ├── run_checks.py
│ └── utils
│     ├── add_users.py
│     ├── check_slots.py
│     ├── emails.py
│     ├── loggers.py
│     ├── logging_setup.py
│     └── send_notifs.py
├── Procfile
├── README.md
├── requirements.txt
└── templates
    ├── index.html
    └── thank_you.html
```

---

### Setup and configuration
- All the required dependencies can be installed by running the command `pip3 install -r requirements.txt`
- Create a file in `app/configs/config.py`. Move the params from `sample_config.py`. Now you can add the details 
as per your requirement.
- Config parameters:

    - `max_retries`: maximum allowable retries to the APIs
    - `repeat_freq`: the frequency (in mins) of checking for slot updates
    - `notif_gap`: the gap in mins between two consecutive updates to the users
    - `sender_email`: email address of the sender
    - `sender_pass`: token generated from the email service to allow the application to send emails on your behalf
    - `aws_access_key`: access key for your security group from AWS IAM console
    - `aws_secret_key`: access key for your security group from AWS IAM console
    - `bucket_name`: name of the bucket created on S3
    - `s3_file_name`: name of the object in the S3 bucket

---

### Webpage sample

On running `main.py`, the home page will look like this - 

![Home page sample](https://github.com/darpan-jain/cowin_slots_notif/blob/develop/static/images/result_form.png)

---
