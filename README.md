# Palworld-Service
Application for managing Palworld server via flask app.
This has been tested to run on ubuntu server/ wsl.
The application must be ran in the same enviorment as the Palworld server.

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