import streamlit as st
import pandas as pd
import plotly.express as px
import pdfplumber
import re
import pickle
import numpy as np
from datetime import datetime
from scipy.sparse import hstack

@st.cache_resource
def load_model_artifacts():
    model = pickle.load(open("best_model.pkl", "rb"))
    tfidf_vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
    onehot_encoder = pickle.load(open("onehot_encoder.pkl", "rb"))
    return model, tfidf_vectorizer, onehot_encoder

def assign_severity(category):
    severity_map = {
        1: ['NON-CRIMINAL', 'SUSPICIOUS OCCURRENCE', 'MISSING PERSON', 'RUNAWAY', 'RECOVERED VEHICLE'],
        2: ['WARRANTS', 'OTHER OFFENSES', 'VANDALISM', 'TRESPASS', 'DISORDERLY CONDUCT', 'BAD CHECKS'],
        3: ['LARCENY/THEFT', 'VEHICLE THEFT', 'FORGERY/COUNTERFEITING', 'DRUG/NARCOTIC',
            'STOLEN_PROPERTY', 'FRAUD', 'BRIBERY', 'EMBEZZLEMENT'],
        4: ['ROBBERY', 'WEAPON LAWS', 'BURGLARY', 'EXTORTION'],
        5: ['KIDNAPPING', 'ARSON']
    }
    for severity, categories in severity_map.items():
        if category in categories:
            return severity
    return None

def transform_new_data(parsed_report, tfidf_vectorizer, onehot_encoder):
    description_text = parsed_report.get('Detailed Description', '')
    X_text_vector = tfidf_vectorizer.transform([description_text])

    dt_str = parsed_report.get('Date & Time', '')
    try:
        dt_obj = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        year = dt_obj.year
        month = dt_obj.month
        hour = dt_obj.hour
        day_of_week = dt_obj.strftime('%A')
    except:
        year = 0
        month = 0
        hour = 0
        day_of_week = "Unknown"

    is_weekend = 1 if day_of_week in ['Saturday', 'Sunday'] else 0

    peak_hour = 1 if hour in [12, 17, 18] else 0

    loc_str = parsed_report.get('Incident Location', '')
    import re
    match_block = re.search(r'(\d+)\s*Block', loc_str, re.IGNORECASE)
    if match_block:
        address_block = int(match_block.group(1))
    else:
        address_block = 0

    coords_str = parsed_report.get('Coordinates', '')
    try:
        lat_str, lon_str = coords_str.split(',')
        lat = float(lat_str.strip())
        lon = float(lon_str.strip())
        lat_bin = int(pd.cut([lat], bins=20, labels=False)[0])
        lon_bin = int(pd.cut([lon], bins=20, labels=False)[0])
        geo_cluster = f"{lat_bin}_{lon_bin}"
    except:
        geo_cluster = "0_0"

    pd_district = parsed_report.get('Police District', 'Unknown')

    new_data = pd.DataFrame([{
        'Year': year,
        'Month': month,
        'Hour': hour,
        'IsWeekend': is_weekend,
        'PeakHour': peak_hour,
        'AddressBlock': address_block,
        'GeoCluster': geo_cluster,
        'PdDistrict': pd_district,
        'DayOfWeek': day_of_week
    }])

    X_new_encoded = onehot_encoder.transform(new_data)

    X_combined = hstack([X_text_vector, X_new_encoded])

    return X_combined

def predict_crime_and_severity_full(parsed_report, model, tfidf_vectorizer, onehot_encoder):
    X_combined = transform_new_data(parsed_report, tfidf_vectorizer, onehot_encoder)
    predicted_category = model.predict(X_combined)[0]
    predicted_severity = assign_severity(predicted_category)
    return predicted_category, predicted_severity

