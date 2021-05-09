# Vaccine Slots Notifactions - https://cowin-slots-notif.herokuapp.com/

## Contents

- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [Results](#results)

***

## Introduction
This repository contains the code for creating a web server to send updates about vaccine slots availability to register users. 

***

## Repository Structure

```
├── app
│   ├── configs
│   │   └── sample_config.py
│   └── main.py
├── check_scheduler
│   ├── run_checks.py
│   └── utils
│       ├── add_users.py
│       ├── check_slots.py
│       ├── emails.py
│       ├── loggers.py
│       ├── logging_setup.py
│       └── send_notifs.py
├── Procfile
├── README.md
├── requirements.txt
└── templates
    ├── index.html
    └── thank_you.html
```

***

## Webpage
Upon running `main.py`, the home page will look like this - 

![Image of Yaktocat](https://github.com/darpan-jain/cowin_slots_notif-develop/static/images/result_form.png)

***

## Prerequisites
All the required dependencies can be installed by running the command `pip3 install -r requirements.txt`
***


***
