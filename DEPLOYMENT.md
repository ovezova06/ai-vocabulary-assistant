# Deployment Guide - AI Vocabulary Assistant

## Local Deployment

### Development Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access at http://localhost:5000
```

## Docker Deployment

### Build and Run

```bash
# Build the image
docker build -t ai-vocabulary-assistant .

# Run the container
docker run -p 5000:5000 ai-vocabulary-assistant
```

### Using Docker Compose

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

## Production Deployment

### Prerequisites

- Python 3.8+
- pip
- A production-grade WSGI server (Gunicorn recommended)
- A reverse proxy (Nginx recommended)

### Step 1: Prepare Environment

```bash
# Create directory
mkdir -p /var/www/ai-vocabulary-assistant
cd /var/www/ai-vocabulary-assistant

# Clone/copy project
git clone https://github.com/yourusername/ai-vocabulary-assistant .

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 2: Configure Application

Update `.env` file:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=sqlite:///instance/vocabulary.db
```

Generate a secure SECRET_KEY:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 3: Setup Gunicorn

Create `wsgi.py`:

```python
from app import app

if __name__ == "__main__":
    app.run()
```

### Step 4: Create Systemd Service

Create `/etc/systemd/system/ai-vocabulary.service`:

```ini
[Unit]
Description=AI Vocabulary Assistant
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/ai-vocabulary-assistant
Environment="PATH=/var/www/ai-vocabulary-assistant/venv/bin"
ExecStart=/var/www/ai-vocabulary-assistant/venv/bin/gunicorn --workers 4 --bind unix:/run/ai-vocabulary.sock wsgi:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-vocabulary
sudo systemctl start ai-vocabulary
```

### Step 5: Configure Nginx

Create `/etc/nginx/sites-available/ai-vocabulary`:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://unix:/run/ai-vocabulary.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/ai-vocabulary-assistant/static;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/ai-vocabulary /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Setup SSL (Let's Encrypt)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Heroku Deployment

### Prerequisites

- Heroku account
- Heroku CLI installed
- Git installed

### Step 1: Create Heroku App

```bash
heroku login
heroku create your-app-name
```

### Step 2: Set Environment Variables

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

### Step 3: Deploy

```bash
git push heroku main
```

### Step 4: Initialize Database

```bash
heroku run python -c "from database import init_db; init_db()"
```

### View Logs

```bash
heroku logs --tail
```

## AWS Deployment

### Option 1: Elastic Beanstalk

```bash
# Install EB CLI
pip install awseb-cli

# Initialize
eb init -p python-3.11 ai-vocabulary

# Create environment
eb create ai-vocabulary-env

# Deploy
eb deploy
```

### Option 2: EC2

1. Launch Ubuntu 22.04 LTS instance
2. SSH into instance
3. Follow "Production Deployment" steps above

## Database Backup

### Backup SQLite Database

```bash
# Backup
cp instance/vocabulary.db instance/vocabulary.backup.db

# Restore
cp instance/vocabulary.backup.db instance/vocabulary.db
```

### Automated Backups

Create backup script `backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/ai-vocabulary"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
cp /var/www/ai-vocabulary-assistant/instance/vocabulary.db \
   $BACKUP_DIR/vocabulary_$TIMESTAMP.db

# Keep only last 30 days
find $BACKUP_DIR -name "*.db" -mtime +30 -delete
```

Add to crontab:

```bash
0 2 * * * /home/user/backup.sh
```

## Monitoring

### Health Check

```bash
curl http://yourdomain.com/
```

### View Logs

```bash
# Systemd logs
sudo journalctl -u ai-vocabulary -f

# Application logs (if configured)
tail -f /var/log/ai-vocabulary.log
```

## Performance Optimization

### Gunicorn Workers

```bash
# Calculate optimal workers
workers = (2 × CPU cores) + 1

# Example for 2-core machine:
gunicorn --workers 5 app:app
```

### Database Optimization

```python
# Enable WAL mode for SQLite
import sqlite3
conn = sqlite3.connect('vocabulary.db')
conn.execute('PRAGMA journal_mode=WAL')
```

## Security Checklist

- ✅ Change SECRET_KEY from default
- ✅ Set FLASK_DEBUG=False in production
- ✅ Use HTTPS/SSL certificate
- ✅ Enable CSRF protection
- ✅ Validate all user inputs
- ✅ Use environment variables for secrets
- ✅ Regular security updates
- ✅ Database backups
- ✅ Monitor logs for errors

## Troubleshooting

### 502 Bad Gateway (Nginx)

```bash
# Check Gunicorn socket
ls -la /run/ai-vocabulary.sock

# Check service status
sudo systemctl status ai-vocabulary
```

### Database Locked

```bash
# Reset database
rm instance/vocabulary.db
python -c "from database import init_db; init_db()"
```

### High Memory Usage

```bash
# Reduce worker processes
gunicorn --workers 2 app:app

# Monitor memory
top -p $(pgrep -f gunicorn | tr '\n' ',')
```

## Support

For deployment issues, consult the official documentation:

- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Heroku Documentation](https://devcenter.heroku.com/)
