# CryptIQ

CryptIQ is a cryptocurrency portfolio management system that utilizes advanced AI algorithms, market data analysis, and automated strategies to optimize trading decisions. The application combines real-time data analysis with trend prediction to generate buy, sell, and hold signals.

## Features
- **Automated Coin Analysis**: Analyzes top cryptocurrencies and generates trading signals based on technical indicators.
- **Asynchronous Data Fetching**: Uses `asyncio` for concurrent API requests.
- **Support for Multiple Timeframes**: Provides insights from 15-minute to weekly timeframes.
- **Technical Indicators**: Integrates indicators like SMA, RSI, MACD, Fibonacci levels, and Ichimoku.
- **Entry and Exit Signals**: Generates precise entry and exit signals based on market conditions.
- **Sound Notifications**: Audio alerts for exit signals or completion of analysis runs.
- **Blofin Holdings Integration**: Fetches and analyzes current holdings from Blofin exchange.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- Docker (optional, for containerization)
- Redis (for caching)
- PostgreSQL/MongoDB (for data storage)

### Environment Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/m0r6aN/CryptIQ.git
   cd CryptIQ

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables. Create a .env file in the root directory with the following:
```bash
CRYPTOCOMPARE_API_KEY=your_api_key_here
BLOFIN_API_KEY=your_api_key_here
BLOFIN_SECRET=your_secret_here
BLOFIN_PASSWORD=your_password_here
```

**CHANCE OR ADD EXCHANGES AS NEEDED**

## Running the Application

You can start the application with the following:
```bash
python crypto_portfolio_manager/apps/bot/scanner.py
```

**This is the entry for the scanning functionality. I'm using this until I vet the strategies**

### Docker

To run the app in Docker:

1. Build the Docker image:
```bash
docker build -t cryptiq .
```

2. Run the Docker container:
```bash
docker run -d cryptiq
```

## Architecture
The project is organized as follows:

- apps/bot/scanner.py: Entry point for scanning only. Retrieves the top x coins, filters coins of interest, performs analysis, and creates a .csv file
- utils/shared.py: Shared utilities, including data fetching and API integration.
- utils/coin_analyzer.py: Technical analysis logic, signal generation, and trend detection.

### Recent Updates
- Added retry logic and exponential backoff for Blofin API calls.
- Refactored sound playback into a reusable function.
- Improved error handling and logging for API requests.
- Consolidated leverage calculation and position parameter logic to reduce code redundancy.