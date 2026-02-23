#import libraries
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
  page_title="Sales Performance",
  page_icon="📊",
  layout="wide"
)

#load_dataset
@st.cache_data
def load_data():
  df = pd.read_csv("cleaned_sales_performance.csv")
  
  return df

df = load_data()

def main():
  #sidebar
  st.sidebar.title("📊 Sales Performance")
  st.sidebar.markdown("---")
  st.sidebar.subheader("Filter Options")

  region_filter = st.sidebar.selectbox(
    "Select Region:",
    options=["All Regions"] + sorted(df['region'].unique().tolist())
  )

  year_filter = st.sidebar.selectbox(
    "Select Years:",
    options=["All Years"] + sorted(df['year'].unique().tolist())
  )

  product_filter = st.sidebar.multiselect(
    "Select Products:",
    options=df['product'].unique().tolist(),
    default=df['product'].unique().tolist()
  )

  #filter data
  filtered_data = df.copy()
  if filtered_data != "All Regions":
    filtered_data = filtered_data[filtered_data['region'] == region_filter]
  
  if filtered_data != "All Years":
    filtered_data = filtered_data[filtered_data['year'] == year_filter]
  
  if product_filter:
    filtered_data = filtered_data[filtered_data['year'].isin(product_filter)]

if __name__ == "__main__":
  main()


