#################################################
#TouchPoint Email Sanitizer
#
#This script is used to duplicate and email and sanitize it by removing/replacing email replacement codes so that functions as a standalone webpage.
#
#Features:
#- Replaces registerlink with standard format registration: https://YourChurch.tpsdb.com/OnlineReg/xxx
#- Replaces registerlink2 with standard format registration: https://YourChurch.tpsdb.com/OnlineReg/xxx?showamily=true'
#- Replaces rsvplink and regretslink with popup that says: "Please respond directly from email or contact church office"

#- Removes predefined sections of HTML (e.g. Manage Subscription button, {tracklinks} etc)
#- Sends sanitized email to user and makes it public
#- Finally redirects to the public viewemail link for the new email
#
#Written By: Heath Kouns
#Email: Heath@nrvhope.com
#################################################

# Import necessary modules
import re
import traceback
import urllib

# Set script title
model.Title = "Email Sanitizer"

def get_email_info(email_id):
    """Get organization info"""
    try:
        sql = '''Select Top 1 eq.Body, eq.Subject from EmailQueue eq
        where id = %s''' % email_id
        result = q.QuerySql(sql)
        
        if result:
            for item in result:
                return {"Body": item.Body, "Subject": item.Subject}
        
        return None
    except Exception as e:
        print "<div class='error'>Error getting email: " + str(e) + "</div>"
        return None

def replace_links(content):
    # Define the patterns and their replacements for links
    link_patterns = [
        (r'https://registerlink/\?org=(\d+)', r'https://nrvhope.tpsdb.com/OnlineReg/\1'),
        (r'https://registerlink2/\?org=(\d+)', r'https://nrvhope.tpsdb.com/OnlineReg/\1?showfamily=true')
    ]
    
    counts = {'registerlink': 0, 'registerlink2': 0, 'rsvplink': 0, 'regretslink': 0}
    
    # Apply each pattern replacement and count occurrences
    for i, (pattern, replacement) in enumerate(link_patterns):
        matches = re.findall(pattern, content)
        counts['registerlink' if i == 0 else 'registerlink2'] = len(matches)
        content = re.sub(pattern, replacement, content)
    
    # Handle rsvplink and regretslink
    response_patterns = [
        (r'href="(https://rsvplink/[^"]*)"', 'rsvplink'),
        (r'href="(https://regretslink/[^"]*)"', 'regretslink')
    ]
    
    for pattern, link_type in response_patterns:
        matches = re.findall(pattern, content)
        counts[link_type] = len(matches)
        
        for match in matches:
            replacement = '''href="#" onclick="alert('Please respond directly from email or contact church office'); return false;"'''
            content = content.replace('href="%s"' % match, replacement)
        
        # Add a note about responding directly
        content = re.sub(
            r'(<a[^>]*' + pattern + r'[^>]*>.*?</a>)',
            r'\1<br><small>(Please respond directly from email or contact church office)</small>',
            content
        )
    
    return content, counts
    
def remove_html_sections(content):
    # Define the sections to remove
    sections_to_remove = [
        r'<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 12px; line-height: 16.8px;">You are receiving this email because </span></p>\s*<p style="font-size: 14px; line-height: 140%;"><span style="font-size: 12px; line-height: 16.8px;">you are subscribed to the General Church Updates Mailing List.</span></p>\s*<p style="font-size: 14px; line-height: 140%;">&nbsp;</p>\s*<p style="line-height: 140%; font-size: 14px;"><span style="font-size: 12px; line-height: 16.8px;"><span style="line-height: 16.8px; font-size: 12px;">Manage your Subscriptions or </span>&lt;dropfromorg id="2"&gt;Unsubscribe&lt;/dropfromorg&gt;</span></p>',
        r'<a rel="noopener" href="https://nrvhope.tpsdb.com/OnlineReg/47" target="_blank"><span style="font-size: 12px; line-height: 16.8px;">Manage your Subscriptions</span></a>',
        r'{track}{tracklinks}'
    ]
    
    sections_removed = 0
    for section in sections_to_remove:
        new_content, count = re.subn(section, '', content, flags=re.DOTALL)
        if count > 0:
            content = new_content
            sections_removed += count
    
    return content, sections_removed

# CSS styles
styles = """
<style>
    .container {
        max-width: 1000px;
        margin: 0 auto;
        padding: 20px;
        font-family: Arial, sans-serif;
    }
    .form-group {
        margin-bottom: 15px;
    }
    label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
    }
    input[type="text"] {
        width: 20%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    button, .btn {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-right: 5px;
        text-decoration: none;
        display: inline-block;
    }
    button:hover, .btn:hover {
        background-color: #45a049;
    }
    .btn-secondary {
        background-color: #3498db;
    }
    .btn-secondary:hover {
        background-color: #2980b9;
    }
    .success {
        color: green;
        font-weight: bold;
    }
    .error {
        color: red;
        font-weight: bold;
    }
    .alert {
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid transparent;
        border-radius: 4px;
    }
    .alert-info {
        color: #31708f;
        background-color: #d9edf7;
        border-color: #bce8f1;
    }
    .alert-success {
        color: #3c763d;
        background-color: #dff0d8;
        border-color: #d6e9c6;
    }
    .action-cell {
        display: flex;
        gap: 5px;
    }
</style>

"""

