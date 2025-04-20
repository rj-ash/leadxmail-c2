# Deployment Guide

## Prerequisites
- Ubuntu/Debian server (20.04 LTS or later recommended)
- Domain name (optional but recommended)
- SSH access to the server
- Sudo privileges

## Step 1: Server Setup

1. Connect to your server via SSH:
```bash
ssh username@your_server_ip
```

2. Clone your repository:
```bash
cd /var/www
git clone https://github.com/your_username/your_repo.git email_api
```

3. Make the deployment script executable:
```bash
chmod +x deploy.sh
```

## Step 2: Configuration

1. Update the Nginx configuration:
   - Edit `/etc/nginx/sites-available/email_api`
   - Replace `your_domain.com` with your actual domain name
   - If using IP address, replace with your server's IP

2. Update environment variables:
   - Create `.env` file in `/var/www/email_api`
   - Add your API keys and other configuration

## Step 3: Deployment

1. Run the deployment script:
```bash
./deploy.sh
```

2. Verify the installation:
```bash
# Check service status
sudo systemctl status email_api

# Check Nginx status
sudo systemctl status nginx

# Test the API
curl http://localhost:10000/health
```

## Step 4: SSL Configuration (Optional but Recommended)

1. Install Certbot:
```bash
sudo apt-get install -y certbot python3-certbot-nginx
```

2. Obtain SSL certificate:
```bash
sudo certbot --nginx -d your_domain.com
```

## Step 5: Monitoring and Maintenance

1. Check logs:
```bash
# Application logs
sudo journalctl -u email_api

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

2. Restart services if needed:
```bash
sudo systemctl restart email_api
sudo systemctl restart nginx
```

## Troubleshooting

1. If the service fails to start:
```bash
# Check service status
sudo systemctl status email_api

# Check logs
sudo journalctl -u email_api -n 50
```

2. If Nginx fails:
```bash
# Check Nginx configuration
sudo nginx -t

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

3. If the API is not responding:
```bash
# Check if the service is running
curl http://localhost:10000/health

# Check firewall settings
sudo ufw status
```

## Security Considerations

1. Update firewall rules:
```bash
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

2. Keep system updated:
```bash
sudo apt-get update
sudo apt-get upgrade
```

3. Regular backups:
```bash
# Backup application directory
tar -czf email_api_backup.tar.gz /var/www/email_api
``` 