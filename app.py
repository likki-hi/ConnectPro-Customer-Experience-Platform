
import streamlit as st
import pandas as pd
import plotly.express as px

from database import create_tables
from customer_manager import add_customer, get_customers
from agent_manager import add_agent, get_agents, update_agent_status
from contact_manager import (
    add_contact,
    get_contact_details,
    update_contact_status
)
from routing_engine import (
    get_routing_queue,
    assign_agent,
    route_next_contact
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="ConnectPro | Customer Experience",
    page_icon="💙",
    layout="wide"
)

create_tables()


# ==========================================
# PROFESSIONAL NAVY BLUE THEME
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #F7F9FC;
}

section[data-testid="stSidebar"] {
    background-color: #142D4E;
}

section[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

h1, h2, h3 {
    color: #172B4D !important;
    font-weight: 700;
}

p, label {
    color: #475569;
}

div.stButton > button {
    background-color: #2563EB;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    padding: 0.55rem 1rem;
}

div.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
}

div.stFormSubmitButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
}

[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
}

.stTextInput input,
.stTextArea textarea {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #CBD5E1;
}

[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

hr {
    border-color: #E2E8F0;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("💙 ConnectPro")

st.sidebar.caption("Customer Experience Platform")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Customers",
        "Agents",
        "Contact Center",
        "Smart Routing",
        "Reports & Analytics"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("### Technology Stack")

st.sidebar.caption(
    "Python | Streamlit | SQLite | NLP | Plotly"
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Educational local simulation inspired by Amazon Connect"
)


# ==========================================
# COMMON DATA FUNCTIONS
# ==========================================

def load_contacts():

    records = get_contact_details()

    columns = [
        "Contact ID",
        "Customer",
        "Agent",
        "Issue",
        "Channel",
        "Priority",
        "Status",
        "Created At",
        "Sentiment",
        "Sentiment Score"
    ]

    return pd.DataFrame(records, columns=columns)


def show_sentiment(value):

    if value == "Positive":
        return "🟢 Positive"

    elif value == "Negative":
        return "🔴 Negative"

    return "🟡 Neutral"


# ==========================================
# 1. OVERVIEW DASHBOARD
# ==========================================

if page == "Overview":

    st.title("Welcome to ConnectPro")

    st.caption(
        "Customer support management and intelligent "
        "customer experience analytics."
    )

    contacts = load_contacts()

    customers = get_customers()

    agents = get_agents()

    total_customers = len(customers)

    total_agents = len(agents)

    total_contacts = len(contacts)

    available_agents = sum(
        1 for agent in agents
        if agent[2] == "Available"
    )

    open_contacts = (
        (contacts["Status"] == "Open").sum()
        if not contacts.empty else 0
    )

    in_progress = (
        (contacts["Status"] == "In Progress").sum()
        if not contacts.empty else 0
    )

    resolved = (
        (contacts["Status"] == "Resolved").sum()
        if not contacts.empty else 0
    )

    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)

    col2.metric("Total Agents", total_agents)

    col3.metric("Total Contacts", total_contacts)

    col4.metric("Available Agents", available_agents)

    st.subheader("Contact Status")

    col5, col6, col7 = st.columns(3)

    col5.metric("Open Contacts", open_contacts)

    col6.metric("In Progress", in_progress)

    col7.metric("Resolved", resolved)

    left, right = st.columns(2)

    with left:

        st.subheader("Contact Status Distribution")

        if not contacts.empty:

            status_data = (
                contacts["Status"]
                .value_counts()
                .rename_axis("Status")
                .reset_index(name="Count")
            )

            fig = px.pie(
                status_data,
                names="Status",
                values="Count",
                hole=0.45,
                color_discrete_sequence=[
                    "#2563EB",
                    "#60A5FA",
                    "#CBD5E1"
                ]
            )

            st.plotly_chart(
                fig,
               width="stretch"
            )

        else:

            st.info("No contact data available yet.")

    with right:

        st.subheader("Customer Sentiment")

        if not contacts.empty:

            sentiment_data = (
                contacts["Sentiment"]
                .value_counts()
                .rename_axis("Sentiment")
                .reset_index(name="Count")
            )

            fig = px.pie(
                sentiment_data,
                names="Sentiment",
                values="Count",
                hole=0.45,
                color_discrete_sequence=[
                    "#2563EB",
                    "#F59E0B",
                    "#94A3B8"
                ]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info("Sentiment analytics will appear here.")

    st.subheader("Recent Customer Interactions")

    if not contacts.empty:

        recent = contacts.head(8).copy()

        recent["Sentiment"] = (
            recent["Sentiment"].apply(show_sentiment)
        )

        st.dataframe(
            recent[
                [
                    "Contact ID",
                    "Customer",
                    "Issue",
                    "Priority",
                    "Sentiment",
                    "Status"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Register your first customer contact.")


# ==========================================
# 2. CUSTOMER MANAGEMENT
# ==========================================

elif page == "Customers":

    st.title("Customer Management")

    st.caption(
        "Register customers and manage customer information."
    )

    st.subheader("Register New Customer")

    with st.form("customer_form"):

        name = st.text_input("Customer Name")

        email = st.text_input("Email Address")

        phone = st.text_input("Phone Number")

        submitted = st.form_submit_button(
            "Register Customer"
        )

        if submitted:

            if name.strip() and email.strip():

                result = add_customer(
                    name,
                    email,
                    phone
                )

                st.success(result)

            else:

                st.error(
                    "Customer name and email are required."
                )

    st.markdown("---")

    st.subheader("Customer Directory")

    customers = get_customers()

    if customers:

        customer_df = pd.DataFrame(
            customers,
            columns=[
                "Customer ID",
                "Name",
                "Email",
                "Phone"
            ]
        )

        search = st.text_input(
            "Search Customer"
        )

        if search:

            mask = customer_df.astype(str).apply(
                lambda col: col.str.contains(
                    search,
                    case=False,
                    na=False
                )
            ).any(axis=1)

            customer_df = customer_df[mask]

        st.dataframe(
            customer_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No customers registered yet.")


# ==========================================
# 3. AGENT MANAGEMENT
# ==========================================

elif page == "Agents":

    st.title("Agent Management")

    st.caption(
        "Register support agents and manage availability."
    )

    st.subheader("Register New Agent")

    with st.form("agent_form"):

        agent_name = st.text_input("Agent Name")

        submitted = st.form_submit_button(
            "Register Agent"
        )

        if submitted:

            if agent_name.strip():

                st.success(
                    add_agent(agent_name)
                )

            else:

                st.error("Please enter an agent name.")

    st.markdown("---")

    st.subheader("Agent Directory")

    agents = get_agents()

    if agents:

        agent_df = pd.DataFrame(
            agents,
            columns=[
                "Agent ID",
                "Agent Name",
                "Availability"
            ]
        )

        st.dataframe(
            agent_df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Update Agent Availability")

        agent_options = {
            f"{agent[1]} (ID: {agent[0]})": agent[0]
            for agent in agents
        }

        selected_agent = st.selectbox(
            "Select Agent",
            list(agent_options.keys())
        )

        new_status = st.selectbox(
            "Select Availability",
            ["Available", "Busy"]
        )

        if st.button("Update Availability"):

            result = update_agent_status(
                agent_options[selected_agent],
                new_status
            )

            st.success(result)

            st.rerun()

    else:

        st.info("No agents registered yet.")


# ==========================================
# 4. CONTACT CENTER
# ==========================================

elif page == "Contact Center":

    st.title("Contact Center")

    st.caption(
        "Manage Voice, Chat and Email customer interactions."
    )

    customers = get_customers()

    if not customers:

        st.warning(
            "Please register a customer before creating a contact."
        )

    else:

        customer_options = {
            f"{customer[1]} ({customer[2]})": customer[0]
            for customer in customers
        }

        st.subheader("Register New Contact")

        with st.form("contact_form"):

            selected_customer = st.selectbox(
                "Select Customer",
                list(customer_options.keys())
            )

            issue = st.text_area(
                "Customer Message / Issue",
                placeholder=(
                    "Example: I am unhappy because "
                    "my refund is delayed."
                )
            )

            channel = st.selectbox(
                "Contact Channel",
                ["Voice", "Chat", "Email"]
            )

            priority = st.selectbox(
                "Contact Priority",
                ["Low", "Medium", "High"],
                index=1
            )

            submitted = st.form_submit_button(
                "Register Contact"
            )

            if submitted:

                if issue.strip():

                    result = add_contact(
                        customer_options[selected_customer],
                        issue,
                        priority,
                        channel
                    )

                    st.success(result)

                else:

                    st.error(
                        "Please enter the customer message."
                    )

    st.markdown("---")

    st.subheader("Customer Contact Records")

    contacts = load_contacts()

    if not contacts.empty:

        status_filter = st.multiselect(
            "Filter by Status",
            ["Open", "In Progress", "Resolved"],
            default=[
                "Open",
                "In Progress",
                "Resolved"
            ]
        )

        filtered_contacts = contacts[
            contacts["Status"].isin(status_filter)
        ].copy()

        filtered_contacts["Sentiment"] = (
            filtered_contacts["Sentiment"].apply(show_sentiment)
        )

        st.dataframe(
            filtered_contacts,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Update Contact Status")

        contact_ids = contacts["Contact ID"].tolist()

        selected_contact = st.selectbox(
            "Select Contact ID",
            contact_ids
        )

        new_status = st.selectbox(
            "Select New Status",
            ["Open", "In Progress", "Resolved"]
        )

        if st.button("Update Contact Status"):

            result = update_contact_status(
                int(selected_contact),
                new_status
            )

            st.success(result)

            st.rerun()

    else:

        st.info("No contacts registered yet.")


# ==========================================
# 5. SMART ROUTING
# ==========================================

elif page == "Smart Routing":

    st.title("Smart Routing Engine")

    st.caption(
        "Prioritize customer issues using priority and "
        "sentiment-based routing rules."
    )

    queue = get_routing_queue()

    if queue:

        queue_df = pd.DataFrame(
            queue,
            columns=[
                "Contact ID",
                "Customer",
                "Issue",
                "Priority",
                "Sentiment",
                "Sentiment Score",
                "Created At"
            ]
        )

        st.subheader("Unassigned Contact Queue")

        st.dataframe(
            queue_df,
            use_container_width=True,
            hide_index=True
        )

        st.info(
            "Queue order: High priority first, then negative "
            "sentiment, then older contacts."
        )

        contact_ids = [
            contact[0] for contact in queue
        ]

        selected_contact = st.selectbox(
            "Select Contact to Assign",
            contact_ids
        )

        if st.button("Assign Selected Contact"):

            result = assign_agent(
                int(selected_contact)
            )

            st.success(result)

            st.rerun()

        if st.button("Route Next Highest Priority Contact"):

            result = route_next_contact()

            st.success(result)

            st.rerun()

    else:

        st.success(
            "No unassigned active contacts in the queue."
        )

    st.markdown("---")

    st.subheader("Agent Availability")

    agents = get_agents()

    if agents:

        agent_df = pd.DataFrame(
            agents,
            columns=[
                "Agent ID",
                "Agent Name",
                "Availability"
            ]
        )

        st.dataframe(
            agent_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("Register agents to enable routing.")


# ==========================================
# 6. REPORTS AND ANALYTICS
# ==========================================

elif page == "Reports & Analytics":

    st.title("Reports & Analytics")

    st.caption(
        "Understand customer interactions and service trends."
    )

    contacts = load_contacts()

    if contacts.empty:

        st.info(
            "Register customer contacts to generate reports."
        )

    else:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Contacts by Priority")

            priority_data = (
                contacts["Priority"]
                .value_counts()
                .rename_axis("Priority")
                .reset_index(name="Count")
            )

            fig = px.bar(
                priority_data,
                x="Priority",
                y="Count",
                color="Priority",
                color_discrete_sequence=[
                    "#142D4E",
                    "#2563EB",
                    "#93C5FD"
                ]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader("Contacts by Channel")

            channel_data = (
                contacts["Channel"]
                .value_counts()
                .rename_axis("Channel")
                .reset_index(name="Count")
            )

            fig = px.pie(
                channel_data,
                names="Channel",
                values="Count",
                hole=0.4,
                color_discrete_sequence=[
                    "#142D4E",
                    "#2563EB",
                    "#93C5FD"
                ]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.subheader("Customer Sentiment Distribution")

        sentiment_data = (
            contacts["Sentiment"]
            .value_counts()
            .rename_axis("Sentiment")
            .reset_index(name="Count")
        )

        fig = px.bar(
            sentiment_data,
            x="Sentiment",
            y="Count",
            color="Sentiment",
            color_discrete_sequence=[
                "#2563EB",
                "#F59E0B",
                "#94A3B8"
            ]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Sentiment Score Details")

        st.dataframe(
            contacts[
                [
                    "Contact ID",
                    "Customer",
                    "Sentiment",
                    "Sentiment Score"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader("Export Contact Report")

        csv_data = contacts.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Contact Report CSV",
            data=csv_data,
            file_name="connectpro_contact_report.csv",
            mime="text/csv"
        )


# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.caption(
    "ConnectPro | Customer Experience Platform | "
    "Python • Streamlit • SQLite • VADER NLP • Plotly"
)

st.caption(
    "Educational local simulation inspired by Amazon Connect. "
    "Not connected to live Amazon Connect services."
)
