#!/bin/bash

# Update system packages
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
sudo apt-get install -y python3 python3-pip python3-venv

# Install Nginx
sudo apt-get install -y nginx

# Create application directory
sudo mkdir -p /var/www/email_api
sudo chown -R $USER:$USER /var/www/email_api

# Create and activate virtual environment
cd /var/www/email_api
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/email_api.service << EOF
[Unit]
Description=Email API Service
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/var/www/email_api
Environment="PATH=/var/www/email_api/venv/bin"
ExecStart=/var/www/email_api/venv/bin/gunicorn -c gunicorn_config.py app:asgi_app

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
sudo tee /etc/nginx/sites-available/email_api << EOF
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://localhost:10000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable Nginx configuration
sudo ln -s /etc/nginx/sites-available/email_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start and enable the service
sudo systemctl daemon-reload
sudo systemctl start email_api
sudo systemctl enable email_api

# Check service status
sudo systemctl status email_api 