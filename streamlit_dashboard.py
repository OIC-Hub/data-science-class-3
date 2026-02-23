import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(page_title="Sales Dashboard", layout="wide", page_icon="📊")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_sales_performance.csv')
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    return df

df = load_data()

# Sidebar
st.sidebar.header("📊 Sales Dashboard")
st.sidebar.markdown("---")
st.sidebar.subheader("Filter Options")

region_filter = st.sidebar.selectbox(
    "Select Region:",
    options=['All Regions'] + sorted(df['region'].unique().tolist())
)

year_filter = st.sidebar.selectbox(
    "Select Year:",
    options=['All Years'] + sorted(df['year'].unique().tolist())
)

product_filter = st.sidebar.multiselect(
    "Select Products:",
    options=df['product'].unique().tolist(),
    default=df['product'].unique().tolist()
)

# Filter data
filtered_df = df.copy()
if region_filter != 'All Regions':
    filtered_df = filtered_df[filtered_df['region'] == region_filter]
if year_filter != 'All Years':
    filtered_df = filtered_df[filtered_df['year'] == year_filter]
if product_filter:
    filtered_df = filtered_df[filtered_df['product'].isin(product_filter)]

# Main content
st.title("📈 Sales Performance Dashboard")
st.markdown("---")

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = filtered_df['total_sales'].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

with col2:
    total_orders = len(filtered_df)
    st.metric("Total Orders", f"{total_orders:,}")

with col3:
    avg_order_value = filtered_df['total_sales'].mean()
    st.metric("Avg Order Value", f"${avg_order_value:,.2f}")

with col4:
    total_customers = filtered_df['customer_id'].nunique()
    st.metric("Total Customers", f"{total_customers:,}")

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Region")
    region_sales = filtered_df.groupby('region')['total_sales'].sum().reset_index()
    fig_region = px.pie(
        region_sales, 
        values='total_sales', 
        names='region',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.4
    )
    fig_region.update_layout(height=400)
    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    st.subheader("Sales Trend Over Time")
    trend_data = filtered_df.groupby('purchase_date')['total_sales'].sum().reset_index()
    fig_trend = px.line(
        trend_data, 
        x='purchase_date', 
        y='total_sales',
        labels={'total_sales': 'Sales ($)', 'purchase_date': 'Date'}
    )
    fig_trend.update_traces(line_color='#3498db', line_width=3)
    fig_trend.update_layout(height=400)
    st.plotly_chart(fig_trend, use_container_width=True)

# Charts Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Product Performance")
    product_sales = filtered_df.groupby('product')['total_sales'].sum().sort_values(ascending=True).reset_index()
    fig_product = px.bar(
        product_sales, 
        x='total_sales', 
        y='product',
        labels={'total_sales': 'Total Sales ($)', 'product': 'Product'},
        orientation='h',
        color='total_sales',
        color_continuous_scale='Blues'
    )
    fig_product.update_layout(height=400)
    st.plotly_chart(fig_product, use_container_width=True)

with col2:
    st.subheader("Sales by Customer Segment")
    segment_data = filtered_df.groupby('age_group')['total_sales'].sum().reset_index()
    fig_segment = px.bar(
        segment_data, 
        x='age_group', 
        y='total_sales',
        labels={'total_sales': 'Total Sales ($)', 'age_group': 'Age Group'},
        color='total_sales',
        color_continuous_scale='Viridis'
    )
    fig_segment.update_layout(height=400)
    st.plotly_chart(fig_segment, use_container_width=True)

# Additional insights
st.markdown("---")
st.subheader("📋 Top Performing Products")

col1, col2 = st.columns(2)

with col1:
    top_products = filtered_df.groupby('product').agg({
        'total_sales': 'sum',
        'quantity': 'sum'
    }).sort_values('total_sales', ascending=False).reset_index()
    st.dataframe(top_products, use_container_width=True, hide_index=True)

with col2:
    st.subheader("Sales by Manager")
    manager_sales = filtered_df.groupby('manager')['total_sales'].sum().sort_values(ascending=False).reset_index()
    fig_manager = px.bar(
        manager_sales, 
        x='manager', 
        y='total_sales',
        labels={'total_sales': 'Total Sales ($)', 'manager': 'Manager'},
        color='total_sales',
        color_continuous_scale='Greens'
    )
    fig_manager.update_layout(height=300)
    st.plotly_chart(fig_manager, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Sales Performance Dashboard | Data updated in real-time")
