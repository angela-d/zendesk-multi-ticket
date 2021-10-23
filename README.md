# Zendesk Form to Multiple Tickets
Ticket generator to delegate IT tasks by opening multiple simultaneous, customized tickets from a single form (based on content or "category" from the ticket submitter).

Example form is an IT onboarding request for a new hire at an organization.

Each member of IT has a separate ticket generated, specifically for what they need to do.

## Setup
This script uses Zendesk API tokens.

Modify the following to suit your agent/token (in **new.py**):
```python
# api config
headers = {'content-type': 'application/json'}
user = 'myagent@example.com/token'
api_token = '2zFD893XpPWQFhj235FyHV5WpNGpTcdDFKk65n'
url = 'https://example.zendesk.com/api/v2/requests.json'
```

For the agent(s) you want to pre-assign (this is currently non-functional but not in a breaking state, cc is working -- see 'Known Bugs' section.):
```python
# agent id
phone_agent = '001'
tech_trainer = '002'
admin_agent = '003'
email_agent = '004'
computer_agent = '005'
```

- First, install dependencies to the server.  My OS of choice is Debian-based Linux, which uses the apt package manager.
```bash
apt install python3-bottle nginx
```

- Make a directory for your form, for example:
  ```bash
  /var/www/employee-forms
  ```

- Go into the directory on the remote server where the application is kept, install Python dependencies:
  - :warning: Do not use pip under sudo/root! *Standard user only!* -- it should be the user you want your Python server to run as (also, **should not be root**)
  ```bash
  cd /var/www/employee-forms
  pip3 install -r requirements.txt
  ```



  > It's worth noting that Pip isn't a package manager like apt.  These packages need to be *manually* updated, so a means to watch for security updates.
  >
  > Pip packages also aren't subject to being signed packages.  So it's not difficult at all for someone to get a hold of a package developer's credentials and upload an update  ([Has happened to Python, too](https://www.zdnet.com/article/malicious-python-libraries-targeting-linux-servers-removed-from-pypi/))


- Create a service for the application; this is necessary as Python is not a "web language," so it requires a server overlay to execute stuff for web-facing stuff like webpages.  This will launch the script that loads the server. (You can load modules to run Python through Nginx or Apache, optionally)
```bash
pico /etc/systemd/system/newemployee.service
```

  - Populate with the following
    ```bash
    [Unit]
    Description=New Employee Form
    After=network.target

    [Service]
    User=YOUR_USER ### dont use root...
    ExecStart=/var/www/employee-forms/new.py
    WorkingDirectory=/var/www/employee-forms/
    Restart=on-failure
    RemainAfterExit=yes

    [Install]
    WantedBy=multi-user.target
    ```

- Test it
  ```bash
  systemctl service newemployee start
  ```

- Create a startup service (after server reboot, it will be auto-started):
```bash
systemctl enable newemployee
```

### How does the Python server work?
Note the following from the systemd unit file:
```bash
ExecStart=/var/www/employee-forms/new.py
```
Open that file:
```bash
pico /var/www/employee-forms/new.py
```

This is what speaks to nginx:
```python
run(server='paste', host='localhost', port=8081, debug=True)
```
Note that the port can be anything; 8080 was already in use (for me), so I simply incremented to the next available port.

To change from dev to prod, change:
```python
run(server='paste', host='localhost', port=8081, debug=True)
```

to:
```python
run(server='paste', host='localhost', port=8081, debug=False)
```


## On an Nginx-based system - Virtualhost Setup
The following assumes you already have DNS pointed at the server for your subdomain.

Virtualhost config for Nginx lives in `/etc/nginx`
Copy a pre-configured virtualhost, to save time

*(All of) the following steps are technically not required with Nginx (in this manner), but to keep similarity between Nginx and Apache systems, I keep the sites-available/sites-enabled setup.*

- **Port 80/non-SSL (direct URL types)**
  ```bash
  cp /etc/nginx/sites-available/existing_site.conf /etc/nginx/sites-available/newemployee.conf
  ```

- Symlink it to sites-enabled (this is the only step you'd have to do if you didn't care about Apache synchronicity) -- to break Apache-like behavior, bypass *sites-available* & use *sites-enabled*, only.
  ```bash
  ln -s /etc/nginx/sites-available/newemployee.conf /etc/nginx/sites-enabled/newemployee.conf
  ```

  - Contents of *newemployee*:
    ```bash
    server {
        listen 80;

        server_name newemployee.example.com;
        client_max_body_size 25m;

        location / {
            return 301 https://newemployee.example.com/create_ticket;
        }
    }
    ```

- **Port 443/SSL (destination)**
  ```bash
  cp /etc/nginx/sites-available/existing-site-ssl.conf /etc/nginx/sites-available/newemployee-ssl.conf
  ```
- Symlink it to sites-enabled
  ```bash
  ln -s /etc/nginx/sites-available/newemployee-ssl.conf /etc/nginx/sites-enabled/newemployee-ssl.conf
  ```

  - Contents of *newemployee-ssl.conf* (note the proxy_pass field):
    ```bash
    server {
        listen 443;
        ssl on;
        server_name newmployee.example.com;
        root /var/www/employee-forms/;
        index new.py;
        ssl_certificate /path/to/your/cert.pem;
        ssl_certificate_key /path/to/your/key.pem;
        client_max_body_size 25m;

        location / {
            proxy_pass http://127.0.0.1:8081;
            proxy_set_header X-Forwarded-Host $server_name;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-Proto $scheme;
            add_header P3P 'CP="ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV"';
        }
    }
    ```

## Breakdown
***

- Form fields (template) are housed under `/var/www/employee-forms/views/ticket_form.tpl`
  - Plain html, javascript just to prevent double-submissions
- CSS/images/font are shared with the new employee form, at `/var/www/employee-forms/static/inc`
  - Note that the woff files are an embedded font that load from the stylesheet (see the .css file); I used a public-domain font
    - This bypasses the need of loading third party junk like Google fonts (aka Google tracking through website assets)

Server details:
- The Python server runs under the `YOUR_USER` user environment (customize to suit!)
- This form was developed for and hosted on a restricted intranet IP only accessible to trusted users and is not accessible from the public web; so you should pentest before using this publicly!

Script details:
- The `new.py` script loads a third-party pip package, [paste](https://paste.readthedocs.io/en/latest/) which you can see from the .py script that it governs the server for the script to execute.  Updates are governed by pip and are done manually.
- [bottle](https://bottlepy.org/docs/dev/) runs the templating, but comes from Debian's repos and is maintained by apt


## Extending
You can have multiple servers/forms using the same assets and space.
- Duplicate `new.py` and `views/ticket_form.tpl` (adjust ticket_form.tpl call in new.py copy, appropriately)
- Modify newcopy.py and +1 the paste port
- Create systemd services pointed at your new newcopy.py script
- Create an nginx virtualhost for your new path

### Known Bugs
Pre-assigning tickets to agents does not work.  There appears to be some joining of APIs that has to be done to pull the agent IDs successfully (so they're recognized by the right API), since it's more of an annoyance that a blockage, it's a low priority fix.

Auto-adding of an agent to the ticket's CC is working.

### Credits
- Example company logo in the template from [DesignContest](https://iconarchive.com/show/ecommerce-business-icons-by-designcontest/company-building-icon.html)
- Default motherboard background by [Athena](https://www.pexels.com/photo/black-and-gray-motherboard-2582937/)
- Default font [Istok](https://www.fontsquirrel.com/fonts/istok) by Andrey V. Panov
