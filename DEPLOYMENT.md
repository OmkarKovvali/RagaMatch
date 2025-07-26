# 🚀 Production Deployment Guide

This guide covers deploying RagaMatch to production environments including EC2, AWS, and other cloud platforms.

## 📋 Prerequisites

- Docker and Docker Compose installed
- Domain name (optional but recommended)
- SSL certificate (for HTTPS)
- Cloud provider account (AWS, GCP, Azure, etc.)

## 🏗️ Deployment Options

### Option 1: Simple Docker Deployment

1. **Clone and setup**
   ```bash
   git clone https://github.com/yourusername/RagaMatch.git
   cd RagaMatch
   cp .env.example .env
   ```

2. **Configure environment**
   ```bash
   # Edit .env file
   VITE_API_URL=http://your-server-ip:8000
   ```

3. **Deploy**
   ```bash
   ./scripts/deploy.sh
   ```

### Option 2: AWS EC2 Deployment

1. **Launch EC2 Instance**
   - Use Ubuntu 22.04 LTS
   - t3.medium or larger (2GB RAM minimum)
   - Configure security groups:
     - Port 80 (HTTP)
     - Port 443 (HTTPS)
     - Port 22 (SSH)

2. **Connect and setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo usermod -aG docker ubuntu
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Deploy application**
   ```bash
   git clone https://github.com/yourusername/RagaMatch.git
   cd RagaMatch
   cp .env.example .env
   
   # Edit .env with your EC2 IP
   VITE_API_URL=http://your-ec2-ip:8000
   
   # Deploy
   ./scripts/deploy.sh
   ```

### Option 3: Production with Nginx Reverse Proxy

1. **Install Nginx**
   ```bash
   sudo apt install nginx -y
   ```

2. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/ragamatch
   ```

   Add this configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:80;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       location /api/ {
           proxy_pass http://localhost:8000/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

3. **Enable site and restart**
   ```bash
   sudo ln -s /etc/nginx/sites-available/ragamatch /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### Option 4: Docker Swarm Deployment

1. **Initialize swarm**
   ```bash
   docker swarm init
   ```

2. **Deploy stack**
   ```bash
   docker stack deploy -c docker-compose.prod.yml ragamatch
   ```

3. **Check status**
   ```bash
   docker stack services ragamatch
   docker stack ps ragamatch
   ```

## 🔒 SSL/HTTPS Setup

### Using Let's Encrypt with Certbot

1. **Install Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

2. **Obtain certificate**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

3. **Auto-renewal**
   ```bash
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

## 📊 Monitoring and Logging

### Basic Monitoring

1. **Container health checks**
   ```bash
   docker ps
   docker stats
   ```

2. **Application logs**
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f
   ```

### Advanced Monitoring with Prometheus/Grafana

1. **Add monitoring stack**
   ```yaml
   # Add to docker-compose.prod.yml
   prometheus:
     image: prom/prometheus
     ports:
       - "9090:9090"
     volumes:
       - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
   
   grafana:
     image: grafana/grafana
     ports:
       - "3000:3000"
     environment:
       - GF_SECURITY_ADMIN_PASSWORD=admin
   ```

## 🔧 Environment-Specific Configurations

### Development
```env
VITE_API_URL=http://localhost:8000
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### Staging
```env
VITE_API_URL=http://staging.yourdomain.com/api
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

### Production
```env
VITE_API_URL=https://yourdomain.com/api
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**
   ```bash
   # Check what's using port 80
   sudo lsof -i :80
   sudo lsof -i :8000
   ```

2. **Permission issues**
   ```bash
   # Fix Docker permissions
   sudo chmod 666 /var/run/docker.sock
   ```

3. **Memory issues**
   ```bash
   # Check memory usage
   free -h
   docker stats
   ```

4. **Network issues**
   ```bash
   # Test connectivity
   curl -I http://localhost:8000/docs
   curl -I http://localhost
   ```

### Performance Optimization

1. **Resource limits**
   ```yaml
   # In docker-compose.prod.yml
   deploy:
     resources:
       limits:
         memory: 2G
         cpus: '1.0'
   ```

2. **Caching**
   - Enable Nginx caching
   - Use CDN for static assets
   - Implement Redis for session storage

## 📈 Scaling

### Horizontal Scaling

1. **Load balancer setup**
   ```bash
   # Use HAProxy or Nginx as load balancer
   docker run -d --name haproxy -p 80:80 haproxy:latest
   ```

2. **Multiple instances**
   ```bash
   # Scale backend service
   docker-compose -f docker-compose.prod.yml up -d --scale backend=3
   ```

### Vertical Scaling

1. **Increase resources**
   - Upgrade EC2 instance type
   - Add more memory/CPU
   - Use dedicated instances

## 🔄 Backup and Recovery

### Data Backup

1. **Model files**
   ```bash
   # Backup model directory
   tar -czf model-backup-$(date +%Y%m%d).tar.gz backend/model/
   ```

2. **Configuration**
   ```bash
   # Backup configuration
   cp .env .env.backup-$(date +%Y%m%d)
   ```

### Recovery

1. **Restore from backup**
   ```bash
   # Restore model files
   tar -xzf model-backup-YYYYMMDD.tar.gz
   
   # Restore configuration
   cp .env.backup-YYYYMMDD .env
   ```

2. **Redeploy**
   ```bash
   ./scripts/deploy.sh
   ```

## 📞 Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Verify configuration: `docker-compose config`
3. Test connectivity: `curl -I http://localhost:8000/docs`
4. Open GitHub issue with logs and configuration

---

**Happy Deploying! 🚀** 