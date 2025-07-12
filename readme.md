# What does it do and why
This script scrapes [next-episode.net](https://next-episode.net/) and [promiedos.com.ar](https://www.promiedos.com.ar/) according to the config.json file to find the upcoming episodes and matches that interests you. Once found, they are uploaded to a db.


I created it so I don't miss my favorite shows and sporting events.
# How to use
Modify the config.json file according to your preferences and run the main.py file. You'll also need to replace the connection string on events_db.py and create a database to host the data.


The program may take some seconds to scrape the sites, after which it will close automatically.


The program doesn't take any extra arguments.
# How should you use it
I use (and would recommend using) Windows Task Scheduler to run it periodically and automatically.

# System
Tested on Windows 11. Should also work on Windows 10. Not sure about older versions of Windows or different OS.

The libraries used include pathlib, sys, datetime, json, sqlalchemy, bs4, requests and logging.