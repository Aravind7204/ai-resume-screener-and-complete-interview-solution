# AI Resume Screener & Complete Interview Solution

A comprehensive Flask-based web application that uses AI to screen resumes, conduct ATS analysis, and manage interview processes.

## 🚀 Features

- **Resume Analysis**: AI-powered resume screening and classification
- **ATS Score Calculation**: Automated applicant tracking system scoring
- **Interview Management**: Schedule and conduct virtual interviews
- **User Management**: Separate dashboards for HR and candidates
- **Email Integration**: Automated notifications and communications
- **Gemini AI Integration**: Advanced resume analysis and suggestions

## 🛠 Technology Stack

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **AI/ML**: Sentence Transformers, Scikit-learn, Google Gemini AI
- **Deployment**: AWS EC2, Nginx, Gunicorn
- **Storage**: Git LFS for large model files

## 📋 Prerequisites

- Python 3.8+
- Git with Git LFS
- Gmail account with App Password (for email features)
- Google Gemini AI API key
- AWS Account (for deployment)

## 🔧 Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Aravind7204/ai-resume-screener-and-complete-interview-solution.git
   cd ai-resume-screener-and-complete-interview-solution
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

5. **Download NLTK data**
   ```python
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt')
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

## ☁️ AWS Deployment

### Quick Deploy (Automated)

1. **Launch EC2 Instance**
   - Use Amazon Linux 2023 AMI
   - Instance type: t2.micro (Free Tier)
   - Copy content from `deploy/user_data.sh` to User Data field

2. **Configure Security Group**
   ```
   SSH (22) - Your IP
   HTTP (80) - 0.0.0.0/0
   Custom TCP (8000) - 0.0.0.0/0
   ```

3. **Access Application**
   - Visit: `http://your-ec2-public-ip`

### Manual Deploy

Follow the detailed guide in `deploy/aws_setup.md`

## 🔐 Environment Variables

Create a `.env` file with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-flask-key-here
SECURITY_PASSWORD_SALT=your-security-password-salt-here
FLASK_ENV=production

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password-here

# Google Gemini AI
GOOGLE_API_KEY=your-gemini-api-key-here
```

## 📁 Project Structure

```
ai-resume-screener/
├── app.py                 # AWS entry point
├── run.py                 # Main Flask application
├── model_loader.py        # Optimized ML model loading
├── gunicorn_config.py     # Production server configuration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── backend/
│   ├── models/           # ML models and encoders
│   └── api.py           # API endpoints
├── frontend/
│   ├── templates/       # HTML templates
│   └── static/         # CSS, JS, images
├── deploy/
│   ├── user_data.sh    # EC2 deployment script
│   └── aws_setup.md    # Detailed deployment guide
└── uploads/            # Resume file uploads
```

## 🎯 Key Features Explained

### Resume Analysis
- Extracts text from PDF and DOCX files
- Calculates ATS compatibility scores
- Provides improvement suggestions
- Classifies resumes by job categories

### Interview Management
- Schedule interviews with candidates
- Automated email notifications
- Interview status tracking
- Candidate and HR dashboards

### AI Integration
- Sentence transformers for semantic analysis
- Google Gemini AI for advanced insights
- Spell checking and grammar analysis
- Keyword density optimization

## 🔧 Performance Optimization

### For AWS t2.micro
- Optimized model loading with caching
- Gunicorn configuration for low memory
- Nginx reverse proxy for better performance
- Swap file configuration for memory management

### Model Loading
- Singleton pattern for model instances
- Lazy loading for heavy models
- Memory-efficient caching
- Graceful error handling

## 📊 Monitoring & Logs

### Application Logs
```bash
sudo journalctl -u ai-resume-screener -f
```

### Performance Monitoring
```bash
htop
free -h
df -h
```

### Log Files
- Access logs: `/opt/ai-resume-screener/logs/access.log`
- Error logs: `/opt/ai-resume-screener/logs/error.log`

## 🛡️ Security Best Practices

1. **Environment Variables**: Never commit secrets to Git
2. **HTTPS**: Use SSL certificates for production
3. **Firewall**: Restrict access to necessary ports only
4. **Updates**: Regular system and dependency updates
5. **Backup**: Regular database and file backups

## 💰 AWS Cost Optimization

### Free Tier Usage
- EC2 t2.micro: 750 hours/month
- EBS storage: 30 GB
- Data transfer: 15 GB/month

### Cost Monitoring
- Set up billing alerts
- Use AWS Cost Explorer
- Monitor resource usage regularly

## 🐛 Troubleshooting

### Common Issues

1. **Models not loading**
   ```bash
   # Check disk space and memory
   df -h && free -h
   # Restart application
   sudo systemctl restart ai-resume-screener
   ```

2. **Email not working**
   - Verify Gmail App Password
   - Check SMTP settings in .env
   - Ensure firewall allows SMTP traffic

3. **Application slow**
   - Monitor memory usage with `htop`
   - Check if swap is enabled
   - Optimize Gunicorn worker count

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review AWS deployment logs

## 🔄 Updates

To update the application on AWS:

```bash
cd /opt/ai-resume-screener
git pull origin main
sudo systemctl restart ai-resume-screener
```

---

**Note**: This application uses Git LFS for large model files. Ensure Git LFS is installed and configured before cloning.
