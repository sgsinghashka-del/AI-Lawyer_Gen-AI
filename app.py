import streamlit as st
import pandas as pd
import os

from datetime import datetime
from PyPDF2 import PdfReader


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Lawyer",
    layout="wide",
    page_icon="⚖️"
)


# =========================
# CUSTOM CSS
# =========================

st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }

    .stButton button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(135deg, #111827, #7c3aed);
        color: white;
        border: none;
        padding: 10px;
        font-weight: 600;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox div,
    .stMultiSelect div {
        border-radius: 10px;
    }

    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }

    .notice-box {
        background: #ffffff;
        padding: 25px;
        border-radius: 14px;
        border-left: 6px solid #7c3aed;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        line-height: 1.8;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# FILE PATHS
# =========================

LEGAL_FILE = "legal.csv"
CASE_FILE = "case_history.csv"


# =========================
# SESSION STATE
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "matched_results" not in st.session_state:
    st.session_state.matched_results = []


# =========================
# CSV FUNCTIONS
# =========================

def load_legal_data():

    if os.path.exists(LEGAL_FILE):
        return pd.read_csv(LEGAL_FILE)

    return pd.DataFrame(
        columns=[
            "keyword",
            "section",
            "law_type",
            "category",
            "punishment",
            "bailable",
            "court",
            "action_required",
            "description"
        ]
    )


def load_case_history():

    if os.path.exists(CASE_FILE):
        return pd.read_csv(CASE_FILE)

    return pd.DataFrame(
        columns=[
            "case_id",
            "date",
            "client_name",
            "case_type",
            "priority",
            "status",
            "matched_section",
            "case_score"
        ]
    )


def save_case_history(data):

    data.to_csv(
        CASE_FILE,
        index=False
    )


def generate_case_id(history):

    if history.empty:
        return "CASE001"

    last_id = history.iloc[-1]["case_id"]
    number = int(last_id.replace("CASE", "")) + 1

    return f"CASE{number:03d}"


# =========================
# LOGIN PAGE
# =========================

def login_page():

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:

        st.markdown("## ⚖️ AI Lawyer Login")
        st.caption("Secure Legal Case Management System")

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if username == "admin" and password == "admin123":

                st.session_state.logged_in = True
                st.rerun()

            else:

                st.error("Invalid username or password")


# =========================
# MATCH LEGAL SECTION
# =========================

def find_legal_matches(user_problem, legal_data):

    text = user_problem.lower()

    matches = []

    for index, row in legal_data.iterrows():

        keyword = str(row["keyword"]).lower()

        if keyword in text:

            matches.append(row)

    return matches


# =========================
# PDF READING
# =========================

def read_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    pdf_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pdf_text += text + "\\n"

    return pdf_text


# =========================
# DASHBOARD
# =========================

def dashboard():

    legal_data = load_legal_data()
    case_history = load_case_history()

    # Sidebar
    st.sidebar.title("⚖️ AI Lawyer")
    st.sidebar.caption("Real-Time CSV Legal System")
    st.sidebar.success("Admin Logged In")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "New Case",
            "Legal Search",
            "Case History",
            "Legal Database",
            "Analytics"
        ]
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()


    # =========================
    # NEW CASE PAGE
    # =========================

    if menu == "New Case":

        st.title("AI Lawyer Dashboard")
        st.caption("Create, analyze, and store legal case details using CSV database")

        total_cases = len(case_history)
        open_cases = len(case_history[case_history["status"] == "Open"]) if not case_history.empty else 0
        pending_cases = len(case_history[case_history["status"] == "Pending"]) if not case_history.empty else 0

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Cases", total_cases)
        c2.metric("Open Cases", open_cases)
        c3.metric("Pending Cases", pending_cases)

        st.divider()

        left, right = st.columns([1.2, 1])

        with left:

            st.write("## Client Case Form")

            user_name = st.text_input("Client Name")

            mobile = st.text_input("Mobile Number")

            case_type = st.selectbox(
                "Case Type",
                [
                    "Property Case",
                    "Cyber Crime",
                    "Family Case",
                    "Money Dispute",
                    "Business Issues",
                    "Criminal Case",
                    "Employment Case",
                    "Other"
                ]
            )

            priority = st.selectbox(
                "Priority",
                [
                    "Low",
                    "Medium",
                    "High"
                ]
            )

            user_problem = st.text_area(
                "Legal Problem",
                height=160
            )

            evidence = st.multiselect(
                "Available Evidence",
                [
                    "Written Agreement",
                    "Payment Proof",
                    "Chat Screenshot",
                    "Witness",
                    "Police Complaint",
                    "Legal Document",
                    "Call Recording",
                    "Email Proof",
                    "Video Proof",
                    "Bank Statement",
                    "CCTV Footage"
                ]
            )

            uploaded_file = st.file_uploader(
                "Upload PDF Document",
                type=["pdf"]
            )

        with right:

            st.write("## Real-Time Case Preview")

            st.info("Client preview will appear after submission.")

            if uploaded_file:

                st.success(f"Uploaded File: {uploaded_file.name}")

                pdf_text = read_pdf(uploaded_file)

                with st.expander("View Extracted PDF Text"):
                    st.write(pdf_text)

        st.divider()

        submit_col, section_col, notice_col = st.columns(3)

        with submit_col:

            submit_case = st.button("Submit Case")

        with section_col:

            find_section = st.button("Find Legal Sections")

        with notice_col:

            generate_notice = st.button("Generate Notice")


        if find_section:

            matches = find_legal_matches(
                user_problem,
                legal_data
            )

            st.session_state.matched_results = matches

            if matches:

                st.write("## Matched Legal Sections")

                for row in matches:

                    with st.container():

                        st.success(row["section"])

                        st.write("Law Type:", row["law_type"])
                        st.write("Category:", row["category"])
                        st.write("Punishment:", row["punishment"])
                        st.write("Bailable:", row["bailable"])
                        st.write("Court:", row["court"])
                        st.write("Action Required:", row["action_required"])
                        st.write("Description:", row["description"])

                        st.divider()

            else:

                st.warning("No matching legal section found.")


        if generate_notice:

            st.write("## Legal Notice Draft")

            st.markdown(
                f"""
                <div class="notice-box">

                <b>Date:</b> {datetime.now().date()} <br><br>

                <b>To,</b><br>
                Concerned Party<br><br>

                <b>Subject:</b> Legal Notice Regarding {case_type}<br><br>

                This legal notice is prepared on behalf of <b>{user_name}</b>. 
                The matter is related to <b>{case_type}</b>. 
                The case priority is marked as <b>{priority}</b>.<br><br>

                <b>Issue Details:</b><br>
                {user_problem}<br><br>

                <b>Evidence Available:</b><br>
                {", ".join(evidence) if evidence else "No evidence selected"}<br><br>

                You are hereby requested to resolve this matter within the legally appropriate time period. 
                If the matter is not resolved, the client may proceed with further legal action as advised by a legal professional.<br><br>

                <b>Generated By:</b><br>
                AI Lawyer System

                </div>
                """,
                unsafe_allow_html=True
            )


        if submit_case:

            matches = find_legal_matches(
                user_problem,
                legal_data
            )

            matched_section = matches[0]["section"] if matches else "Not Found"

            score = len(evidence) * 10

            if priority == "High":
                score += 20

            elif priority == "Medium":
                score += 10

            new_case = {
                "case_id": generate_case_id(case_history),
                "date": datetime.now().date(),
                "client_name": user_name,
                "case_type": case_type,
                "priority": priority,
                "status": "Open",
                "matched_section": matched_section,
                "case_score": score
            }

            case_history = pd.concat(
                [
                    case_history,
                    pd.DataFrame([new_case])
                ],
                ignore_index=True
            )

            save_case_history(case_history)

            st.success("Case saved successfully in case_history.csv")
            st.write("Case ID:", new_case["case_id"])
            st.write("Matched Section:", matched_section)
            st.write("Case Score:", score)


    # =========================
    # LEGAL SEARCH PAGE
    # =========================

    elif menu == "Legal Search":

        st.title("Legal Section Search")

        search_text = st.text_input(
            "Search by keyword, section, category, or law type"
        )

        if search_text:

            result = legal_data[
                legal_data.apply(
                    lambda row: search_text.lower() in row.astype(str).str.lower().to_string(),
                    axis=1
                )
            ]

            st.dataframe(
                result,
                use_container_width=True
            )

        else:

            st.dataframe(
                legal_data,
                use_container_width=True
            )


    # =========================
    # CASE HISTORY PAGE
    # =========================

    elif menu == "Case History":

        st.title("Case History")

        status_filter = st.selectbox(
            "Filter By Status",
            [
                "All",
                "Open",
                "Pending",
                "Closed"
            ]
        )

        if status_filter != "All":

            filtered_data = case_history[
                case_history["status"] == status_filter
            ]

        else:

            filtered_data = case_history

        st.dataframe(
            filtered_data,
            use_container_width=True
        )


    # =========================
    # LEGAL DATABASE PAGE
    # =========================

    elif menu == "Legal Database":

        st.title("Legal CSV Database")

        st.dataframe(
            legal_data,
            use_container_width=True
        )

        st.download_button(
            "Download legal.csv",
            legal_data.to_csv(index=False),
            "legal.csv",
            "text/csv"
        )


    # =========================
    # ANALYTICS PAGE
    # =========================

    elif menu == "Analytics":

        st.title("Case Analytics")

        if case_history.empty:

            st.warning("No case history available.")

        else:

            c1, c2, c3 = st.columns(3)

            c1.metric("Total Cases", len(case_history))
            c2.metric("Average Score", round(case_history["case_score"].mean(), 2))
            c3.metric("Highest Score", case_history["case_score"].max())

            st.write("## Cases By Type")

            st.bar_chart(
                case_history["case_type"].value_counts()
            )

            st.write("## Cases By Priority")

            st.bar_chart(
                case_history["priority"].value_counts()
            )


# =========================
# APP START
# =========================

if st.session_state.logged_in:
    dashboard()
else:
    login_page()
