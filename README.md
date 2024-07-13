# (Let's Hunt)
This DNS information gathering tool, designed with a user-friendly GUI in Tkinter, allows users to input a domain name and retrieve detailed data including IP Address, DNS Records, Server Details, WHOIS info, Subdomains, and Open Ports. The tool features a progress bar to providing visual feedback during data fetching operations.

## Features
- **IP Address Retrieval:** 
Fetches and displays the IP address associated with the specified domain.

- **DNS Records Retrieval:**
Retrieves and displays DNS records including A, AAAA, CNAME, MX, and TXT records.

- **Server Details:**
  Displays detailed information about the web server and operating system.
  Lists HTTP headers associated with the domain.

- **WHOIS Information:**
Retrieves and displays WHOIS data including registration details and contact information.

- **Subdomain Enumeration:**
Enumerates and displays subdomains along with their associated IP addresses.

- **Port Scanning:**
Performs a port scan on the domain and displays open ports.

## Graphical User Interface
- Easy-to-use GUI built with Tkinter.
- Scrolled text widgets for displaying detailed results.
- Progress bar to indicate ongoing data fetching.
- Clear separation of different data types for easy readability.

## Requirements
- pip install dnspython requests python-whois
- Python 3.x
- Tkinter (comes pre-installed with standard Python installations)
- Custom LetsHunt.py module with necessary functions
- update and upgrade your system if it isn't already

 ## Installation
1. **Clone the repository:**
  ```bash
   git clone  --ADD LINK--
```
2. **Go to Directory:**
  ```bash
  cd --write project Directory name-- 
```

3. **Install the required packages:**
  ```bash
  pip install dnspython requests python-whois 
   ```
 **To Run CLI**
 <br>
 `run command:`
  ```bash
 python3 LetsHunt.py
```
 **To Run GUI**
 <br>
`run command:`
   ```bash
   python3 gui.py
```

You can use both commands one by one to experience the CLI and GUI versions of the tool.
<br>
I am not an expert in Python programming, but I've made an effort to create a GUI for my tool. In the future, I plan to enhance this tool by adding more features and improving the user experience. My goal is to create a more sophisticated and user-friendly GUI as I continue to develop my skills and the functionality of this project.

<br>

**Enter the target domain in the input field**
<br>
    ` e.g: google.com `
    
<br>

Click the "Start Hunt" button to begin gathering information.
<br>
View the fetched information in the respective sections.
