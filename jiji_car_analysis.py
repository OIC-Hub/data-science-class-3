import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title = "Jiji Car Analysis Dashboard",
    page_icon = "🚘",
    layout = "wide"
)
@st.cache_data
def load_data():
    df=pd.read_csv("jiji_cleaned_car_dataset")
    
    return df
df=load_data()

def main():
    st.sidebar.title("🚘 Jiji Car Analysis")
    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter Options")
    brand_filter = st.sidebar.selectbox(
        'Select Car Brand:',
        options=["All Car Brands"] + sorted(df['make'].unique().tolist())
    )
    condition_filter = st.sidebar.selectbox(
        "Select Condition of Car:",
        options=["All Condition"] + sorted(df['condition'].unique().tolist())
    )

    year_filter = st.sidebar.selectbox(
        "Select Years:",
        options=["All Years"] + sorted(df['year'].unique().tolist())
    )

    transmission_filter = st.sidebar.selectbox(
        "Select Transmission of Car:",
        options=['All Transmission'] + sorted(df['transmission'].unique().tolist())
    )
    
    filtered_data = df.copy()
    if brand_filter != "All Car Brands":
        filtered_data = filtered_data[filtered_data['make'] == brand_filter]
    if condition_filter != "All Condition":
        filtered_data = filtered_data[filtered_data['condition'] ==condition_filter]
    
    if year_filter != "All Years":
        filtered_data = filtered_data[filtered_data['year'] ==year_filter]
    
    if transmission_filter != "All Transmission":
        filtered_data = filtered_data[filtered_data['transmission'] ==transmission_filter]

    st.title("🚘 Jiji Car Analysis Dashboard")
    st.markdown("---")
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        total_cars = len(filtered_data)
        st.metric("🚘 Total Cars", f"{total_cars:,}")
    with col2:
        mean_price = filtered_data['price'].mean()
        st.metric("💵Average Car Price", f"{mean_price:,.0f}")
    with col3:
        most_common_car_make = filtered_data['make'].mode()[0]
        st.metric("🚗Most Listed Car Brand", f"{most_common_car_make}")
    with col4:
        foreign_used_percentage = filtered_data['condition'].value_counts(normalize=True)['Foreign Used'] * 100
        st.metric("Percentage of Foreign Used Cars", f"{foreign_used_percentage:.2f}%")

    st.markdown("---")

    col1,col2 = st.columns(2)
    with col1:
        brand_count = filtered_data['make'].value_counts().reset_index().head(10)
        brand_count.columns=['make', 'count']
        fig_count = px.bar(
        brand_count,
        x = 'make',
        y='count',
        labels={
            'Make':'Car Brand', 
            'Count':'Number of Cars'
            },
        title= "Count of Brand Cars",
        text='count'
        )
        st.plotly_chart(fig_count, use_container_width=True)
    with col2:
        Avg_price = filtered_data.groupby('make', as_index=False)['price'].mean().sort_values(by='price', ascending=False)
        Avg_price.columns = ['make', 'price']
        fig_avg_make_price = px.bar(
            Avg_price,
            x='price',
            y='make',
            orientation='h',
            labels = {'make': 'Car brand', 'price':'Price'},
            title= 'Average Price By Car Brands',
            text='price'

        )  
        st.plotly_chart(fig_avg_make_price, use_container_width=True)
    
    col1,col2=st.columns(2)
    with col1: 
        fig_price_distribution = px.box(
            filtered_data,
            x='condition',
            y='price',
            title='Price Distribution by Condition',

        )
        st.plotly_chart(fig_price_distribution, use_container_width=True)
    with col2: 
        fig_distribution_year = px.histogram(
            filtered_data,
            x='year',
            nbins=10,
            title= 'Price Distribution of Years'
        )
        st.plotly_chart(fig_distribution_year, use_container_width=True)
    st.markdown('---')

    col1, col2 = st.columns(2)
    with col1:
        fig_year_price_scatterplot = px.scatter(
            filtered_data,
            x='year',
            y='price',
            color='condition',
            title='Scatterplot of Year and Price of Cars',

        )
        st.plotly_chart(fig_year_price_scatterplot, use_container_width=True)
    with col2:
        corr = filtered_data[['price', 'year']].corr().round(2)
        fig_corr= px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title= 'Correlation between Year and Price'
        )
        st.plotly_chart(fig_corr, use_container_width=True)

if __name__ == "__main__":
    main()