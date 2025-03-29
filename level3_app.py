import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("""
    <style>
    /* Change the color of most text elements */
    .css-12oz5g7, .css-1cpxqw2, .css-18e3th9, body {
        color: #FAFAFA !important;
    }
    /* Adjust sidebar text color */
    .sidebar-content, .css-1d391kg {
        color: #FAFAFA !important;
    }
    </style>
""", unsafe_allow_html=True)



@st.cache_data
def load_data():
    df = pd.read_csv("data/processed_crime_data.csv")
    return df

def main():
    st.title("Level 3 - Rihal CityX Crime Dashboard")
    st.markdown("### Interactive Dashboard for Crime Analysis in CityX by Mohd Saif Ali")
    

    st.sidebar.header("Filter Options")
    
    data = load_data()
    
    # Filter by Severity Level (allowing multiple selections)
    severity_options = sorted(data['Severity'].unique())
    selected_severity = st.sidebar.multiselect("Select Severity Level(s):", 
                                               severity_options, default=severity_options)
    
    # Filter by Crime Category
    category_options = sorted(data['Category'].unique())
    selected_categories = st.sidebar.multiselect("Select Crime Category(ies):", 
                                                 category_options, default=category_options)
    
    # Filter by Year
    year_options = sorted(data['Year'].unique())
    selected_years = st.sidebar.multiselect("Select Year(s):", 
                                            year_options, default=year_options)
    
    # Apply filters to data
    filtered_data = data[
        (data['Severity'].isin(selected_severity)) & 
        (data['Category'].isin(selected_categories)) & 
        (data['Year'].isin(selected_years))
    ]
    
    st.sidebar.markdown("#### Filter Summary")
    st.sidebar.write(f"Total records: {len(filtered_data)}")

    st.subheader("Data Overview")
    st.write("Below is a sample of the filtered dataset:")
    st.dataframe(filtered_data.head(10))
    
    # Layout: Two columns for charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Crime Category Distribution")
        fig_cat = px.bar(
            filtered_data['Category'].value_counts().sort_values(ascending=False),
            title="Crime Category Counts",
            labels={'index':'Category', 'value':'Count'},
            template="plotly_white"
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        st.subheader("Severity Level Distribution")
        fig_sev = px.bar(
            filtered_data['Severity'].value_counts().sort_index(),
            title="Severity Level Counts",
            labels={'index':'Severity Level', 'value':'Count'},
            template="plotly_white"
        )
        st.plotly_chart(fig_sev, use_container_width=True)
    

    st.subheader("Crime Density Map")
    fig_map = px.density_mapbox(
        filtered_data,
        lat='Latitude',
        lon='Longitude',
        radius=5,
        center=dict(lat=filtered_data['Latitude'].mean(), 
                    lon=filtered_data['Longitude'].mean()),
        zoom=12,
        mapbox_style='open-street-map',
        hover_name='Category',
        hover_data=['Address', 'Severity'],
        title='CityX Crime Density'
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
if __name__ == "__main__":
    main()
