import os
from datetime import datetime

import altair as alt
import pandas as pd
import requests
import streamlit as st

# Configuration
backend_url = os.getenv("BACKEND_URL", "http://backend_api:8000")
st.set_page_config(
    page_title="Prescription Data Extractor",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        font-weight: 500;
    }
    .prescription-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .highlight {
        background-color: #f0f7ff;
        padding: 2px 5px;
        border-radius: 3px;
        font-weight: 500;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        font-weight: 500;
    }
    .error-msg {
        color: #d32f2f;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffebee;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Session state initialization
if "prescription_history" not in st.session_state:
    st.session_state.prescription_history = []
if "current_prescription" not in st.session_state:
    st.session_state.current_prescription = None
if "backend_status" not in st.session_state:
    st.session_state.backend_status = None


def check_backend_health():
    """Check if the backend API is accessible."""
    try:
        response = requests.get(f"{backend_url}/health", timeout=5)
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False


def process_prescription(text):
    """Send text to backend for processing and return structured data."""
    try:
        response = requests.post(
            f"{backend_url}/process_text/", json={"text": text}, timeout=10
        )

        if response.status_code == 200:
            prescription_data = response.json()

            # Add to history
            st.session_state.prescription_history.append(
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data": prescription_data,
                }
            )

            # Set as current prescription
            st.session_state.current_prescription = prescription_data

            return prescription_data, None
        else:
            error_msg = f"Error: {response.status_code} - {response.text}"
            return None, error_msg

    except requests.RequestException as e:
        return None, f"Connection error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def display_prescription_card(prescription):
    """Display a formatted prescription card."""
    with st.container():
        st.markdown('<div class="prescription-card">', unsafe_allow_html=True)

        # Header with Rx info
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(
                f"<h3>Patient: {prescription['patient_name']}</h3>",
                unsafe_allow_html=True,
            )
            if prescription["patient_dob"]:
                st.markdown(f"DOB: {prescription['patient_dob']}")
        with col2:
            st.markdown(f"Date: {prescription['date_written']}")
            if prescription["rx_number"]:
                st.markdown(f"Rx #: {prescription['rx_number']}")

        st.divider()

        # Medication details
        st.markdown("<h4>Medication</h4>", unsafe_allow_html=True)
        medication = prescription["medication"]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<span class='highlight'>{medication['name']}</span> {medication['strength']}, {medication['form']}",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(f"Quantity: {medication['quantity']}")

        # Dosage instructions
        dosage = prescription["dosage"]
        st.markdown(f"<b>Sig:</b> {dosage['frequency']}", unsafe_allow_html=True)

        if dosage["duration"]:
            st.markdown(f"Duration: {dosage['duration']}")
        if dosage["special_instructions"]:
            st.markdown(
                f"<i>{dosage['special_instructions']}</i>", unsafe_allow_html=True
            )

        st.divider()

        # Prescriber info and refills
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"<b>Prescriber:</b> {prescription['prescriber_name']}",
                unsafe_allow_html=True,
            )
            if prescription["prescriber_id"]:
                st.markdown(f"ID: {prescription['prescriber_id']}")
        with col2:
            st.markdown(
                f"<b>Refills:</b> {prescription['refills']}", unsafe_allow_html=True
            )
            if prescription["is_controlled_substance"]:
                st.markdown("⚠️ **CONTROLLED SUBSTANCE**", unsafe_allow_html=True)

        # Notes if present
        if prescription["notes"]:
            st.divider()
            st.markdown(
                f"<i>Notes: {prescription['notes']}</i>", unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)


def display_history_chart():
    """Display a chart of prescription history."""
    if not st.session_state.prescription_history:
        return

    # Extract data for visualization
    data = []
    for entry in st.session_state.prescription_history:
        rx = entry["data"]
        data.append(
            {
                "timestamp": entry["timestamp"],
                "patient": rx["patient_name"],
                "medication": rx["medication"]["name"],
                "is_controlled": rx["is_controlled_substance"],
            }
        )

    df = pd.DataFrame(data)

    # Simple bar chart of medications
    med_counts = df["medication"].value_counts().reset_index()
    med_counts.columns = ["Medication", "Count"]

    chart = (
        alt.Chart(med_counts)
        .mark_bar()
        .encode(
            x=alt.X("Medication", sort="-y"),
            y="Count",
            color=alt.Color("Medication", legend=None),
        )
        .properties(title="Medications Processed", height=300)
    )

    st.altair_chart(chart, use_container_width=True)


