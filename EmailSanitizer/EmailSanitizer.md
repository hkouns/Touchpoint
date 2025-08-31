###  [Email Sanitizer]
This script is used to duplicate and email and sanitize it by removing/replacing email replacement codes so that functions as a standalone webpage.

- ⚙️ **Implementation Level: Easy
- 🧩 **Installation: This is a paste-and-go Python script, with the only configuration needed to schedule it to run.

#
#Features:
#- Replaces registerlink with standard format registration: https://YourChurch.tpsdb.com/OnlineReg/xxx
#- Replaces registerlink2 with standard format registration: https://YourChurch.tpsdb.com/OnlineReg/xxx?showamily=true'
#- Replaces rsvplink and regretslink with popup that says: "Please respond directly from email or contact church office"

#- Removes predefined sections of HTML (e.g. Manage Subscription button, {tracklinks} etc)
#- Sends sanitized email to user and makes it public
#- Finally redirects to the public viewemail link for the new email
