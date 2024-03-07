# Palworld-Service
Application for managing Palworld server via flask app.
This has been tested to run on ubuntu server/ wsl.
The application must be ran in the same enviorment as the Palworld server.

Basic login information is:
user: admin
pass: admin

change your password after login on!

## systemd service dependant:
This app is depedant on setting up palworld with systemd services.
see this page for instructions.
You may skip to Step 25 if you understand what's being done.

https://pimylifeup.com/ubuntu-palworld-dedicated-server/



## Installation

```bash
sudo mkdir -p /home/app
sudo curl -LJO https://github.com/GiRx8/Palworld-Service/archive/refs/tags/latest.tar.gz
sudo tar -xzf Palworld-Service-latest.tar.gz -C /home/app --strip-components=1
cd /home/app
```

```bash
sudo chmod +x deploy.sh
./deploy.sh
```

## After installation progress
Please update your ip in the following file
```bash
sudo nano /etc/nginx/sites-available/PalService
```
```bash
server {
    listen 80;
    server_name your_ip or domain_here;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/app/pals/main/static;
    }

    location /media {
        alias /home/app/pals/main/media;
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```
## Useful commands

```bash
sudo systemctl status nginx 
sudo systemctl status gunicorn
sudo systemctl stop nginx
sudo systemctl start nginx 
sudo systemctl stop gunicorn
sudo systemctl start gunicorn
```
## Important information
In order for the application to start, stop, and restart the palworld services, the deployment script grants ubuntu steam user permission in the sudoer file to run them without password check (only 4 command permissions are being given to the steam user)

```bash
steam   ALL=(ALL) NOPASSWD: /bin/systemctl start palworld.service, /bin/systemctl stop palworld.service, /bin/systemctl restart palworld.service, /bin/systemctl is-active palworld.service
```

## Images
![alt text](https://i.postimg.cc/xfNT6K2W/palworld.png)
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.