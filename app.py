import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1. Page Configuration & Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Marketing Campaign Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve aesthetics
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .stMetric label {
        font-size: 1.1rem !important;
        font-weight: 600;
    }
    .stMetric .css-1wivap2 {
        font-size: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. Data Loading & Preprocessing
# -----------------------------------------------------------------------------
@st.cache_data
def load_and_clean_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Please ensure the CSV file is in the same directory.")
        return None

    # --- Data Cleaning ---
    
    # 1. Handling Missing Values
    # Income often has nulls in this dataset. We'll impute with median or drop.
    # Dropping is safer for accurate analysis unless specific imputation strategy is required.
    df = df.dropna(subset=['Income'])

    # 2. Feature Engineering: Age
    # Assuming the dataset context is around 2014 (based on Dt_Customer max date)
    current_year = 2014 
    df['Age'] = current_year - df['Year_Birth']
    
    # 3. Feature Engineering: Total Spend
    products = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    df['Total_Spend'] = df[products].sum(axis=1)

    # 4. Feature Engineering: Total Campaigns Accepted
    campaigns = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Response']
    df['Total_Accepted_Campaigns'] = df[campaigns].sum(axis=1)

    # 5. Feature Engineering: Enrollment Duration (Tenure) in days
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%Y-%m-%d', errors='coerce')
    # If standard format fails, try inferring
    if df['Dt_Customer'].isnull().all():
         df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], dayfirst=True, errors='coerce')
         
    df['Tenure_Days'] = (pd.to_datetime(f"{current_year}-12-31") - df['Dt_Customer']).dt.days

    # 6. Cleaning Categorical Values for Better Visuals
    # Consolidate Marital Status
    df['Marital_Status'] = df['Marital_Status'].replace({
        'Married': 'Partner', 'Together': 'Partner',
        'Single': 'Single', 'Divorced': 'Single', 'Widow': 'Single', 'Alone': 'Single',
        'Absurd': 'Other', 'YOLO': 'Other'
    })
    
    # Consolidate Education
    df['Education'] = df['Education'].replace({
        'Basic': 'Undergraduate', '2n Cycle': 'Master', 
        'Graduation': 'Graduate', 'Master': 'Master', 'PhD': 'PhD'
    })

    # 7. Outlier Removal (Optional but recommended for Income/Age)
    df = df[df['Age'] < 100] 
    df = df[df['Income'] < 600000] 

    return df

# Load the data
# NOTE: Ensure 'marketing_campaign_data.csv' is in your folder
df = load_and_clean_data('marketing_campaign_data.csv')

