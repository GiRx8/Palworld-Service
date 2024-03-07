#!/bin/bash

# Step 1: Install Nginx
echo "Installing Nginx..."
sudo apt update
sudo apt install -y nginx

# Step 2: Configure Nginx
echo "Configuring Nginx..."
cat <<'EOF' | sudo tee /etc/nginx/sites-available/PalService > /dev/null

server {
    listen 80;
    server_name 192.168.33.78;

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
EOF

# Step 3: Enable site
sudo ln -s /etc/nginx/sites-available/PalService /etc/nginx/sites-enabled

# Step 4: Enable and Start Services
echo "Enabling and starting services..."
sudo systemctl enable nginx
sudo systemctl start nginx

# Step 5: Install Python venv
echo "Installing Python 3.10-venv..."
sudo apt install -y python3.10-venv

# Step 6: Configure Firewall
echo "Configuring firewall..."
sudo ufw allow 80
#sudo ufw enable

# Step 7: Add new line to sudoers using visudo
echo "Adding a new line to sudoers..."
echo "steam   ALL=(ALL) NOPASSWD: /bin/systemctl start palworld.service, /bin/systemctl stop palworld.service, /bin/systemctl restart palworld.service, /bin/systemctl is-active palworld.service" | sudo tee -a /etc/sudoers

# Step 8: Set up Python virtual environment
echo "Setting up Python virtual environment..."
cd /home/app/pals
sudo python3 -m venv venv
sudo chown -R $USER:$USER venv
source venv/bin/activate

# Step 9: install gunicorn
echo "Installing Gunicorn..."
pip install gunicorn

# Step 10: Configure Gunicorn
echo "Configuring Gunicorn..."
cat <<EOF | sudo tee /etc/systemd/system/gunicorn.service > /dev/null

[Unit]
Description=Gunicorn instance to serve your Flask application
After=network.target

[Service]
User=steam
Group=steam
WorkingDirectory=/home/app/pals
Environment="PATH=/home/app/pals/venv/bin"
ExecStart=/home/app/pals/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 main:create_app()

[Install]
WantedBy=multi-user.target
EOF

# Step 11: Enable and Start Services
echo "Enabling and starting services..."
sudo systemctl enable gunicorn
sudo systemctl start gunicorn

# Step 12: Install Flask and other dependencies
echo "Installing Flask and dependencies..."
pip install -r requirements.txt

# Step 13: Deactivate virtual environment
deactivate

# Step 14: Grant steam user permissions
echo "Grant steam user folder permission..."
sudo chown -R steam:steam /home/app

# Step 15: Restart services
echo "Restarting nginx and gunicorn..."
sudo systemctl restart nginx
sudo systemctl restart gunicorn

echo "Deployment completed!"
