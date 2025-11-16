# MNB Yokoy FX Sync

A Python tool to fetch foreign exchange rates from the Hungarian National Bank (MNB) and upload them to Yokoy.

## Current Status

**Phase 3: Yokoy Integration** ✅ COMPLETED

The tool can now fetch exchange rates from MNB and upload them to Yokoy's FX Rates API!

## Quick Start

### 1. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Yokoy (Optional)

To enable uploading to Yokoy:

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Yokoy API credentials
# YOKOY_API_URL=https://app.yokoy.io/public/v1
# YOKOY_API_KEY=your_actual_api_key_here
```

### 3. Run the Tool

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Fetch current exchange rates
python main.py

# Fetch rates for a specific date
python main.py --date 2025-11-07

# Fetch and upload to Yokoy
python main.py --upload

# Fetch specific date and upload
python main.py --date 2025-11-07 --upload
```

## Project Structure

```
mnb-yokoy-fx-sync/
├── main.py           # Main script with CLI interface
├── config.py         # Configuration management
├── yokoy_client.py   # Yokoy API client
├── requirements.txt  # Python dependencies
├── .env.example      # Environment configuration template
├── todos.txt         # Project progress tracker
└── README.md         # This file
```

## Features

**Fetch Exchange Rates:**
- Connects to MNB API using the `mnb` library
- Fetches current or historical exchange rates
- Displays all currency rates in a formatted table

**Upload to Yokoy (Optional):**
- Transforms MNB data to Yokoy API format
- Uploads FX rates via Yokoy's REST API
- Handles authentication and error reporting

## Command Line Options

```
--date, -d DATE    Fetch rates for specific date (format: YYYY-MM-DD)
--upload, -u       Upload rates to Yokoy (requires configuration)
--help, -h         Show help message
```

## Requirements

- Python 3.7+
- Dependencies (see `requirements.txt`):
  - `mnb` - MNB API client library
  - `python-dotenv` - Environment configuration
  - `requests` - HTTP client for Yokoy API

## About

**MNB (Magyar Nemzeti Bank)** is the Central Bank of Hungary. They provide a public SOAP API with daily foreign exchange rates. The `mnb` library (https://github.com/belidzs/mnb) wraps this API in a clean, Pythonic interface.

**Yokoy** is an AI-powered spend management platform. Their FX Rates API allows automated upload of exchange rates for expense management.

## Next Steps
