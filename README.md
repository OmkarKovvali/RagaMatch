# 🎵 RagaMatch

**Classical Roots. Modern Intelligence.**

RagaMatch is an AI-powered application that identifies Indian classical music ragas from audio files in seconds. Built with React frontend and FastAPI backend, it uses deep learning models to analyze audio features and provide accurate raga predictions.

IMPORTANT: The currently implemented TDNN+LSTM+Attention model pipeline achieves a ~92% test accuracy but does NOT generalize well to audio outside the dataset. This issue is currently being investigated and will hopefully be fixed soon.

## 🌟 Features

- **Instant Raga Identification**: Upload any audio file and get raga predictions in seconds
- **Modern Web Interface**: Beautiful, responsive React frontend with intuitive design
- **Robust Backend**: FastAPI-powered API with comprehensive audio processing
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Production Ready**: Configured for both development and production environments

## 🏗️ Architecture

```
RagaMatch/
├── frontend/          # React application
├── backend/           # FastAPI server
├── model/            # ML model files
├── scripts/          # Deployment scripts
└── docker-compose.yml # Container orchestration
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for development)
- Python 3.11+ (for development)

### Option 1: Docker Deployment (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/RagaMatch.git
   cd RagaMatch
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Deploy with Docker**
   ```bash
   # For production
   ./scripts/deploy.sh
   
   # Or manually
   docker-compose -f docker-compose.prod.yml up -d
   ```

4. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Option 2: Development Setup

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Configure environment**
   ```bash
   # In frontend/.env
   VITE_API_URL=http://localhost:8000
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Frontend Configuration
VITE_API_URL=http://localhost:8000

# Production Configuration (for EC2 deployment)
# VITE_API_URL=http://your-ec2-ip:8000
```

### Production Deployment

For production deployment on EC2 or other cloud platforms:

1. **Update environment variables**
   ```env
   VITE_API_URL=http://your-server-ip:8000
   ```

2. **Deploy with production compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Configure reverse proxy (optional)**
   - Use Nginx or Apache for SSL termination
   - Set up domain name and SSL certificates

## 📁 Project Structure

```
RagaMatch/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── model/               # ML model and utilities
│   │   ├── best_model.pth   # Trained model weights
│   │   ├── class_names.json # Raga class names
│   │   ├── my_model.py      # Model architecture
│   │   └── utils.py         # Feature extraction utilities
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   └── assets/         # Static assets
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Frontend container
│   └── nginx.conf          # Nginx configuration
├── scripts/
│   └── deploy.sh           # Deployment script
├── docker-compose.yml      # Development compose
├── docker-compose.prod.yml # Production compose
└── README.md              # This file
```

## 🎯 API Endpoints

### POST /predict/
Upload an audio file to get raga prediction.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (audio file)

**Response:**
```json
{
  "prediction": "Dhenuka"
}
```

**Example:**
```bash
curl -X POST -F "file=@audio.wav" http://localhost:8000/predict/
```

## 🛠️ Development

### Adding New Features

1. **Backend Changes**
   - Modify `backend/main.py` for new endpoints
   - Update `backend/model/utils.py` for new ML features
   - Test with `curl` or FastAPI docs

2. **Frontend Changes**
   - Modify `frontend/src/App.jsx` for UI changes
   - Update styles in `frontend/src/App.css`
   - Test with `npm run dev`

### Testing

```bash
# Test backend API
curl -X POST -F "file=@Trial.wav" http://localhost:8000/predict/

# Test frontend
npm run dev  # in frontend directory
```

## 🐳 Docker Commands

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## 🔍 Troubleshooting

### Common Issues

1. **Frontend can't connect to backend**
   - Check `VITE_API_URL` in `.env`
   - Ensure backend is running on correct port
   - Check CORS configuration

2. **Docker build fails**
   - Clear Docker cache: `docker system prune -a`
   - Check Dockerfile syntax
   - Verify file paths

3. **Model loading errors**
   - Ensure model files exist in `backend/model/`
   - Check file permissions
   - Verify model file integrity

### Logs and Debugging

```bash
# View container logs
docker-compose logs backend
docker-compose logs frontend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Check service health
docker-compose ps
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Indian Classical Music community for inspiration
- FastAPI and React communities for excellent frameworks
- Contributors and testers

## 📞 Support

For support and questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review API documentation at `/docs`

---

**Made with ❤️ for Indian Classical Music**

