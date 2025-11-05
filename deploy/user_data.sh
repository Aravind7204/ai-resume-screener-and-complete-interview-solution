#!/bin/bash
# AWS EC2 User Data Script for AI Resume Screener
# This script runs when the EC2 instance starts

# Update system
yum update -y

# Install Python 3.9 and required packages
yum install -y python3 python3-pip git htop

# Install Git LFS for large model files
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | bash
yum install -y git-lfs
git lfs install

# Create application directory
mkdir -p /opt/ai-resume-screener
cd /opt/ai-resume-screener

# Clone the repository
git clone https://github.com/Aravind7204/ai-resume-screener-and-complete-interview-solution.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -c "
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('stopwords')
nltk.download('punkt')
"

# Create necessary directories
mkdir -p uploads
mkdir -p logs

# Set up environment variables
cat > .env << EOF
SECRET_KEY=$(openssl rand -base64 32)
SECURITY_PASSWORD_SALT=$(openssl rand -base64 32)
FLASK_ENV=production
HOST=0.0.0.0
PORT=8000
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=
DATABASE_URL=sqlite:///database.db
UPLOAD_FOLDER=uploads
EOF

# Set permissions
chown -R ec2-user:ec2-user /opt/ai-resume-screener
chmod +x app.py

# Create systemd service
cat > /etc/systemd/system/ai-resume-screener.service << EOF
[Unit]
Description=AI Resume Screener Flask App
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/opt/ai-resume-screener
Environment=PATH=/opt/ai-resume-screener/venv/bin
ExecStart=/opt/ai-resume-screener/venv/bin/gunicorn --bind 0.0.0.0:8000 --workers 2 --timeout 300 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start and enable the service
systemctl daemon-reload
systemctl enable ai-resume-screener
systemctl start ai-resume-screener

# Install and configure nginx as reverse proxy
yum install -y nginx

cat > /etc/nginx/conf.d/ai-resume-screener.conf << EOF
server {
    listen 80;
    server_name _;
    
    client_max_body_size 20M;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
EOF

# Start nginx
systemctl enable nginx
systemctl start nginx

echo "AI Resume Screener deployment completed!"
echo "Application should be accessible on port 80"
