# ADtools

usage : `python3 tool.py config.txt`

Done :
  - connecting to all machines using SSH
  - Listing running services
  - locating usage of php and python dangerous functions
  - uploading and running a script that terminates any reverse shell

To Be Done :
  - locating multiple web roots using apache,ngnix,...etc config files
  - uploading and running snoopy to monitor the processes running on the machines 
  - uploading and running a network logger to detect potential attacks and perform replay attacks
  - implementing a site-wide defence against potential attacks on web services using middlewares,htaccess,...etc (for example see /kick/.htaccess)
  - detecting misconfigurations and hardcoded credentials
    
To Be Improved :
  - code readability
  - output format
  - detecting reverse shells in a better way
  - detecting dangerous functions in a better way and for more languages