def parse_pdf_report(pdf_bytes):
    data_dict = {
        'Report Number': None,
        'Date & Time': None,
        'Incident Location': None,
        'Coordinates': None,
        'Detailed Description': None,
        'Police District': None,
        'Resolution': None
    }

    with pdfplumber.open(pdf_bytes) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            full_text += page_text + "\\n"

    report_num_match = re.search(r'Report Number:\s*(.*)', full_text)
    if report_num_match:
        data_dict['Report Number'] = report_num_match.group(1).strip()

    datetime_match = re.search(r'Date & Time:\s*(.*)', full_text)
    if datetime_match:
        data_dict['Date & Time'] = datetime_match.group(1).strip()

    location_match = re.search(r'Incident Location:\s*(.*)', full_text)
    if location_match:
        data_dict['Incident Location'] = location_match.group(1).strip()

    coord_match = re.search(r'Coordinates:\s*\(([^)]+)\)', full_text)
    if coord_match:
        data_dict['Coordinates'] = coord_match.group(1).strip()

    desc_match = re.search(r'Detailed Description:\s*(.*)\s*Police District:', full_text, re.DOTALL)
    if desc_match:
        data_dict['Detailed Description'] = desc_match.group(1).replace('\\n',' ').strip()

    district_match = re.search(r'Police District:\s*(.*)', full_text)
    if district_match:
        data_dict['Police District'] = district_match.group(1).split('\\n')[0].strip()

    resolution_match = re.search(r'Resolution:\s*(.*)', full_text)
    if resolution_match:
        data_dict['Resolution'] = resolution_match.group(1).split('\\n')[0].strip()

    return data_dict

@st.cache_data
def load_processed_data():
    df = pd.read_csv("processed_crime_data.csv")
    return df

def main():
    st.title("CityX Crime Dashboard")
    st.markdown("#### Unified Dashboard: Level 3 + Level 4 with OneHotEncoder by Mohd Saif Ali")

    data = load_processed_data()
    model, tfidf_vectorizer, onehot_encoder = load_model_artifacts()

    st.sidebar.header("Filter Options")

    severity_options = sorted(data['Severity'].dropna().unique())
    selected_severity = st.sidebar.multiselect("Select Severity Level(s):", 
                                               severity_options, default=severity_options)

    year_options = sorted(data['Year'].unique())
    selected_years = st.sidebar.multiselect("Select Year(s):", 
                                            year_options, default=year_options)

    filtered_data = data[
        (data['Severity'].isin(selected_severity)) &
        (data['Year'].isin(selected_years))
    ]

    st.subheader("Filtered Data Overview")
    st.write(f"Number of records: {len(filtered_data)}")
    st.dataframe(filtered_data.head(10))

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Crime Category Distribution")
        if not filtered_data.empty:
            fig_cat = px.bar(
                filtered_data['Category'].value_counts().sort_values(ascending=False),
                title="Crime Category Counts",
                labels={'index':'Category', 'value':'Count'},
                template="plotly_white"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.write("No data to display.")

    with col2:
        st.subheader("Severity Level Distribution")
        if not filtered_data.empty:
            fig_sev = px.bar(
                filtered_data['Severity'].value_counts().sort_index(),
                title="Severity Level Counts",
                labels={'index':'Severity Level', 'value':'Count'},
                template="plotly_white"
            )
            st.plotly_chart(fig_sev, use_container_width=True)
        else:
            st.write("No data to display.")

    st.subheader("Crime Density Map")
    if not filtered_data.empty:
        fig_map = px.density_mapbox(
            filtered_data,
            lat='Latitude',
            lon='Longitude',
            radius=5,
            center=dict(lat=filtered_data['Latitude'].mean(), lon=filtered_data['Longitude'].mean()),
            zoom=12,
            mapbox_style='open-street-map',
            hover_name='Category',
            hover_data=['Address','Severity'],
            title='CityX Crime Density'
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.write("No data available for the selected filters.")

    st.subheader("PDF Report Extraction & Classification")
    uploaded_pdf = st.file_uploader("Upload a Police Crime Report (PDF)", type=["pdf"])

    if uploaded_pdf is not None:
        parsed_report = parse_pdf_report(uploaded_pdf)
        st.write("**Extracted Fields:**")
        st.json(parsed_report)

        predicted_category, predicted_severity = predict_crime_and_severity_full(
            parsed_report, model, tfidf_vectorizer, onehot_encoder
        )

        st.markdown(f"**Predicted Crime Category:** {predicted_category}")
        if predicted_severity:
            st.markdown(f"**Assigned Severity:** {predicted_severity}")
        else:
            st.markdown("**Assigned Severity:** Could not determine (no matching category).")

if __name__ == "__main__":
    main()