if df is not None:
    # -----------------------------------------------------------------------------
    # 3. Sidebar Filters
    # -----------------------------------------------------------------------------
    st.sidebar.header("🔍 Filter Data")
    
    # Filter by Country (if exists) or Education
    if 'Country' in df.columns:
        selected_countries = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
        df_filtered = df[df['Country'].isin(selected_countries)]
    else:
        df_filtered = df

    # Filter by Education
    selected_education = st.sidebar.multiselect("Select Education", options=df['Education'].unique(), default=df['Education'].unique())
    df_filtered = df_filtered[df_filtered['Education'].isin(selected_education)]

    # Filter by Marital Status
    selected_marital = st.sidebar.multiselect("Select Marital Status", options=df['Marital_Status'].unique(), default=df['Marital_Status'].unique())
    df_filtered = df_filtered[df_filtered['Marital_Status'].isin(selected_marital)]

    # -----------------------------------------------------------------------------
    # 4. Main Dashboard UI
    # -----------------------------------------------------------------------------
    st.title("🚀 Marketing Campaign Analytics Dashboard")
    st.markdown("Analysing customer behavior, spending patterns, and campaign effectiveness.")

    # --- Row 1: KPI Cards ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", f"{len(df_filtered):,}")
    with col2:
        st.metric("Avg Income", f"${df_filtered['Income'].mean():,.0f}")
    with col3:
        st.metric("Avg Total Spend", f"${df_filtered['Total_Spend'].mean():,.0f}")
    with col4:
        avg_cmp = df_filtered['Total_Accepted_Campaigns'].mean()
        st.metric("Avg Campaigns Accepted", f"{avg_cmp:.2f}")

    st.markdown("---")

    # --- Tabs for different analysis sections ---
    tab1, tab2, tab3 = st.tabs(["📢 Campaign Performance", "💰 Spending Analysis", "👥 Customer Segmentation"])

    # -----------------------------------------------------------------------------
    # Tab 1: Campaign Performance
    # -----------------------------------------------------------------------------
    with tab1:
        st.subheader("Which customer segments accept campaigns?")
        
        # 1. Overall Campaign Acceptance Rate
        campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3', 'AcceptedCmp4', 'AcceptedCmp5', 'Response']
        acceptance_rates = df_filtered[campaign_cols].mean() * 100
        acceptance_df = acceptance_rates.reset_index()
        acceptance_df.columns = ['Campaign', 'Acceptance Rate (%)']
        
        fig_cmp = px.bar(acceptance_df, x='Campaign', y='Acceptance Rate (%)', 
                         title='Acceptance Rate by Campaign', 
                         text_auto='.2f', color='Acceptance Rate (%)', color_continuous_scale='Viridis')
        st.plotly_chart(fig_cmp, use_container_width=True)

        # 2. Response Rate by Demographics
        col_demo1, col_demo2 = st.columns(2)
        
        with col_demo1:
            # Response by Education
            edu_resp = df_filtered.groupby('Education')['Response'].mean().reset_index()
            fig_edu = px.bar(edu_resp, x='Education', y='Response', 
                             title='Response Rate by Education Level', labels={'Response': 'Response Rate'})
            st.plotly_chart(fig_edu, use_container_width=True)
            
        with col_demo2:
            # Response by Marital Status
            mar_resp = df_filtered.groupby('Marital_Status')['Response'].mean().reset_index()
            fig_mar = px.bar(mar_resp, x='Marital_Status', y='Response', 
                             title='Response Rate by Marital Status', labels={'Response': 'Response Rate'})
            st.plotly_chart(fig_mar, use_container_width=True)

    # -----------------------------------------------------------------------------
    # Tab 2: Spending Analysis
    # -----------------------------------------------------------------------------
    with tab2:
        st.subheader("Spending Patterns & Product Preferences")

        # 1. Spend Breakdown by Product
        product_cols = ['MntWines', 'MntFruits', 'MntMeatProducts', 'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
        avg_spend_product = df_filtered[product_cols].mean().reset_index()
        avg_spend_product.columns = ['Product', 'Average Spend']
        
        fig_prod = px.pie(avg_spend_product, values='Average Spend', names='Product', 
                          title='Average Spending Breakdown by Product Category', hole=0.4)
        st.plotly_chart(fig_prod, use_container_width=True)

        # 2. Income vs Total Spend
        fig_scatter = px.scatter(df_filtered, x='Income', y='Total_Spend', color='Education',
                                 title='Relationship: Income vs. Total Spend',
                                 trendline="ols", hover_data=['Age', 'Marital_Status'])
        st.plotly_chart(fig_scatter, use_container_width=True)

        # 3. Spending differences by Age Group (Binning Age)
        df_filtered['Age Group'] = pd.cut(df_filtered['Age'], bins=[0, 30, 45, 60, 100], labels=['<30', '30-45', '46-60', '60+'])
        
        fig_age_spend = px.box(df_filtered, x='Age Group', y='Total_Spend', color='Age Group',
                               title='Distribution of Total Spending by Age Group')
        st.plotly_chart(fig_age_spend, use_container_width=True)

    # -----------------------------------------------------------------------------
    # Tab 3: Customer Segmentation (Demographics)
    # -----------------------------------------------------------------------------
    with tab3:
        st.subheader("Customer Demographics Analysis")
        
        col_seg1, col_seg2 = st.columns(2)
        
        with col_seg1:
            # Age Distribution
            fig_age = px.histogram(df_filtered, x='Age', nbins=20, title='Customer Age Distribution', color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_age, use_container_width=True)
            
        with col_seg2:
            # Income Distribution
            fig_inc = px.histogram(df_filtered, x='Income', nbins=20, title='Customer Income Distribution', color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig_inc, use_container_width=True)

        # Country Heatmap (if Country column exists)
        if 'Country' in df_filtered.columns:
            country_counts = df_filtered['Country'].value_counts().reset_index()
            country_counts.columns = ['Country', 'Count']
            fig_map = px.choropleth(country_counts, locations="Country", locationmode='country names',
                                    color="Count", title="Customer Distribution by Country",
                                    color_continuous_scale="Plasma")
            st.plotly_chart(fig_map, use_container_width=True)

else:
    st.info("Awaiting data load. Please ensure the CSV file is present.")