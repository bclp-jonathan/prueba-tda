import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="World Explorer 🌍", layout="wide")

st.title("🌍 World Explorer App")
st.markdown("Explore countries with visual insights powered by the [REST Countries API](https://restcountries.com/)")

@st.cache_data
def load_data():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    data = response.json()
    return data

data = load_data()

# Parse data into DataFrame
def create_dataframe(data):
    records = []
    for country in data:
        records.append({
            "Name": country.get("name", {}).get("common"),
            "Region": country.get("region"),
            "Subregion": country.get("subregion"),
            "Population": country.get("population"),
            "Area": country.get("area"),
            "Languages": list(country.get("languages", {}).values()) if "languages" in country else [],
            "Capital": ", ".join(country.get("capital", [])) if "capital" in country else "N/A",
            "Flag": country.get("flags", {}).get("png"),
        })
    return pd.DataFrame(records)

df = create_dataframe(data)

# --- Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔎 Country Details", "📊 Population Top 10", "🌍 Regions", "🗣️ Languages", "⚖️ Compare Countries"])

# --- Tab 1: Country Details
with tab1:
    st.subheader("🔎 Country Details")
    country_name = st.selectbox("Select a country", df["Name"].sort_values())
    country_info = df[df["Name"] == country_name].iloc[0]
    
    st.image(country_info["Flag"], width=100)
    st.markdown(f"**Capital**: {country_info['Capital']}")
    st.markdown(f"**Region**: {country_info['Region']} / {country_info['Subregion']}")
    st.markdown(f"**Population**: {country_info['Population']:,}")
    st.markdown(f"**Area**: {country_info['Area']:,} km²")
    st.markdown(f"**Languages**: {', '.join(country_info['Languages']) if country_info['Languages'] else 'N/A'}")

# --- Tab 2: Population Top 10
with tab2:
    st.subheader("📊 Top 10 Most Populous Countries")
    top_pop = df.nlargest(10, "Population")
    fig_pop = px.bar(top_pop, x="Name", y="Population", text="Population", color="Population",
                     color_continuous_scale="Viridis", title="Top 10 Countries by Population")
    st.plotly_chart(fig_pop, use_container_width=True)

# --- Tab 3: Region Distribution
with tab3:
    st.subheader("🌍 Number of Countries per Region")
    region_counts = df["Region"].value_counts().reset_index()
    region_counts.columns = ["Region", "Count"]
    fig_region = px.pie(region_counts, names="Region", values="Count", title="World Regions by Country Count")
    st.plotly_chart(fig_region, use_container_width=True)

# --- Tab 4: Top Languages
with tab4:
    st.subheader("🗣️ Top Spoken Languages (