def main():
    # Check backend health
    st.session_state.backend_status = check_backend_health()

    # Sidebar
    with st.sidebar:
        st.markdown('<p class="sub-header">Configuration</p>', unsafe_allow_html=True)

        # Backend status indicator
        if st.session_state.backend_status:
            st.success("Backend API: Connected")
        else:
            st.error("Backend API: Disconnected")
            st.warning(f"Attempting to connect to: {backend_url}")

        st.divider()

        # History section
        st.markdown('<p class="sub-header">History</p>', unsafe_allow_html=True)
        if st.session_state.prescription_history:
            history_count = len(st.session_state.prescription_history)
            st.info(f"{history_count} prescriptions processed")

            if st.button("Clear History"):
                st.session_state.prescription_history = []
                st.session_state.current_prescription = None
                st.rerun()

            # Show history visualization
            display_history_chart()
        else:
            st.info("No prescriptions processed yet")

    # Main content
    st.markdown(
        '<p class="main-header">Prescription Data Extractor</p>', unsafe_allow_html=True
    )
    st.markdown("Extract structured data from prescription text using AI")

    # Prescription input
    st.markdown(
        '<p class="sub-header">Enter Prescription Text</p>', unsafe_allow_html=True
    )

    # Example button
    if st.button("Load Example"):
        example_text = """
        Dr. Sarah Johnson, MD (NPI: 1234567890)
        Health First Medical Center
        123 Medical Parkway, Suite 300
        
        Patient: John Smith
        DOB: 05/12/1975
        Date: 2023-10-15
        
        Rx #: 7890123
        
        Lisinopril 10mg Tablet
        Disp: 30 tablets
        Sig: Take 1 tablet by mouth once daily for hypertension
        
        Refills: 3
        
        Electronically signed by Dr. Sarah Johnson, MD
        """
        st.session_state.example_text = example_text

    # Text input area
    input_text = st.text_area(
        "Paste prescription text here:",
        value=st.session_state.get("example_text", ""),
        height=200,
    )

    # Process button
    process_col, clear_col = st.columns([1, 4])
    with process_col:
        process_button = st.button(
            "Extract Data", type="primary", disabled=not st.session_state.backend_status
        )
    with clear_col:
        if st.button("Clear"):
            st.session_state.example_text = ""
            st.rerun()

    # Process text when button is clicked
    if process_button:
        if not input_text:
            st.warning("Please enter prescription text.")
        else:
            with st.spinner("Processing prescription..."):
                prescription_data, error = process_prescription(input_text)

                if error:
                    st.markdown(
                        f'<div class="error-msg">{error}</div>', unsafe_allow_html=True
                    )
                elif prescription_data:
                    st.success("Prescription data extracted successfully!")

    # Display current prescription if available
    if st.session_state.current_prescription:
        st.markdown(
            '<p class="sub-header">Extracted Prescription Data</p>',
            unsafe_allow_html=True,
        )

        tabs = st.tabs(["Card View", "JSON Data", "Database Preview"])

        with tabs[0]:
            display_prescription_card(st.session_state.current_prescription)

        with tabs[1]:
            st.json(st.session_state.current_prescription)

        with tabs[2]:
            st.markdown("### Database Storage Preview")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### prescriptions table")
                prescription = st.session_state.current_prescription
                prescription_df = pd.DataFrame(
                    [
                        {
                            "id": 1,
                            "rx_number": prescription.get("rx_number", ""),
                            "date_written": prescription.get("date_written", ""),
                            "patient_name": prescription.get("patient_name", ""),
                            "prescriber_name": prescription.get("prescriber_name", ""),
                            "refills": prescription.get("refills", 0),
                            "is_controlled": prescription.get(
                                "is_controlled_substance", False
                            ),
                        }
                    ]
                )
                st.dataframe(prescription_df, use_container_width=True)

            with col2:
                st.markdown("#### medication_details table")
                medication_df = pd.DataFrame(
                    [
                        {
                            "id": 1,
                            "name": prescription["medication"]["name"],
                            "strength": prescription["medication"]["strength"],
                            "form": prescription["medication"]["form"],
                            "quantity": prescription["medication"]["quantity"],
                        }
                    ]
                )
                st.dataframe(medication_df, use_container_width=True)


if __name__ == "__main__":
    main()
