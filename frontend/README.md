# VentureGuard AI - Frontend

AI-Powered Business Intelligence Guardian for Entrepreneurs

## Features

- **Risk Dashboard** - Multi-dimensional risk overview with real-time alerts
- **Business Health Predictor** - AI-powered risk prediction 30-90 days ahead
- **Smart Contract Analyzer** - GPT-4 powered contract analysis
- **Cyber Threat Monitor** - Security scanning and breach detection
- **Crisis Response Generator** - AI-generated crisis playbooks

## Tech Stack

- Next.js 14
- React 18
- Ant Design 5
- TypeScript
- Axios

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-repo/ventureguard-ai)

Or manually:

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx      # Root layout with Ant Design
│   ├── page.tsx        # Main dashboard
│   └── globals.css     # Global styles
├── public/             # Static assets
├── package.json
└── vercel.json         # Vercel configuration
```

## API Integration

The frontend connects to the FastAPI backend:

- Business Health: `/api/v1/business-health`
- Contracts: `/api/v1/contracts`
- Cyber Security: `/api/v1/cyber`
- Risk Dashboard: `/api/v1/risks`
- Crisis Response: `/api/v1/crisis`

## License

MIT - GEF2025 Hackathon Project
