# Student Import 

The Student_Import.py is the script that automatically create or suspend student accounts from a CSV into Google Apps for Ed

This script utilizes Python 3.6 and GAM for google apps (https://github.com/jay0lee/GAM).

It looks at a csv file exported at 4:00 AM from PowerSchool to determine if there are new accounts created or suspended accounts for students no long with us.

Features are specific to the way PowerSchool is configured for our district.  We also utilize custom data fields which are reflected in this script.

This script runs on Mac OS, but could be modified to run on Linux or Windows.

The org.ccsd89.studentimport.plist file is excutes the script evry day at 4:45 and needs to go into the /Users/Username/Libray/LaunchAgents folder - this user MUST be logged in for this execution to occur.

The stuImport.sh is the file that the plist calls to run the Python script. 

studentAccounts9.csv is a sample file with fictional data used to test out the import.

Use this application/script at your own risk.


# Next Steps: 
Add modules for comparing data from yesterday to today to determine if a student was transfered between buildings
If a student is transfered, then move them to the correct new organizational unit within google, remove them fron the printer group and add them to the correct building printer group.
