# This custom script is designed to take a data export from PowerSchool and import it into Google.
# Created by J. Romani  - jromani@ccsd989.org - 630-254-0923
#
#

# Global arguments use Python 3
import csv
from datetime import datetime
import subprocess
import logging
import smtplib
from os import rename
import os.path as op
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
import subprocess
from subprocess import run, PIPE


# Configure the logging of this application
# logging.basicConfig(filename="Student_Import.log", level = logging.DEBUG,
#     format = "%(asctime)s %(levelname)s %(message)s"
#      )
logging.basicConfig(filename="Student_Import.log", level = logging.DEBUG,
    format = "%(asctime)s %(message)s"
     )


#Static Data for testing purposes.
#exitdate =  '2/21/18'
#entrydate = '2/15/18'
now = datetime.now()

#testing date is 2/15/18 works with Sample StudentAccounts9.csv file
#today = '2/15/18'
today = now.strftime('%-m/%-d/%y')
plainday = now.strftime('%m%d%y')

# File import funcation
# Pull the csv file from the local server
#datafile = '/Users/admin/bin/gam/StudentAccounts9.csv'
datafile = '/Users/admin/bin/gam/StudentAccounts.csv'

fieldnames = ['enroll_status', 'schoolid', 'last_name', 'first_name', 'grade_level', 'studentid', 'student_password', 'student_email', 'home_room', 'entrydate', 'exitdate', 'bus_1', 'bus_2', 'bus_trans_am', 'bus_trans_pm']
input_file = csv.DictReader(open(datafile), fieldnames=fieldnames)

# Pulls date for comparision
today_date = today
for row in input_file:


    # Define vaiblaes to hold data from file
    enroll_status = row["enroll_status"]
    schoolid = row["schoolid"]
    last_name =row["last_name"]
    first_name = row["first_name"]
    grade_level =row["grade_level"]
    studentid = row["studentid"]
    student_password = row["student_password"]
    student_email = row["student_email"]
    home_room = row["home_room"]
    entrydate = row["entrydate"]
    exitdate = row["exitdate"]
    bus_1 = row["bus_1"]
    bus_2 = row["bus_2"]
    bus_trans_am = row["bus_trans_am"]
    bus_trans_pm = row["bus_trans_pm"]
    name = row["first_name"] +" "+ row["last_name"]


    if schoolid == '9': # Out of District Assignement
        # Show this info until there is a confrimation message created at the end.
        print (last_name, student_email, "attends out of district - ", schoolid)
        logging.debug("- Out of district: %s, %s %s %s", last_name, first_name, studentid, schoolid)
        # No gam command needed to add student
        # No gam command needed to add studnet to print group

#def compareExitDate(exitdate, today):
# Need to pass more varibles for this funcation to work as a funcation

# This section looks at the student's exit date and compares it to today's date.
# If the date is a match the student account is suspended automatically.
# If the dates do not match, then the logic is to examine entry date.

#    print ("Exit Date: ", exitdate)
#    print ("Today's Date: ", today_date)
    elif exitdate == today_date:
        # gam command to suspend student account
        args = ['./gam', 'update', 'user', student_email, 'org', "/xxx_Suspended" ]
        p = run(args, stdout=subprocess.PIPE, close_fds=True)
        print(p.returncode)
        print(p.stdout)

        #print ("Exit Date is Today")
        # Prints to console
        print (last_name, student_email, " This Student account is suspended.")
        # Sends to a log file
        logging.debug("- Suspended Account - %s, %s %s Exit Date: %s", last_name, first_name, student_email, exitdate)

    # enter goto command to look at entry date?

#def compareEntryDate(entrydate, today):
# This looks at the student's entry date and compares it to today's date.
# if the date is a match the student account is created

