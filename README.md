# Crypto Portfolio Manager Documentation

## Table of Contents
- [Crypto Portfolio Manager Documentation](#crypto-portfolio-manager-documentation)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Key Features](#key-features)
  - [Technical Architecture](#technical-architecture)
  - [Directory Structure](#directory-structure)
  - [Backend Details](#backend-details)
    - [Models](#models)
  - [Views](#views)
  - [Serializers](#serializers)
  - [URLs](#urls)
  - [Authentication](#authentication)
  - [WebSockets Integration](#websockets-integration)
  - [AI Services Integration](#ai-services-integration)
  - [Frontend Details](#frontend-details)
  - [React Components](#react-components)
  - [Redux Store](#redux-store)
  - [Routing](#routing)
    - [Routes:](#routes)
  - [API Services](#api-services)
  - [DevOps and Deployment](#devops-and-deployment)
  - [Docker Configuration](#docker-configuration)
    - [Dockerfile (Backend)](#dockerfile-backend)
  - [Deployment Steps](#deployment-steps)
  - [Testing and Quality Assurance](#testing-and-quality-assurance)

## Project Overview

The **Crypto Portfolio Manager** is a personal web application designed to help users manage their cryptocurrency portfolios efficiently. It consolidates assets from multiple exchanges and wallets, provides real-time tracking of portfolio performance, allows manual trading and swaps, and includes advanced analytics and AI-powered assistance.

## Key Features
- **Multi-Exchange Integration**: Connect to unlimited centralized exchanges (e.g., Binance, Coinbase Pro, Kraken).
- **Web3 Wallet Connectivity**: Integrate with various Web3 wallets, including MetaMask and hardware wallets like Ledger.
- **Unified Portfolio Dashboard**: Real-time tracking of portfolio performance and asset allocation.
- **Manual Trading and Swaps**: Execute trades directly from the platform.
- **Automated Portfolio Management**: Intelligent rebalancing based on user-defined strategies.
- **Advanced Analytics and Reporting**: In-depth analytics tools for performance tracking.
- **AI-Powered Personal Assistant**: Integrated AI chat assistant for personalized recommendations.
- **Security and Compliance**: 6-digit PIN authentication and data encryption.
- **User-Friendly Interface**: Responsive UI/UX design with customizable dashboards.
- **Notifications and Alerts**: Real-time notifications for significant portfolio changes.

## Technical Architecture

The application is built using a **React.js** frontend and a **Django** backend, with **Docker** used for containerization. The backend uses **PostgreSQL** for relational data, **MongoDB** for non-relational data, and **Redis** for caching. The frontend manages state using **Redux** and styles components using **Tailwind CSS**.

## Directory Structure

```plaintext
CryptoPortfolioManager/
├── backend/
│   ├── crypto_portfolio_manager/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   │   ├── accounts/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├── ai_assistant/
│   │   │   │   ├── services.py
│   │   │   │   ├── urls.py
│   │   │   │   ├── views.py
│   │   │   ├── market_data/
│   │   │   │   ├── views.py
│   │   │   ├── portfolio/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── consumers.py
│   │   │   │   ├── models.py
│   │   │   │   ├── routing.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   │   │   ├──  trading/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── serializers.py
│   │   │   │   ├── urls.py
│   │   │   │   └── views.py
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
├── docker-compose.yml
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── public/
    └── src/
        ├── App.js
        ├── index.js
        ├── components/
        ├── pages/
        ├── redux/
        ├── services/
        ├── styles/
        └── utils/
```

Installation and Setup
Prerequisites
Docker and Docker Compose installed on your machine.
Node.js and npm (if running the frontend without Docker).
Python 3.9+ (if running the backend without Docker).

Steps
Clone the Repository

```bash
git clone https://github.com/yourusername/CryptoPortfolioManager.git
cd CryptoPortfolioManager
```

Set Up Environment Variables
Create a .env file in the backend/ directory.

Add the following variables:

```makefile
DJANGO_SECRET_KEY=your-django-secret-key
POSTGRES_DB=crypto_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
OPENAI_API_KEY=your-openai-api-key
```

Build and Run Docker Containers
```bash
docker-compose up --build
```

Apply Database Migrations
Open a new terminal and run:
```bash
docker-compose exec backend python manage.py migrate
```

Access the Application
Frontend: http://localhost:3000
Backend API: http://localhost:8000/api/

## Backend Details

### Models
**Accounts App **(accounts/models.py)
- User: Custom user model extending AbstractBaseUser with email and 6-digit PIN for authentication.

**Portfolio App **(portfolio/models.py)
- ExchangeAccount: Stores user's exchange API credentials.
- Wallet: Stores user's wallet addresses.
- Asset: Represents a cryptocurrency asset.
- Portfolio: Represents a user's portfolio, linked to holdings.
- Holding: Intermediate model between Portfolio and Asset with quantity.

**Trading App** (trading/models.py)
- Trade: Represents a trade executed by the user, including type, asset, quantity, price, and timestamp.

**AI Assistant App** (ai_assistant/models.py)
- Currently, no models are defined. AI services are provided via external APIs.

## Views
**Accounts App** (accounts/views.py)
- UserCreateView: Allows new users to register.
- TokenObtainPairView: Provides JWT authentication tokens.

**Portfolio App** (portfolio/views.py)
- PortfolioView: Retrieves the user's portfolio.
- ExchangeAccountListCreateView: Lists and creates exchange accounts.
- WalletListCreateView: Lists and creates wallets.

**Trading App** (trading/views.py)
- TradeListCreateView: Lists and creates trades.

**AI Assistant App** (ai_assistant/views.py)
- AIChatView: Handles AI assistant requests.

## Serializers
Serializers convert models to JSON for API responses and handle validation for incoming data.

- UserSerializer
- AssetSerializer
- HoldingSerializer
- PortfolioSerializer
- ExchangeAccountSerializer
- WalletSerializer
- TradeSerializer

## URLs
Defined in each app's urls.py and included in the main crypto_portfolio_manager/urls.py.

- Accounts: /api/accounts/
- Portfolio: /api/portfolio/
- Trading: /api/trading/
- AI Assistant: /api/ai/

## Authentication
Implemented using JWT (JSON Web Tokens) via djangorestframework-simplejwt.
- Token Acquisition: /api/accounts/token/
- Token Refresh: /api/accounts/token/refresh/

## WebSockets Integration
- Implemented using Django Channels for real-time features.
- WebSocket Endpoint: /ws/portfolio/
- Consumer: PortfolioConsumer handles WebSocket connections and broadcasts portfolio updates.

## AI Services Integration
Utilizes the OpenAI API to provide AI-powered assistance.
- Service: get_ai_response in ai_assistant/services.py sends prompts to OpenAI and returns responses.
- API Key: Stored securely in environment variables.

## Frontend Details

## React Components
- App.js: Root component setting up routing.
- Navbar: Navigation bar with links to different pages.
- Dashboard: Main component displaying portfolio summary, asset allocation, recent transactions, and AI assistant link.
- PortfolioPage: Displays detailed portfolio holdings.
- TradePage: Interface for executing trades.
- AIChatPage: Interface for interacting with the AI assistant.
- LoginPage and RegisterPage: Authentication interfaces.
- PortfolioChart: Displays portfolio performance over time using charts.

## Redux Store
- Actions: Define functions to fetch data and dispatch actions (e.g., fetchPortfolio, fetchMarketData).
- Reducers: Handle state changes in response to dispatched actions (portfolioReducer, marketDataReducer).
- Store: Combines reducers and applies middleware (redux-thunk).

## Routing
Implemented using React Router in App.js.

### Routes:
- /: HomePage
- /portfolio: PortfolioPage
- /trade: TradePage
- /ai-chat: AIChatPage
- /login: LoginPage
- /register: RegisterPage

## API Services
- api.js: Configures Axios instance with base URL and interceptors for authentication.
- auth.js: Handles authentication requests (login, register, logout).
- websocket.js: Manages WebSocket connections using Socket.IO.

## DevOps and Deployment

## Docker Configuration

### Dockerfile (Backend)

```dockerfile
FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/
```

Dockerfile (Frontend)
```dockerfile
FROM node:14-alpine

WORKDIR /app

COPY package.json ./

RUN npm install

COPY . ./

CMD ["npm", "start"]
```

docker-compose.yml
Defines services for the backend, frontend, database, Redis, and MongoDB.

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/code
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - db
      - redis
      - mongo

  frontend:
    build: ./frontend
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    depends_on:
      - backend

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: crypto_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your-db-password
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  redis:
    image: redis:6

  mongo:
    image: mongo:4.4
    volumes:
      - mongo_data:/data/db

volumes:
  postgres_data:
  mongo_data:
```

## Deployment Steps

Build Docker Images
```bash
docker-compose build
```

Run Containers
```bash
docker-compose up -d
```

Apply Migrations and Collect Static Files
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```

**Set Up a Production Server**
- Use Gunicorn and Nginx for the backend.
- Configure SSL/TLS certificates for secure connections.
- Use environment variables for production settings (e.g., DEBUG=False).

## Testing and Quality Assurance
Backend Testing
- Unit Tests: Written using pytest or Django's built-in test framework.
- Test Coverage: Models, views, serializers, and utilities.

Commands:
```bash
docker-compose exec backend python manage.py test
```

Frontend Testing
Unit Tests: Using Jest and React Testing Library.
End-to-End Tests: Using Cypress or Selenium.

Commands:
```bash
npm test
```

Security Considerations
Authentication: Uses JWT tokens with secure storage and handling.
Data Encryption: Ensure data in transit uses HTTPS. Use SSL certificates in production.
Environment Variables: Sensitive information is stored in .env files and not checked into version control.
Access Control: API endpoints are secured with proper permission classes.
WebSocket Security: Authentication middleware ensures only authenticated users can establish WebSocket connections.
Further Development
Suggested Enhancements
Automated Portfolio Rebalancing: Implement algorithms for user-defined rebalancing strategies.
Advanced Analytics: Integrate more comprehensive analytics tools and visualizations.
Notifications System: Implement real-time notifications for significant events.
User Settings: Allow users to customize dashboard widgets and preferences.
Multi-Language Support: Internationalize the application for broader accessibility.
Mobile App: Develop a React Native application for mobile users.
Technical Debt
Error Handling: Improve error handling and user feedback across the application.
Code Refactoring: Optimize code for better performance and maintainability.
Documentation: Enhance inline code comments and developer documentation.