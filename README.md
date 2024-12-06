#Log-Script-Analysis

This submission contains a log analysis program that is written in Python and has the purpose to parse through server logs and accumulate some intelligence from them. The code will scan the log entries to determine which IP address has made how many requests, which sensors are the most requested ones, and whether there is a possibility of some security threats – strange behavior associated with multiple failed login attempts.

1. Request Analysis : It counts the some the request made from an individual IP address so as to enable you identify the users that make up the larger chunk of requests.  

2. Understanding User Access Patterns: It demonstrates the least, yet most accessed endpoints, which acts as an invaluable asset in determining the users and optimizing the server performance.  

3.Intrusion Prevention & Detection:These analyze redundant login sessions from particular source, recording the duration period in which a number of failed attempts is likely to exceed a limit, 
   showing potential invasion attempts.  

4. Features Output: There will also be a tabular representation of the analysis results using a format from the library ‘tabulate’ that enhances readability.  

5. Save analyzed data to CSV Format. Other attributes such as statistics on the requests, how active the endpoints were and the amount of malicious activity that likely took place will also be exported in a CSV format for future assessment and storage.