# Main script
try:
    # Print CSS
    print styles
    
    # Get parameters
    email_id = model.Data.email_id
    new_email_body = ''
    new_email_subject = ''
    
    # Show base container
    print "<div class='container'>"
    
    print """<h1>Email Sanitizer  <svg xmlns="http://www.w3.org/2000/svg" 
	 width="25px" height="25px" viewBox="0 0 162.511 162.512"
	 xml:space="preserve">
<g>
	<path d="M76.404,72.669L0.009,23.012h152.78L76.404,72.669z M127.745,121.438c-13.146,0-25.386-7.052-31.926-18.401
		c-4.92-8.488-6.229-18.408-3.666-27.922c0.634-2.332,1.462-4.552,2.497-6.674L76.397,80.308L0,30.636v91.69h132.981l-0.676-1.182
		C130.783,121.334,129.266,121.438,127.745,121.438z M152.801,30.642l-26.592,17.287c0.481-0.015,0.944-0.094,1.432-0.094
		c9.462,0,18.413,3.689,25.16,9.961V30.642z M153.684,69.646c8.251,14.328,3.331,32.713-10.991,40.983
		c-14.334,8.264-32.723,3.35-40.992-10.99c-8.269-14.319-3.33-32.705,10.985-40.98C127.007,50.395,145.415,55.309,153.684,69.646z
		 M149.373,72.127c-6.887-11.953-22.231-16.062-34.19-9.173c-11.946,6.908-16.063,22.24-9.158,34.2
		c6.899,11.952,22.231,16.087,34.179,9.182C152.18,99.425,156.259,84.093,149.373,72.127z M150.244,108.766l-12.915,7.459
		l9.925,17.189l12.916-7.453L150.244,108.766z M161.515,128.318l-12.909,7.453c2.063,3.568,6.618,4.785,10.199,2.728
		C162.343,136.465,163.567,131.893,161.515,128.318z" fill="darkblue"/>
</g>
</svg></h1>"""
    
    # Show organization form
    print """
    <form id='orgForm' method='get' action=''>
        <div class='form-group'>
            <label for='email_id'>Email ID:</label>
            <input type='text' id='email_id' name='email_id' value='""" + (str(email_id) if email_id else "") + """' required>
        </div>
        <button type='submit' onclick='showLoading()'>Sanitize Email</button>
        
        
    </form>
    """
    
    print "<div id='loading' class='loading'>"
    #print "<div class='spinner'></div>"
    #print "<p>Loading attachments...</p>"
    print "</div>"
 
    if email_id:
        # Get organization info
        old_email = get_email_info(email_id)
        old_email_body= old_email["Body"] 
        
        if not old_email:
            print "<div class='error'>Error: Email ID " + str(email_id) + " not found.</div>"
        else:
            # Get attachments
            #attachments = get_org_attachments(email_id)
            
            old_email_body = old_email["Body"] 
            
            # First, replace links
            new_email_body, link_counts = replace_links(old_email_body)
            
            # Then, remove HTML sections
            new_email_body, sections_removed = remove_html_sections(new_email_body)


            new_email_subject = old_email["Subject"]
            
            
            QueuedBy = model.UserPeopleId   # People ID of record the email should be queued by
            MailToQuery = str(model.UserPeopleId) # 
            MailedFrom  = 'Admin@nrvhope.com' #
            MailedFromName  = model.UserName #
            model.Email(MailToQuery, QueuedBy, MailedFrom, MailedFromName, new_email_subject, new_email_body)
            
            
            
            
            
            try:
                sql = '''Select Top 1 eq.Id from EmailQueue eq
                        where eq.Subject = '%s'
                        And eq.FromName = '%s'
                        And eq.Queued > DATEADD(minute, -2, GETDATE())
                        order by Queued Desc''' % (new_email_subject, MailedFromName )
                #print sql
                
                result = q.QuerySql(sql)
                
                if result:
                    for item in result:
                        print "<div class='alert alert-info'>"
                        print "<p>Changes made to the email:</p>"
                        print "<ul>"
                        print "<li>registerlink replacements: %d</li>" % link_counts['registerlink']
                        print "<li>registerlink2 replacements: %d</li>" % link_counts['registerlink2']
                        print "<li>rsvplink modifications: %d</li>" % link_counts['rsvplink']
                        print "<li>regretslink modifications: %d</li>" % link_counts['regretslink']
                        print "<li>HTML sections removed: %d</li>" % sections_removed
                        print "</ul>"
                        print "</div>"
                        print 'New Email created with ID:' + str(item.Id) +'</br>'
                        print '<i>Click button below to get URL for new Email</i> </br>'
                        
                        make_public_button = '''
                        <a href="https://nrvhope.tpsdb.com/Manage/Emails/MakePublic/%s" class="btn btn-secondary">Make Public</a>
                        ''' % str(item.Id)
                        print make_public_button
                                        
                
            except Exception as e:
                print "<div class='error'>Error getting email ID: " + str(e) + "</div>"
    
    # Close container
    print "</div>"
     
except Exception as e:
    # Print any errors
    import traceback
    print "<h2>Error</h2>"
    print "<p>An error occurred: " + str(e) + "</p>"
    print "<pre>"
    traceback.print_exc()
    print "</pre>"