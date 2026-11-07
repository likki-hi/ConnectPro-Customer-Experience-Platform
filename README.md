
# ConnectPro – Customer Experience Platform

A purple-themed customer support management application inspired by Amazon Connect.

## Overview

ConnectPro is a local customer experience simulation that demonstrates customer management, support agent management, contact handling, automatic agent routing and business analytics.

## Technology Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly

## Features

- Customer registration and directory
- Support agent registration
- Agent availability management
- Customer contact registration
- Voice, Chat and Email channels
- Priority-based contact tracking
- Automatic agent assignment
- Contact status management
- Interactive analytics dashboard
- CSV report export

## Project Structure

- app.py – Streamlit frontend
- database.py – SQLite database configuration
- customer_manager.py – Customer operations
- agent_manager.py – Agent operations
- contact_manager.py – Contact management
- call_routing.py – Automatic agent routing

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

## Database

SQLite stores customer, agent and contact records locally.

## Disclaimer

This is a local simulation inspired by Amazon Connect. It does not connect to an actual AWS Amazon Connect instance.
 
 ## Author : Likitha Kalal