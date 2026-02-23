import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

# Load data
df = pd.read_csv('cleaned_sales_performance.csv')
df['purchase_date'] = pd.to_datetime(df['purchase_date'])

# Initialize app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# KPI calculations
total_revenue = df['total_sales'].sum()
total_orders = len(df)
avg_order_value = df['total_sales'].mean()
total_customers = df['customer_id'].nunique()

# Sidebar
sidebar = html.Div(
    [
        html.H2("Sales Dashboard", className="text-white mb-4"),
        html.Hr(className="bg-white"),
        html.P("Filter Options", className="text-white-50 mb-3"),
        
        html.Label("Select Region:", className="text-white mb-2"),
        dcc.Dropdown(
            id='region-filter',
            options=[{'label': 'All Regions', 'value': 'all'}] + 
                    [{'label': region.title(), 'value': region} for region in df['region'].unique()],
            value='all',
            className="mb-3"
        ),
        
        html.Label("Select Year:", className="text-white mb-2"),
        dcc.Dropdown(
            id='year-filter',
            options=[{'label': 'All Years', 'value': 'all'}] + 
                    [{'label': str(year), 'value': year} for year in sorted(df['year'].unique())],
            value='all',
            className="mb-3"
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#2c3e50",
    }
)

# Main content
content = html.Div(
    [
        # KPI Cards
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Total Revenue", className="card-title text-muted"),
                            html.H2(id="kpi-revenue", className="text-primary")
                        ])
                    ], className="shadow-sm"),
                    width=3
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Total Orders", className="card-title text-muted"),
                            html.H2(id="kpi-orders", className="text-success")
                        ])
                    ], className="shadow-sm"),
                    width=3
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Avg Order Value", className="card-title text-muted"),
                            html.H2(id="kpi-avg", className="text-info")
                        ])
                    ], className="shadow-sm"),
                    width=3
                ),
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Total Customers", className="card-title text-muted"),
                            html.H2(id="kpi-customers", className="text-warning")
                        ])
                    ], className="shadow-sm"),
                    width=3
                ),
            ],
            className="mb-4"
        ),
        
        # Charts Row 1
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='sales-by-region'), width=6),
                dbc.Col(dcc.Graph(id='sales-trend'), width=6),
            ],
            className="mb-4"
        ),
        
        # Charts Row 2
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='product-performance'), width=6),
                dbc.Col(dcc.Graph(id='customer-segments'), width=6),
            ],
            className="mb-4"
        ),
    ],
    style={"margin-left": "18rem", "margin-right": "2rem", "padding": "2rem 1rem"}
)

app.layout = html.Div([sidebar, content])

# Callbacks
@callback(
    [Output('kpi-revenue', 'children'),
     Output('kpi-orders', 'children'),
     Output('kpi-avg', 'children'),
     Output('kpi-customers', 'children'),
     Output('sales-by-region', 'figure'),
     Output('sales-trend', 'figure'),
     Output('product-performance', 'figure'),
     Output('customer-segments', 'figure')],
    [Input('region-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_dashboard(region, year):
    # Filter data
    filtered_df = df.copy()
    if region != 'all':
        filtered_df = filtered_df[filtered_df['region'] == region]
    if year != 'all':
        filtered_df = filtered_df[filtered_df['year'] == year]
    
    # Update KPIs
    revenue = f"${filtered_df['total_sales'].sum():,.2f}"
    orders = f"{len(filtered_df):,}"
    avg_value = f"${filtered_df['total_sales'].mean():,.2f}"
    customers = f"{filtered_df['customer_id'].nunique():,}"
    
    # Sales by Region
    region_sales = filtered_df.groupby('region')['total_sales'].sum().reset_index()
    fig_region = px.pie(region_sales, values='total_sales', names='region', 
                        title='Sales by Region',
                        color_discrete_sequence=px.colors.qualitative.Set3)
    
    # Sales Trend
    trend_data = filtered_df.groupby('purchase_date')['total_sales'].sum().reset_index()
    fig_trend = px.line(trend_data, x='purchase_date', y='total_sales',
                        title='Sales Trend Over Time',
                        labels={'total_sales': 'Sales ($)', 'purchase_date': 'Date'})
    fig_trend.update_traces(line_color='#3498db', line_width=3)
    
    # Product Performance
    product_sales = filtered_df.groupby('product')['total_sales'].sum().sort_values(ascending=True).reset_index()
    fig_product = px.bar(product_sales, x='total_sales', y='product',
                         title='Product Performance',
                         labels={'total_sales': 'Total Sales ($)', 'product': 'Product'},
                         orientation='h',
                         color='total_sales',
                         color_continuous_scale='Blues')
    
    # Customer Segments
    segment_data = filtered_df.groupby('age_group')['total_sales'].sum().reset_index()
    fig_segment = px.bar(segment_data, x='age_group', y='total_sales',
                         title='Sales by Customer Segment',
                         labels={'total_sales': 'Total Sales ($)', 'age_group': 'Age Group'},
                         color='total_sales',
                         color_continuous_scale='Viridis')
    
    return revenue, orders, avg_value, customers, fig_region, fig_trend, fig_product, fig_segment

if __name__ == '__main__':
    app.run(debug=True)