#    print ("Entry Date: ", entrydate)
#    print ("Today's Date: ", today_date)
    elif entrydate == today_date:
        #print ("Entry Date is Today")
        # Arbor View Assignement
        if schoolid == '1':
            # gam command to add student to Arbor View OU
            args = ['./gam', 'create', 'user', student_email, 'firstname', first_name, 'lastname', last_name, 'password', student_password, 'org', "/Arbor View/Students", 'changepassword',  'off' ]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            # gam command to add student to Arbor View Printer group
            args = ['./gam', 'update', 'group', 'avprint', 'add', student_email]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            #logs that the account was created
            print (last_name, student_email, "added to Arbor View OU - ", schoolid)
            logging.debug("- Added %s, %s to Arbor View OU %s Entry Date: %s Homeroom: %s Bus_1: %s Bus_2: %s AM Transfer: %s PM Transfer %s", last_name, first_name, student_email, entrydate, home_room, bus_1, bus_2, bus_trans_am, bus_trans_pm)

        elif schoolid == '2':  # Briar Glen Assignement
            # gam command to add student to Briar Glen OU
            args = ['./gam', 'create', 'user', student_email, 'firstname', first_name, 'lastname', last_name, 'password', student_password, 'org', "/Briar Glen/Students", 'changepassword',  'off' ]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            # gam command to add student to Briar Glen Printer group
            args = ['./gam', 'update', 'group', 'bgprint', 'add', student_email]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            #logs that the account was created
            print (last_name, student_email, "added to Briar Glen OU - ", schoolid)
            logging.debug("- Added %s, %s to Briar Glen OU %s Entry Date: %s Homeroom: %s Bus_1: %s Bus_2: %s AM Transfer: %s PM Transfer %s", last_name, first_name, student_email, entrydate, home_room, bus_1, bus_2, bus_trans_am, bus_trans_pm)


        elif schoolid == '3': # Park View Assignement

            # gam command to add student to Parkview OU
            args = ['./gam', 'create', 'user', student_email, 'firstname', first_name, 'lastname', last_name, 'password', student_password, 'org', "/Park View/Students", 'changepassword',  'off' ]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            # gam command to add student to Parkview Printer group
            args = ['./gam', 'update', 'group', 'pvprint', 'add', student_email]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            #logs that the account was created
            print (last_name, student_email, "added to Park View OU - ", schoolid)
            logging.debug("- Added %s, %s to Park View OU %s Entry Date: %s Homeroom: %s Bus_1: %s Bus_2: %s AM Transfer: %s PM Transfer %s", last_name, first_name, student_email, entrydate, home_room, bus_1, bus_2, bus_trans_am, bus_trans_pm)


        elif schoolid == '4':   # Westfield Assignement
            # gam command to add student to Westfield OU
            args = ['./gam', 'create', 'user', student_email, 'firstname', first_name, 'lastname', last_name, 'password', student_password, 'org', "/Westfield/Students", 'changepassword',  'off' ]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            # gam command to add student to Westfield Printer group
            args = ['./gam', 'update', 'group', 'wfprint', 'add', student_email]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            #logs that the account was created
            print (last_name, student_email, "added to Westfield OU - ", schoolid)
            logging.debug("- Added %s, %s to Westfield OU %s Entry Date: %s Homeroom: %s Bus_1: %s Bus_2: %s AM Transfer: %s PM Transfer %s", last_name, first_name, student_email, entrydate, home_room, bus_1, bus_2, bus_trans_am, bus_trans_pm)

        elif schoolid == '6':  # Glen Crest Assignement
            # gam command to add student to Glen Crest OU
            args = ['./gam', 'create', 'user', student_email, 'firstname', first_name, 'lastname', last_name, 'password', student_password, 'org', "/Glen Crest/Students", 'changepassword',  'off' ]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            # gam command to add student to Glen Crest Printer group
            args = ['./gam', 'update', 'group', 'gcprint', 'add', student_email]
            p = run(args, stdout=subprocess.PIPE, close_fds=True)
            print(p.returncode)
            print(p.stdout)

            #logs that the account was created.
            print (last_name, student_email, "added to Glen Crest OU - ", schoolid)
            logging.debug("- Added %s, %s to Glen Crest OU %s Entry Date: %s Homeroom: %s Bus_1: %s Bus_2: %s AM Transfer: %s PM Transfer %s", last_name, first_name, student_email, entrydate, home_room, bus_1, bus_2, bus_trans_am, bus_trans_pm)


#email log file email via internal relay server
server = smtplib.SMTP('10.7.47.202', 25)
EMAIL_FROM = "log@ccsd89.org"
#EMAIL_TO = "jromani@ccsd89.org"
EMAIL_TO = "sos@ccsd89.org"
SUBJECT = "Students Added/Suspended in CCSD89.me"

fp =open("/Users/admin/bin/gam/Student_Import.log", "r")
body = MIMEText(fp.read())
fp.close()

msg =  MIMEMultipart()

msg['Subject'] = SUBJECT
msg['From'] = EMAIL_FROM
msg['To'] = EMAIL_TO

part = MIMEBase('application', "octet-stream")
part.set_payload(open("/Users/admin/bin/gam/Student_Import.log", "rb").read())

part.add_header('Content-Disposition', 'attachment; filename="Student_Import.log"')

msg.attach(body)
msg.attach(part)

server.sendmail(EMAIL_FROM, EMAIL_TO,  msg.as_string())


#   rename log file with today's date in the new name
new_name = "Student_Import"+plainday+".log"
rename("Student_Import.log", new_name)

#def main():

#    compareExitDate(exitdate, today)
#    compareEntryDate(entrydate, today)

#main ()
