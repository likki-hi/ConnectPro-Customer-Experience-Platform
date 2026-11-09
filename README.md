# ConnectPro – Customer Experience Platform

A customer support management application inspired by **Amazon Connect**, built with Python and Streamlit. ConnectPro handles omnichannel customer contacts (voice, chat, email), routes each contact to an available support agent, and reports on activity through an analytics dashboard.

> **Note:** This is a local simulation. It does not connect to a live AWS Amazon Connect instance. It was built to understand the core ideas behind contact center platforms: contacts, routing, agent availability, and reporting.

## Features

- **Customer management**: register customers and browse a customer directory
- **Agent management**: register support agents and set their availability
- **Omnichannel contacts**: log voice, chat, and email contacts for any customer
- **Priority-based tracking**: each contact carries a priority level
- **Automatic agent routing**: new contacts are assigned to an available agent
- **Contact lifecycle**: update contact status until the issue is resolved
- **Analytics dashboard**: interactive Plotly charts for contact volume, channels, priorities, and agent workload
- **CSV export**: download reports for further analysis

## How It Maps to Amazon Connect

| ConnectPro                     | Amazon Connect equivalent         |
|--------------------------------|-----------------------------------|
| Contact (voice / chat / email) | Contact / channel                 |
| Agent availability             | Agent status                      |
| Automatic agent assignment     | Routing profile and queue routing |
| Priority levels                | Queue priority                    |
| Analytics dashboard            | Real-time and historical metrics  |
| CSV export                     | Reporting and data export         |

## Architecture

```
┌─────────────┐      ┌──────────────────────┐      ┌────────────┐
│  Streamlit  │ ───▶ │  Manager modules     │ ───▶ │   SQLite   │
│  (app.py)   │      │  customer / agent /  │      │ (database) │
└─────────────┘      │  contact / routing   │      └────────────┘
       ▲             └──────────────────────┘
       │                       │
       └──── Plotly dashboards ◀┘
```

**Contact flow:** a contact is created → priority is set → the routing module finds an available agent → the contact is assigned → status is updated until resolved.

## Project Structure

| File                  | Purpose                                |
|-----------------------|----------------------------------------|
| `app.py`              | Streamlit frontend and page navigation |
| `database.py`         | SQLite connection and table setup      |
| `customer_manager.py` | Customer operations                    |
| `agent_manager.py`    | Agent operations and availability      |
| `contact_manager.py`  | Contact creation, status, and priority |
| `call_routing.py`     | Automatic agent routing                |
| `requirements.txt`    | Python dependencies                    |

## Tech Stack

Python · Streamlit · SQLite · Pandas · Plotly

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/likki-hi/ConnectPro-Customer-Experience-Platform.git
cd ConnectPro-Customer-Experience-Platform

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python -m streamlit run app.py
```

The SQLite database is created locally on first run.

## Future Improvements

- Skills-based routing (match contacts to agents by skill and language)
- Queue wait times and service-level metrics
- Unit tests for the routing logic

## Author

**Likitha Kalal**
GitHub: [@likki-hi](https://github.com/likki-hi)
