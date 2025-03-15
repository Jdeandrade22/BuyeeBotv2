# JDM Parts Search Bot

A Python-based GUI application that helps you search for JDM parts on Buyee.jp with a cool matrix effect animation.

## Features

- Search Buyee.jp for JDM parts
- Filter results by keyword and criteria
- Set price ranges for searches
- Cool matrix effect animation during searches
- Save search results to a file
- SQLite database for storing search history

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/BuyeeBotv2.git
cd BuyeeBotv2
```

2. Install the required packages:
```bash
python -m pip install --force-reinstall --extra-index-url https://PySimpleGUI.net/install PySimpleGUI
python -m pip install -r requirements.txt
```

3. Make sure you have Google Chrome installed (required for web scraping)

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter your search parameters:
   - Keyword: What you're looking for (e.g., "work wheels")
   - Matching Criteria: Comma-separated terms to filter results (e.g., "meister,vs,ssr")
   - Min Price: Minimum price in yen
   - Max Price: Maximum price in yen

3. Click the "🔍 Search" button to start searching
4. Use the "💾 Save Results" button to save the results to a text file

## Requirements

- Python 3.6+
- Google Chrome
- See requirements.txt for Python package dependencies

## Note

This bot is designed for personal use and should be used responsibly in accordance with Buyee.jp's terms of service.