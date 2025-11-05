# AWS EC2 Deployment Guide for AI Resume Screener

## Prerequisites
- AWS Account with Free Tier access
- Basic knowledge of AWS Console

## Step 1: Launch EC2 Instance

### 1.1 Go to EC2 Dashboard
- Login to AWS Console
- Navigate to EC2 service
- Click "Launch Instance"

### 1.2 Configure Instance
```
Name: ai-resume-screener
AMI: Amazon Linux 2023 AMI (Free Tier eligible)
Instance Type: t2.micro (Free Tier eligible)
Key Pair: Create new or use existing
```

### 1.3 Configure Security Group
Create a new security group with these rules:
```
Type        Protocol    Port Range    Source
SSH         TCP         22           Your IP
HTTP        TCP         80           0.0.0.0/0
Custom TCP  TCP         8000         0.0.0.0/0
```

### 1.4 Configure Storage
```
Root Volume: 30 GB gp3 (Free Tier eligible)
```

### 1.5 Advanced Details
Copy the content from `user_data.sh` into the "User data" field.

## Step 2: Launch and Configure

### 2.1 Launch Instance
- Review settings
- Click "Launch Instance"
- Wait for instance to be in "running" state

### 2.2 Get Public IP
- Note down the Public IPv4 address
- This will be your application URL

## Step 3: Post-Deployment Configuration

### 3.1 SSH into Instance (if needed)
```bash
ssh -i your-key.pem ec2-user@your-public-ip
```

### 3.2 Check Application Status
```bash
sudo systemctl status ai-resume-screener
sudo systemctl status nginx
```

### 3.3 View Logs
```bash
sudo journalctl -u ai-resume-screener -f
```

### 3.4 Configure Environment Variables
```bash
cd /opt/ai-resume-screener
sudo nano .env
```

Add your actual email credentials:
```
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

Restart the service:
```bash
sudo systemctl restart ai-resume-screener
```

## Step 4: Access Your Application

Visit: `http://your-public-ip`

## Step 5: Optional - Set up Domain Name

### 5.1 Route 53 (if you have a domain)
- Create hosted zone
- Add A record pointing to your EC2 public IP

### 5.2 SSL Certificate (Let's Encrypt)
```bash
sudo yum install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Troubleshooting

### Application not starting
```bash
# Check logs
sudo journalctl -u ai-resume-screener -n 50

# Check if port is listening
sudo netstat -tlnp | grep 8000

# Restart service
sudo systemctl restart ai-resume-screener
```

### Large model loading issues
```bash
# Check disk space
df -h

# Check memory usage
free -h

# Monitor during startup
htop
```

### Email not working
- Ensure Gmail App Password is correct
- Check firewall settings
- Verify SMTP settings

## Cost Monitoring

### Free Tier Limits
- EC2: 750 hours/month (t2.micro)
- EBS: 30 GB storage
- Data Transfer: 15 GB/month

### Monitor Usage
- Set up billing alerts
- Check AWS Cost Explorer regularly

## Security Best Practices

1. **Regular Updates**
   ```bash
   sudo yum update -y
   ```

2. **Firewall Configuration**
   - Only open necessary ports
   - Restrict SSH access to your IP

3. **Environment Variables**
   - Never commit secrets to Git
   - Use strong passwords

4. **Backup Strategy**
   - Regular EBS snapshots
   - Database backups

## Performance Optimization

1. **Enable Swap** (for t2.micro)
   ```bash
   sudo dd if=/dev/zero of=/swapfile bs=1M count=1024
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab
   ```

2. **Optimize Gunicorn**
   ```bash
   # Edit service file
   sudo nano /etc/systemd/system/ai-resume-screener.service
   
   # Adjust workers based on CPU
   ExecStart=/opt/ai-resume-screener/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 1 --timeout 300 --max-requests 1000 app:app
   ```

3. **Monitor Resources**
   ```bash
   # Install monitoring tools
   sudo yum install -y htop iotop
   ```
