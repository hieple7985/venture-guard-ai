# VentureGuard AI

**AI-Powered Business Intelligence Guardian for Entrepreneurs**

Predict risks 30-90 days ahead, analyze contracts with GPT-4, monitor cyber threats, and get AI-generated crisis playbooks.

## 🚀 Live Demo

**Frontend**: https://venture-guard-ai.vercel.app

## ✨ Features

### 1. Business Health Predictor
- AI-powered risk prediction 30-90 days ahead
- Cash flow analysis and forecasting
- Market risk assessment
- Operational risk scoring
- Actionable recommendations

### 2. Smart Contract Analyzer
- GPT-4 powered contract analysis
- Automatic risk detection
- Unfair terms identification
- Missing clause alerts
- Legal risk scoring

### 3. Cyber Threat Monitor
- Real-time data breach scanning
- Domain security analysis
- Email breach detection
- Security score tracking
- Threat intelligence

### 4. Risk Dashboard
- Multi-dimensional risk overview
- Real-time alerts and notifications
- Historical trend analysis
- Risk score aggregation
- Interactive visualizations

### 5. Crisis Response Generator
- AI-generated crisis playbooks
- Step-by-step action plans
- Multiple crisis types supported
- Template-based fallbacks
- Customizable responses

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **AI/ML**: OpenAI GPT-4, Scikit-learn
- **Database**: PostgreSQL / SQLite
- **Cache**: Redis
- **APIs**: HaveIBeenPwned, VirusTotal

### Frontend
- **Framework**: Next.js 14
- **UI Library**: Ant Design 5
- **Language**: TypeScript
- **Styling**: CSS-in-JS
- **State**: React Hooks

## 📦 Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys

# Run server
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local
# Edit .env.local if needed

# Run development server
npm run dev
```

Frontend will run on `http://localhost:3000`

## 🔑 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=sqlite:///./ventureguard.db
REDIS_URL=redis://localhost:6379
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Main Endpoints

#### Business Health
- `POST /api/v1/business-health/analyze` - Analyze business metrics
- `POST /api/v1/business-health/analyze-csv` - Upload CSV for analysis
- `GET /api/v1/business-health/demo` - Demo analysis

#### Contract Analysis
- `POST /api/v1/contracts/analyze` - Analyze contract text
- `POST /api/v1/contracts/analyze-pdf` - Upload PDF contract
- `GET /api/v1/contracts/demo` - Demo analysis

#### Cyber Security
- `POST /api/v1/cyber/scan-email` - Check email breaches
- `POST /api/v1/cyber/scan-domain` - Check domain security
- `POST /api/v1/cyber/scan-url` - Check URL safety
- `GET /api/v1/cyber/demo` - Demo scan

#### Risk Dashboard
- `GET /api/v1/risks/overview` - Get risk overview
- `GET /api/v1/risks/alerts` - Get active alerts
- `POST /api/v1/risks/alerts/{id}/resolve` - Resolve alert
- `GET /api/v1/risks/demo` - Demo dashboard

#### Crisis Response
- `POST /api/v1/crisis/generate` - Generate crisis playbook
- `GET /api/v1/crisis/types` - List crisis types
- `GET /api/v1/crisis/demo` - Demo playbook

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🚀 Deployment

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

### Backend (Railway/Render)
- Connect GitHub repository
- Set environment variables
- Deploy automatically

## 📖 Project Structure

```
venture-guard-ai/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── business_health.py
│   │   │       ├── contract_analyzer.py
│   │   │       ├── cyber_monitor.py
│   │   │       ├── risk_dashboard.py
│   │   │       └── crisis_response.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── schemas/
│   │   └── services/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── package.json
│   └── next.config.js
└── README.md
```

## 🎯 Use Cases

1. **Startups**: Monitor business health and predict risks early
2. **SMEs**: Analyze contracts before signing
3. **Entrepreneurs**: Get cyber security insights
4. **Business Owners**: Prepare for potential crises

## 🔒 Security

- API keys stored in environment variables
- CORS protection enabled
- Rate limiting implemented
- Input validation on all endpoints
- Secure file upload handling

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

## 🏆 Hackathon

Built for **GEF2025 - The AI-Powered Entrepreneur** Hackathon

---

**Made with ❤️ for entrepreneurs worldwide**
