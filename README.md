# Marketing Campaign Agent

An intelligent marketing campaign analysis and recommendation system that combines web research with sales data analytics to provide comprehensive campaign insights and recommendations.

## 🚀 Features

- **Web Research Integration**: Uses Tavily Search API to gather real-time market insights
- **Sales Data Analysis**: Analyzes historical sales data for trend identification
- **AI-Powered Insights**: Leverages Google Gemini 2.0 Flash for intelligent analysis
- **Year-over-Year Analysis**: Provides detailed YoY comparisons for sales and profit trends
- **Regional Analysis**: Identifies regional patterns and opportunities
- **Interactive Web Interface**: Streamlit-based frontend for easy interaction
- **RESTful API**: FastAPI backend for programmatic access

## 🏗️ Architecture

The application consists of two main components:

1. **Backend API** (FastAPI): Handles the core business logic and AI processing
2. **Frontend Interface** (Streamlit): Provides a user-friendly web interface

The system uses a LangGraph-based workflow that:
1. Generates search queries based on user input
2. Executes web searches for market insights
3. Analyzes sales data for relevant trends
4. Aggregates insights into comprehensive reports

## 📋 Prerequisites

- Python 3.13.4 or higher
- Docker (for containerized deployment)
- API Keys:
  - [Tavily API Key](https://tavily.com/) for web search functionality
  - [Google API Key](https://makersuite.google.com/app/apikey) for Gemini AI

## 🛠️ Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd marketing-campaign-agent
```

### 2. Install Dependencies

The project uses `uv` for dependency management. Install it first:

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv sync
```

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add your API keys to the `.env` file:

```env
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

### 4. Run the Application

#### Option A: Run Both Services (Recommended)

Use the provided script to run both the FastAPI backend and Streamlit frontend:

```bash
# Make the script executable
chmod +x scripts/run.sh

# Run both services
./scripts/run.sh
```

#### Option B: Run Services Separately

**Backend (FastAPI):**
```bash
uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend (Streamlit):**
```bash
uv run streamlit run src/frontend/app.py --server.port 8501
```

### 5. Access the Application

- **Frontend Interface**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Endpoint**: http://localhost:8000/prompt

## 🐳 Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t marketing-campaign-agent .
```

### 2. Run with Docker

```bash
# Run with environment variables
docker run -p 8000:8000 -p 8501:8501 \
  -e TAVILY_API_KEY=your_tavily_api_key \
  -e GOOGLE_API_KEY=your_google_api_key \
  marketing-campaign-agent
```

### 3. Using Docker Compose (Optional)

Create a `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  marketing-agent:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    environment:
      - TAVILY_API_KEY=${TAVILY_API_KEY}
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    volumes:
      - ./data:/app/data
```

Run with:
```bash
docker-compose up --build
```

## 📊 Usage

### Web Interface

1. Open http://localhost:8501 in your browser
2. Enter your marketing campaign idea or prompt
3. Click "Generate Response"
4. View the comprehensive analysis and recommendations

### API Usage

Send a POST request to `/prompt`:

```bash
curl -X POST "http://localhost:8000/prompt" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a campaign for office supplies targeting small businesses"}'
```

Example response:
```json
{
  "prompt_response": "Executive Summary:\n- Market analysis shows growing demand for office supplies...\n\nKey Insights:\n- 15% YoY growth in Binders category...\n\nRecommended Actions:\n- Focus on Western region with 25% growth..."
}
```

## 📁 Project Structure

```
marketing-campaign-agent/
├── config/
│   └── settings.py          # Configuration settings
├── data/
│   └── Superstore.xlsx      # Sample sales data
├── notebooks/               # Jupyter notebooks for development
├── scripts/
│   └── run.sh              # Service startup script
├── src/
│   ├── app.py              # FastAPI backend
│   ├── graph.py            # LangGraph workflow
│   ├── prompts.py          # AI prompts
│   └── frontend/
│       └── app.py          # Streamlit frontend
├── Dockerfile              # Docker configuration
├── pyproject.toml          # Project dependencies
└── uv.lock                 # Dependency lock file
```

