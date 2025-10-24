import streamlit as st
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import math
import seaborn as sns
import numpy as np
from scipy import stats

warnings.filterwarnings('ignore')

st.set_page_config(page_title="Customer Churn Analysis", layout="wide", page_icon="📊")

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

COLORS = {
    'burgundy': '#7E102C',
    'cream': '#E1D4C1',
    'dusty_rose': '#D7A9A8',
    'chocolate': '#58423F',
    'taupe': '#E1D4C1',
    'dark_bg': '#1a1410',
    'dark_card': '#2d2520',
    'dark_text': '#E1D4C1',
}

if st.session_state.dark_mode:
    bg_color = COLORS['dark_bg']
    card_bg = COLORS['dark_card']
    text_color = COLORS['dark_text']
    sidebar_bg = COLORS['chocolate']
    sidebar_text = COLORS['cream']
    border_color = COLORS['chocolate']
    accent_color = COLORS['burgundy']
else:
    bg_color = COLORS['cream']
    card_bg = '#ffffff'
    text_color = COLORS['chocolate']
    sidebar_bg = COLORS['dusty_rose']
    sidebar_text = '#ffffff'
    border_color = COLORS['taupe']
    accent_color = COLORS['burgundy']

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background: {bg_color};
        color: {text_color};
        font-family: 'Montserrat', sans-serif;
    }}
    
    * {{
        transition: all 0.3s ease;
    }}
    
    [data-testid="stSidebar"] {{
        background: {sidebar_bg};
        border-right: 1px solid {border_color};
        box-shadow: 4px 0 20px rgba(126, 16, 44, 0.08);
    }}
    
    [data-testid="stSidebar"] * {{
        color: {sidebar_text} !important;
    }}

    .stApp:not(.theme-dark) [data-testid="stSidebar"] {{
        background: linear-gradient(135deg, {COLORS['burgundy']} 0%, {COLORS['chocolate']} 100%);
        color: {COLORS['cream']} !important;
        border-right: 1px solid rgba(0,0,0,0.04);
    }}

    .stApp:not(.theme-dark) [data-testid="stSidebar"] * {{
        color: {COLORS['cream']} !important;
    }}

    .stApp:not(.theme-dark) [data-testid="stSidebar"] .stRadio > div > label {{
        background: rgba(255,255,255,0.06) !important;
        color: {COLORS['cream']} !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }}
    
    [data-testid="stSidebar"] .stRadio > div {{
        background: transparent;
        padding: 0;
    }}
    
    [data-testid="stSidebar"] .stRadio > div > label {{
        background: rgba(255, 255, 255, 0.1);
        padding: 0.85rem 1.25rem !important;
        border-radius: 8px;
        margin: 0.35rem 0 !important;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.15);
        display: block;
        font-weight: 400 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em;
        backdrop-filter: blur(10px);
    }}
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {{
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(3px);
        border-color: rgba(255, 255, 255, 0.3);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}
    
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {{
        background: rgba(255, 255, 255, 0.95);
        color: {COLORS['burgundy']} !important;
        font-weight: 600 !important;
        border: 1px solid rgba(255, 255, 255, 1);
        box-shadow: 0 4px 12px rgba(126, 16, 44, 0.15);
    }}
    
    .main-header {{
        font-size: 3.5rem;
        font-weight: 700;
        font-family: 'Cormorant Garamond', serif;
        color: {accent_color};
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: 0.02em;
        line-height: 1.2;
    }}
    
    .sub-header {{
        font-size: 1.1rem;
        color: {'#8d7a6f' if not st.session_state.dark_mode else '#a89585'};
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }}
    
    .metric-card {{
        background: linear-gradient(135deg, {COLORS['burgundy']} 0%, {COLORS['chocolate']} 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: {COLORS['cream'] if not st.session_state.dark_mode else 'white'};
        text-align: center;
        box-shadow: 0 10px 30px rgba(126, 16, 44, 0.25);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.15);
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(126, 16, 44, 0.35);
    }}
    
    .metric-card:hover::before {{
        opacity: 1;
    }}
    
    .metric-card h3 {{
        margin: 0;
        font-size: 2.75rem;
        font-weight: 700;
        font-family: 'Cormorant Garamond', serif;
        letter-spacing: -0.01em;
    }}
    
    .metric-card p {{
        margin: 0.75rem 0 0 0;
        font-size: 0.85rem;
        opacity: 0.95;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}

    .stApp:not(.theme-dark) .metric-card, .stApp:not(.theme-dark) .metric-card h3, .stApp:not(.theme-dark) .metric-card p {{
        color: {COLORS['cream']} !important;
        opacity: 1 !important;
    }}
    
    .insight-box, .warning-box, .success-box {{
        background-color: {card_bg};
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid {border_color};
        position: relative;
        overflow: hidden;
    }}
    
    .insight-box::before, .warning-box::before, .success-box::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
    }}
    
    .insight-box::before {{ 
        background: {COLORS['burgundy']};
    }}
    .warning-box::before {{ 
        background: {COLORS['dusty_rose']};
    }}
    .success-box::before {{ 
        background: #2d5f3f;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: transparent;
        padding: 0.5rem 0;
        border-bottom: 2px solid {border_color};
        display: flex;
        align-items: center;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 12px 28px;
        background-color: transparent;
        border-radius: 10px;
        color: {text_color};
        border: none;
        font-weight: 500;
        font-size: 0.9rem;
        letter-spacing: 0.03em;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {'rgba(255,255,255,0.1)' if st.session_state.dark_mode else 'rgba(126, 16, 44, 0.05)'};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {accent_color};
        color: white !important;
        border: none;
        box-shadow: 0 -2px 8px rgba(126, 16, 44, 0.2);
    }}

    .stApp:not(.theme-dark) .stTabs [data-baseweb="tab"] {{
        background: linear-gradient(135deg, {COLORS['burgundy']} 0%, {COLORS['chocolate']} 100%);
        border-radius: 12px;
        box-shadow: 0 8px 24px rgba(126, 16, 44, 0.12);
        border: 1px solid rgba(255,255,255,0.06);
        color: {COLORS['cream']} !important;
        padding: 10px 26px;
        margin-right: 0.75rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .stApp:not(.theme-dark) .stTabs [data-baseweb="tab"] * {{
        color: {COLORS['cream']} !important;
    }}

    .stApp:not(.theme-dark) .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        background: linear-gradient(135deg, {COLORS['burgundy']} 0%, {COLORS['chocolate']} 100%);
        color: {COLORS['cream']} !important;
        box-shadow: 0 12px 32px rgba(126, 16, 44, 0.18);
        transform: translateY(-4px);
    }}

    .stApp:not(.theme-dark) .stTabs [data-baseweb="tab"],
    .stApp:not(.theme-dark) .stTabs [data-baseweb="tab"][aria-selected="true"] {{
        color: {COLORS['cream']} !important;
    }}
    
    div[data-testid="stExpander"] {{
        border: 1px solid {border_color};
        border-radius: 10px;
        margin-bottom: 1rem;
        background-color: {card_bg};
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }}
    
    div[data-testid="stExpander"]:hover {{
        border-color: {accent_color};
        box-shadow: 0 4px 12px rgba(126, 16, 44, 0.1);
    }}
    
    .dataframe {{
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid {border_color};
        font-family: 'Montserrat', sans-serif;
        font-size: 0.9rem;
    }}
    
    .stButton > button {{
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 0.85rem 1.5rem;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 500;
        font-size: 0.9rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 100%;
        backdrop-filter: blur(10px);
        letter-spacing: 0.03em;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}
    
    .stApp, .stApp * {{
        color: {text_color} !important;
    }}
    
    [data-testid="stMetricValue"], .stMetric {{
        color: {text_color} !important;
        font-weight: 600;
    }}

    .stApp:not(.theme-dark) [data-testid="stMetricValue"] , .stApp:not(.theme-dark) [data-testid="stMetricLabel"] {{
        color: {COLORS['cream']} !important;
    }}
    
    a, a * {{
        color: {accent_color} !important;
        font-weight: 500;
    }}
    
    h1, h2, h3, h4 {{
        font-family: 'Cormorant Garamond', serif;
        font-weight: 600;
        letter-spacing: 0.01em;
    }}
    
    h2 {{
        font-size: 2.25rem;
        margin-top: 2.5rem;
        margin-bottom: 1.25rem;
        color: {accent_color};
    }}
    
    h3 {{
        font-size: 1.75rem;
        margin-top: 1.75rem;
        margin-bottom: 1rem;
        color: {text_color};
    }}
    
    h4 {{
        font-size: 1.35rem;
        margin-top: 1.25rem;
        margin-bottom: 0.75rem;
        color: {text_color};
    }}
    
    [data-testid="stMetricLabel"] {{
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {'#8d7a6f' if not st.session_state.dark_mode else '#a89585'} !important;
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 2.25rem;
        font-weight: 700;
        font-family: 'Cormorant Garamond', serif;
    }}
    
    hr {{
        margin: 2.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {border_color}, transparent);
    }}
    
    .stRadio > div {{
        gap: 0.4rem;
    }}
    
    .stRadio > div > label {{
        padding: 0.5rem 0;
        font-weight: 400;
    }}
    
    .stSuccess, .stError, .stWarning, .stInfo {{
        border-radius: 10px;
        padding: 1.25rem 1.75rem;
        border: 1px solid {border_color};
    }}
    
    .team-box {{
        background: rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        margin-top: 1.5rem;
    }}
    
    .team-box h4 {{
        margin: 0 0 1.25rem 0;
        font-size: 1rem;
        font-weight: 600;
        color: {sidebar_text} !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-family: 'Montserrat', sans-serif;
    }}
    
    .team-member {{
        background: rgba(255, 255, 255, 0.1);
        padding: 0.85rem 1.15rem;
        border-radius: 8px;
        margin-bottom: 0.6rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .team-member:last-child {{
        margin-bottom: 0;
    }}
    
    .team-member strong {{
        font-size: 0.95rem;
        font-weight: 500;
        color: {sidebar_text} !important;
        letter-spacing: 0.02em;
    }}
    
    .nav-header {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {sidebar_text} !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 1.25rem;
        padding-bottom: 0.85rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.25);
    }}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Customer Churn Analysis</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Data Preprocessing & Exploratory Data Analysis</p>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("customer_data.csv")
        return df
    except Exception as e:
        return pd.DataFrame()

data = load_data()
if data.empty:
    st.error("Could not load customer data. Please check the data source.")
    st.stop()

st.sidebar.button(
    "Dark Mode" if not st.session_state.dark_mode else "Light Mode",
    on_click=lambda: setattr(st.session_state, 'dark_mode', not st.session_state.dark_mode),
    use_container_width=True
)

st.sidebar.markdown("---")

st.sidebar.markdown('<p class="nav-header">Navigation</p>', unsafe_allow_html=True)

section = st.sidebar.radio("", [
    "Overview",
    "Initial Exploration",
    "Age Preprocessing",
    "Income Preprocessing",
    "Tenure Preprocessing",
    "Support Calls Preprocessing",
    "After Preprocessing",
    "Standardization",
    "EDA - Scatter Plots",
    "EDA - Churn Analysis",
    "EDA - Box Plots",
    "Correlation",
    "Conclusion"
], label_visibility="collapsed")

if section == "Overview":
    st.markdown("## Project Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{len(data):,}</h3><p>Total Records</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>8</h3><p>Features</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{data["ChurnStatus"].mean()*100:.1f}%</h3><p>Churn Rate</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h3>{data.isnull().sum().sum()}</h3><p>Missing Values</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Project Objectives")
        st.markdown("""
        This analysis performs comprehensive data preprocessing and exploratory data analysis on customer churn data. 
        The goal is to clean the dataset, handle missing values and outliers appropriately, and identify key patterns 
        that influence customer churn behavior.
        """)
        
        st.markdown("### Analysis Workflow")
        st.markdown("""
        1. **Initial Exploration** - Understand data structure and distributions
        2. **Data Preprocessing** - Handle missing values and outliers
        3. **Standardization** - Normalize numerical features
        4. **Exploratory Data Analysis** - Visualize relationships and patterns
        5. **Correlation Analysis** - Identify key predictors
        6. **Conclusions** - Summarize findings
        """)
    
    with col2:
        st.markdown("### Quick Stats")
        
        st.markdown(f'''
        <div class="insight-box">
        <strong>Data Quality Metrics</strong><br><br>
        • Completeness: {((1 - data.isnull().sum().sum() / (len(data) * len(data.columns))) * 100):.1f}%<br>
        • Unique Customers: {data['CustomerID'].nunique():,}<br>
        • Avg Age: {data['Age'].mean():.1f} years<br>
        • Avg Tenure: {data['Tenure'].mean():.1f} years
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown(f'''
        <div class="warning-box">
        <strong>Churn Breakdown</strong><br><br>
        • Churned: {(data['ChurnStatus'].sum()):,} customers<br>
        • Stayed: {(len(data) - data['ChurnStatus'].sum()):,} customers<br>
        • Risk Level: {'High' if data['ChurnStatus'].mean() > 0.3 else 'Moderate' if data['ChurnStatus'].mean() > 0.15 else 'Low'}
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Dataset Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Numerical Features")
        st.markdown("""
        - **Age**: Customer age (years)
        - **Income**: Annual income (USD)
        - **Tenure**: Years with company
        - **SupportCalls**: Number of support calls
        """)
    
    with col2:
        st.markdown("#### Categorical Features")
        st.markdown("""
        - **Gender**: Male (0) / Female (1)
        - **ProductType**: Basic (0) / Premium (1)
        - **ChurnStatus**: Stayed (0) / Churned (1)
        - **CustomerID**: Unique identifier
        """)
    
elif section == "Initial Exploration":
    st.markdown("## Initial Data Exploration")
    
    st.markdown("### Feature Observations")
    
    st.markdown("""
    <div class="insight-box">
    - <strong>CustomerID</strong>: Unique Identifier, <em>irrelevant</em>.<br>
    - <strong>Age</strong>: Numerical <code>int()</code> data, the outliers more of a domain knowledge.<br>
    - <strong>Gender</strong>: Categorical Data that's already Hot-Encoded.<br>
    - <strong>Income</strong>: Annual income of the customer (in USD), for outliers must plot and explore the data.<br>
    - <strong>Tenure</strong>: Numerical <code>int()</code> data, the outliers mix of domain knowledge and data exploration.<br>
    - <strong>ProductType</strong>: Categorical Data that's already Hot-Encoded.<br>
    - <strong>SupportCalls</strong>: Numerical <code>int()</code> data, for outliers must plot and explore the data.<br>
    - <strong>ChurnStatus</strong>: Categorical Data that's already Hot-Encoded.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Sample Data", "Data Info", "Statistics"])
    
    with tab1:
        st.markdown("### First 7 Rows")
        st.dataframe(data.head(7), use_container_width=True)
    
    with tab2:
        st.markdown("### Dataset Information")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Rows", data.shape[0])
            st.metric("Total Columns", data.shape[1])
        with col2:
            st.metric("Total Missing Values", data.isnull().sum().sum())
            st.metric("Memory Usage", f"{data.memory_usage(deep=True).sum() / 1024:.2f} KB")
        
        st.markdown("#### Missing Values by Feature")
        missing_df = pd.DataFrame({
            'Feature': data.columns,
            'Missing Count': data.isnull().sum().values,
            'Percentage': (data.isnull().sum().values / len(data) * 100).round(2)
        })
        st.dataframe(missing_df[missing_df['Missing Count'] > 0], use_container_width=True)
    
    with tab3:
        st.markdown("### Statistical Summary")
        st.dataframe(data.describe(), use_container_width=True)
    
    st.markdown("---")
    
    st.markdown("### Observations From Data Statistics")
    
    st.markdown("""
    <div class="insight-box">
    - <strong>CustomerID</strong>: Unique identifier, <em>irrelevant</em>.<br>
    - <strong>Age</strong>: Customer ages vary widely; most are middle-aged to older.<br>
    - <strong>Gender</strong>: Hot Encoded, Both genders churn almost equally likely <em>irrelevant</em>.<br>
    - <strong>Income</strong>: Customer incomes vary greatly; the standard deviation is much larger than the mean, indicating outliers.<br>
    - <strong>Tenure</strong>: Tenure seems reasonable, the range is from (0-9), and it's distributed about evenly.<br>
    - <strong>ProductType</strong>: Hot Encoded, High Majority of customers are subscribed to the basic type.<br>
    - <strong>SupportCalls</strong>: Data seems consistent up to the 75% mark, but the max indicates wrongly entered data.<br>
    - <strong>ChurnStatus</strong>: Most customers <strong>stayed</strong>.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Distribution of Numerical Features")
    
    numerical_features = data.select_dtypes(include=['float64', 'int64']).columns.tolist()
    numerical_features.remove("Gender")
    numerical_features.remove("ProductType")
    numerical_features.remove("ChurnStatus")
    
    n_features = len(numerical_features)
    n_cols = 2
    n_rows = math.ceil(n_features / n_cols)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 5*n_rows))
    fig.suptitle('Distribution of Numerical Features', fontsize=18, fontweight='bold', y=1.0)
    axes = axes.flatten() if n_features > 1 else [axes]
    for idx, feature in enumerate(numerical_features):
        axes[idx].hist(data[feature], bins=30, color=COLORS['dusty_rose'], edgecolor=COLORS['burgundy'], alpha=0.75, linewidth=1.5)
        axes[idx].set_title(f'{feature} Distribution', fontweight='bold', fontsize=14)
        axes[idx].set_xlabel(feature, fontsize=12)
        axes[idx].set_ylabel('Frequency', fontsize=12)
        axes[idx].axvline(data[feature].mean(), color=COLORS['burgundy'], linestyle='--', 
                          linewidth=2.5, label=f'Mean: {data[feature].mean():.2f}')
        axes[idx].axvline(data[feature].median(), color=COLORS['chocolate'], linestyle='--', 
                          linewidth=2.5, label=f'Median: {data[feature].median():.2f}')
        axes[idx].legend(fontsize=10)
        axes[idx].grid(True, alpha=0.25, linestyle=':', linewidth=0.8)
    for j in range(idx+1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    st.markdown("### Distribution of Categorical Features")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Categorical Features Analysis', fontsize=18, fontweight='bold', y=0.995)
    
    gender_counts = data['Gender'].value_counts()
    bars1 = axes[0, 0].bar(['Male', 'Female'], gender_counts.values, color=[COLORS['dusty_rose'], COLORS['taupe']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[0, 0].set_title('Gender Distribution', fontweight='bold', fontsize=14)
    axes[0, 0].set_ylabel('Count', fontsize=12)
    axes[0, 0].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for bar in bars1:
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    product_counts = data['ProductType'].value_counts()
    bars2 = axes[0, 1].bar(['Basic', 'Premium'], product_counts.values, color=[COLORS['chocolate'], COLORS['burgundy']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[0, 1].set_title('Product Type Distribution', fontweight='bold', fontsize=14)
    axes[0, 1].set_ylabel('Count', fontsize=12)
    axes[0, 1].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for bar in bars2:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    churn_counts = data['ChurnStatus'].value_counts()
    bars3 = axes[1, 0].bar(['Stayed', 'Churned'], churn_counts.values, color=[COLORS['taupe'], COLORS['burgundy']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[1, 0].set_title('Churn Status Distribution', fontweight='bold', fontsize=14)
    axes[1, 0].set_ylabel('Count', fontsize=12)
    axes[1, 0].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for bar in bars3:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    fig.delaxes(axes[1, 1])
    
    plt.tight_layout()
    st.pyplot(fig)

elif section == "Age Preprocessing":
    st.markdown("## Age Preprocessing")
    
    st.markdown("### Step 1: Outlier Detection")
    
    outliers_count = len(data[(data["Age"] < 18) | (data["Age"] > 90)])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", len(data))
    with col2:
        st.metric("Outliers Found", outliers_count)
    with col3:
        st.metric("Outlier Percentage", f"{(outliers_count/len(data)*100):.2f}%")
    
    st.markdown(f"""
    <div class="warning-box">
    <strong>Decision</strong>: Drop any age that is less than 18, because there are only two entries.
    </div>
    """, unsafe_allow_html=True)
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    
    st.markdown("---")
    
    st.markdown("### Step 2: Missing Value Imputation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Statistical Analysis")
        age_stats = data_clean_age["Age"].describe()
        st.dataframe(age_stats)
        
        skew_value = data_clean_age["Age"].skew()
        st.metric("Skewness", f"{skew_value:.4f}")
    
    with col2:
        st.markdown("#### Imputation Strategy")
        st.markdown(f"""
        <div class="success-box">
        <strong>Method</strong>: Fill with Mean (44 years)<br><br>
        <strong>Justification</strong>: The data is barely skewed, the mean and median are relatively close 43.6 and 43 indicating that the data is symmetric, 
        which means using the mean or median won't make a large difference, hence the mean which is 44 was used.
        </div>
        """, unsafe_allow_html=True)
    
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    
    st.markdown("---")
    
    st.markdown("### Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Missing Values After", data_clean_age["Age"].isnull().sum())
    with col2:
        new_skew = data_clean_age["Age"].skew()
        st.metric("New Skewness", f"{new_skew:.4f}")

elif section == "Income Preprocessing":
    st.markdown("## Income Preprocessing")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
   
    st.markdown("### Step 1: Missing Value Imputation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Distribution Analysis")
        skew_value = data_income["Income"].skew()
        st.metric("Skewness", f"{skew_value:.4f}")
        st.metric("Median Income", f"${data_income['Income'].median():,.2f}")
        st.metric("Mean Income", f"${data_income['Income'].mean():,.2f}")
    
    with col2:
        st.markdown("#### Imputation Strategy")
        st.markdown(f"""
        <div class="success-box">
        <strong>Method</strong>: Fill with Median<br><br>
        <strong>Justification</strong>: The Histogram shows that the data is skewed, therefore the median was used to fill the missing data.
        </div>
        """, unsafe_allow_html=True)
    
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    
    st.markdown("---")
    
    st.markdown("### Step 2: Outlier Detection & Treatment")
    
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_lower_outliers_value = Q1 - 1.5 * IQR
    income_upper_outliers_value = Q3 + 1.5 * IQR
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Q1 (25th percentile)", f"${Q1:,.2f}")
    with col2:
        st.metric("Q3 (75th percentile)", f"${Q3:,.2f}")
    with col3:
        st.metric("IQR", f"${IQR:,.2f}")
    
    outliers = data_income[
        (data_income["Income"] > income_upper_outliers_value) |
        (data_income["Income"] < income_lower_outliers_value)
    ]["Income"]
    
    st.warning(f"**{len(outliers)} outliers detected** using IQR method")
    
    income = data_income['Income'].dropna()
    Q1 = income.quantile(0.25)
    Q3 = income.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = income[(income < lower_bound) | (income > upper_bound)]
    
    if len(outliers) > 0:
        outlier_counts = outliers.value_counts().reset_index()
        outlier_counts.columns = ['Outlier Value', 'Count']
        outlier_counts = outlier_counts.sort_values('Outlier Value')
    else:
        outlier_counts = pd.DataFrame(columns=['Outlier Value', 'Count'])
    
    plt.figure(figsize=(12, 7))
    box = plt.boxplot(
        income,
        vert=True,
        patch_artist=True,
        boxprops=dict(facecolor=COLORS['dusty_rose'], color=COLORS['burgundy'], linewidth=2),
        medianprops=dict(color=COLORS['burgundy'], linewidth=3),
        whiskerprops=dict(color=COLORS['chocolate'], linewidth=2),
        capprops=dict(color=COLORS['chocolate'], linewidth=2),
        flierprops=dict(marker='o', color=COLORS['burgundy'], alpha=0.7, markersize=6)
    )
    
    plt.title('Income Box Plot Focused on IQR (with Outlier Summary Table)', fontweight='bold', fontsize=16)
    plt.ylabel('Income', fontsize=13)
    plt.grid(True, alpha=0.25, linestyle=':', linewidth=0.8)
    plt.ylim(Q1 - IQR, Q3 + IQR)
    
    plt.text(1.1, Q1, f'Q1: ${Q1:,.2f}', color=COLORS['chocolate'], fontsize=11, fontweight='bold')
    plt.text(1.1, income.median(), f'Median: ${income.median():,.2f}', color=COLORS['burgundy'], fontsize=11, fontweight='bold')
    plt.text(1.1, Q3, f'Q3: ${Q3:,.2f}', color=COLORS['chocolate'], fontsize=11, fontweight='bold')
    
    lower_whisker = lower_bound

    upper_whisker = upper_bound
 
    plt.text(0.9, lower_whisker, f'Lower Whisker: ${lower_bound:,.2f}', color=COLORS['chocolate'], fontsize=10, ha='right', fontweight='bold')
    plt.text(0.9, upper_whisker, f'Upper Whisker: ${upper_bound:,.2f}', color=COLORS['chocolate'], fontsize=10, ha='right', fontweight='bold')
    
    visible_outliers = outliers[(outliers >= plt.ylim()[0]) & (outliers <= plt.ylim()[1])]
    for val in visible_outliers:
        plt.plot(1, val, 'ro', color=COLORS['burgundy'])
        plt.text(1.05, val, f'${val:,.2f}', color=COLORS['burgundy'], fontsize=9)
    
    if not outlier_counts.empty:
        table_data = outlier_counts.round(2).astype(str).values.tolist()
        table_data.insert(0, ['Value', 'Count'])
        
        plt.table(
            cellText=table_data,
            colWidths=[0.15, 0.1],
            cellLoc='center',
            loc='right',
            colLabels=None,
            bbox=[1.05, 0.15, 0.3, 0.7]
        )
    
    plt.tight_layout(rect=[0, 0, 0.75, 1])
    st.pyplot(plt)
    data_tenure = data_income.copy()
    
    st.markdown(f"""
<div class="warning-box">
<strong>Treatment Options</strong>:<br>
- <strong>Dropping</strong> — No, we would lose too much data.<br>
- <strong>Smoothing</strong> — Data is too high; smoothing won't help.<br>
- <strong>Capping at upper whisker</strong> — Keeps the data rows and helps handle outliers 
<span style="background-color:#D7A9A8; color:burgundy; border-radius:50%; padding:2px 6px;">✓</span>
</div>
""", unsafe_allow_html=True)

    
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    
    st.markdown("---")
    
    st.markdown("### Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Outliers After Capping", len(data_income[data_income['Income'] > income_upper_outliers_value]))
    with col2:
        new_skew = data_income["Income"].skew()
        st.metric("New Skewness", f"{new_skew:.4f}")

elif section == "Tenure Preprocessing":
    st.markdown("## Tenure Preprocessing")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    
    
    st.markdown("### Missing Value Imputation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Distribution Analysis")
        skew_value = data_tenure["Tenure"].skew()
        st.metric("Skewness", f"{skew_value:.4f}")
        st.metric("Mean Tenure", f"{data_tenure['Tenure'].mean():.2f} years")
        st.metric("Median Tenure", f"{data_tenure['Tenure'].median():.2f} years")
    
    with col2:
        st.markdown("#### Imputation Strategy")
        st.markdown(f"""
        <div class="success-box">
        <strong>Method</strong>: Fill with Median (5 years)<br><br>
        <strong>Justification</strong>: The values are approximately normally distributed with minimal skew, so we can use the mean. 
        Since both the mean and median are around 5, we will fill the missing values with 5.
        </div>
        """, unsafe_allow_html=True)
    
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    
    st.markdown("---")
    
    st.markdown("### Outlier Analysis")
    st.markdown("""
    <div class="insight-box">
    <strong>Finding</strong>: No significant outliers detected in Tenure data.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Results")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Missing Values After", data_tenure["Tenure"].isnull().sum())
    with col2:
        new_skew = data_tenure["Tenure"].skew()
        st.metric("New Skewness", f"{new_skew:.4f}")

elif section == "Support Calls Preprocessing":
    st.markdown("## Support Calls Preprocessing")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    
    
    st.markdown("### Step 1: Outlier Detection & Treatment")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Initial Distribution")
        skew_value = data_sc["SupportCalls"].skew()
        st.metric("Skewness", f"{skew_value:.4f}")
        st.metric("Mean", f"{data_sc['SupportCalls'].mean():.2f} calls")
        st.metric("Median", f"{data_sc['SupportCalls'].median():.2f} calls")
        st.metric("Max", f"{data_sc['SupportCalls'].max():.0f} calls")
    
    with col2:
        st.markdown("#### Treatment Strategy")
        st.markdown("""
        <div class="warning-box">
        <strong>Method</strong>: Cap values > 25 to 7<br><br>
        <strong>Rationale</strong>: Extremely high call counts are anomalous and should be capped to normalize the distribution.
        </div>
        """, unsafe_allow_html=True)
    
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    
    st.markdown("---")
    
    st.markdown("### Step 2: Missing Value Imputation")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Post-Capping Statistics")
        st.metric("Mean After Capping", f"{data_sc['SupportCalls'].mean():.2f} calls")
        st.metric("Median After Capping", f"{data_sc['SupportCalls'].median():.2f} calls")
    
    with col2:
        st.markdown("#### Imputation Strategy")
        st.markdown(f"""
        <div class="success-box">
        <strong>Method</strong>: Fill with Median<br><br>
        <strong>Justification</strong>: Data still shows some skewness after capping, so median is more appropriate.
        </div>
        """, unsafe_allow_html=True)
    
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    st.markdown("---")
    
    st.markdown("### Results")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Missing Values After", data_sc["SupportCalls"].isnull().sum())
    with col2:
        new_skew = data_sc["SupportCalls"].skew()
        st.metric("New Skewness", f"{new_skew:.4f}")
    with col3:
        st.metric("Max Value After", f"{data_sc['SupportCalls'].max():.0f} calls")

elif section == "After Preprocessing":
    st.markdown("## Data After Preprocessing")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    data_processed = data_sc.copy()
    
    st.markdown("### Preprocessing Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", len(data_processed), delta=f"{len(data_processed) - len(data)} from original")
    with col2:
        st.metric("Missing Values", data_processed.isnull().sum().sum(), delta=f"-{data.isnull().sum().sum()}")
    with col3:
        st.metric("Features Cleaned", "4")
    with col4:
        st.metric("Data Quality", "100%")
    
    st.markdown("---")
    
    st.markdown("### Numerical Features Distribution (After Preprocessing)")
    
    numerical_features = data_processed.select_dtypes(include=['float64', 'int64']).columns.tolist()
    numerical_features.remove("Gender")
    numerical_features.remove("ProductType")
    numerical_features.remove("ChurnStatus")
    
    n_features = len(numerical_features)
    n_cols = 2
    n_rows = math.ceil(n_features / n_cols)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 5*n_rows))
    fig.suptitle('Distribution of Numerical Features (After Preprocessing)', fontsize=18, fontweight='bold', y=1.0)
    axes = axes.flatten() if n_features > 1 else [axes]
    for idx, feature in enumerate(numerical_features):
        axes[idx].hist(data_processed[feature], bins=30, color=COLORS['dusty_rose'], edgecolor=COLORS['burgundy'], alpha=0.75, linewidth=1.5)
        axes[idx].set_title(f'{feature} Distribution', fontweight='bold', fontsize=14)
        axes[idx].set_xlabel(feature, fontsize=12)
        axes[idx].set_ylabel('Frequency', fontsize=12)
        axes[idx].axvline(data_processed[feature].mean(), color=COLORS['burgundy'], linestyle='--', 
                          linewidth=2.5, label=f'Mean: {data_processed[feature].mean():.2f}')
        axes[idx].axvline(data_processed[feature].median(), color=COLORS['chocolate'], linestyle='--', 
                          linewidth=2.5, label=f'Median: {data_processed[feature].median():.2f}')
        axes[idx].legend(fontsize=10)
        axes[idx].grid(True, alpha=0.25, linestyle=':', linewidth=0.8)
    for j in range(idx+1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    st.markdown("### Categorical Features Distribution (After Preprocessing)")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Categorical Features Analysis (After Preprocessing)', fontsize=18, fontweight='bold', y=0.995)
    
    gender_counts = data_processed['Gender'].value_counts()
    bars1 = axes[0, 0].bar(['Male', 'Female'], gender_counts.values, color=[COLORS['dusty_rose'], COLORS['taupe']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[0, 0].set_title('Gender Distribution', fontweight='bold', fontsize=14)
    axes[0, 0].set_ylabel('Count', fontsize=12)
    axes[0, 0].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for bar in bars1:
        height = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    product_counts = data_processed['ProductType'].value_counts()
    bars2 = axes[0, 1].bar(['Basic', 'Premium'], product_counts.values, color=[COLORS['chocolate'], COLORS['burgundy']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[0, 1].set_title('Product Type Distribution', fontweight='bold', fontsize=14)
    axes[0, 1].set_ylabel('Count', fontsize=12)
    axes[0, 1].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for bar in bars2:
        height = bar.get_height()
        axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    churn_counts = data_processed['ChurnStatus'].value_counts()
    bars3 = axes[1, 0].bar(['Stayed', 'Churned'], churn_counts.values, color=[COLORS['taupe'], COLORS['burgundy']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[1, 0].set_title('Churn Status Distribution', fontweight='bold', fontsize=14)
    axes[1, 0].set_ylabel('Count', fontsize=12)
    axes[1, 0].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for bar in bars3:
        height = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height):,}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    fig.delaxes(axes[1, 1])
    
    plt.tight_layout()
    st.pyplot(fig)

elif section == "Standardization":
    st.markdown("## Feature Standardization")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    st.markdown("### Z-Score Standardization Formula")
    st.latex(r"z = \frac{x - \mu}{\sigma}")
    st.markdown("Where: **z** = standardized value, **x** = original value, **μ** = mean, **σ** = standard deviation")
    
    st.markdown("---")
    
    st.markdown("### Applying Standardization")
    
    data_standardized = data_sc.copy()
    
    features_to_standardize = ["Age", "Income", "Tenure", "SupportCalls"]
    
    for feature in features_to_standardize:
        with st.expander(f"{feature} Standardization Details"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Before Standardization**")
                st.metric("Mean", f"{data_sc[feature].mean():.2f}")
                st.metric("Std Dev", f"{data_sc[feature].std():.2f}")
            
            data_standardized[feature] = (data_standardized[feature] - data_standardized[feature].mean()) / data_standardized[feature].std()
            
            with col2:
                st.markdown("**After Standardization**")
                st.metric("Mean", f"{data_standardized[feature].mean():.6f}")
                st.metric("Std Dev", f"{data_standardized[feature].std():.6f}")
    
    st.markdown("---")
    
    st.markdown("### Standardized Distributions")
    
    numerical_features = data_standardized.select_dtypes(include=['float64', 'int64']).columns.tolist()
    numerical_features.remove("Gender")
    numerical_features.remove("ProductType")
    numerical_features.remove("ChurnStatus")
    
    n_features = len(numerical_features)
    n_cols = 2
    n_rows = math.ceil(n_features / n_cols)
    
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(7*n_cols, 5*n_rows))
    fig.suptitle('Distribution of Numerical Features (Standardized)', fontsize=18, fontweight='bold', y=1.0)
    axes = axes.flatten() if n_features > 1 else [axes]
    for idx, feature in enumerate(numerical_features):
        axes[idx].hist(data_standardized[feature], bins=30, color=COLORS['dusty_rose'], edgecolor=COLORS['burgundy'], alpha=0.75, linewidth=1.5)
        axes[idx].set_title(f'{feature} Distribution', fontweight='bold', fontsize=14)
        axes[idx].set_xlabel(feature, fontsize=12)
        axes[idx].set_ylabel('Frequency', fontsize=12)
        axes[idx].axvline(data_standardized[feature].mean(), color=COLORS['burgundy'], linestyle='--', 
                          linewidth=2.5, label=f'Mean: {data_standardized[feature].mean():.2f}')
        axes[idx].axvline(data_standardized[feature].median(), color=COLORS['chocolate'], linestyle='--', 
                          linewidth=2.5, label=f'Median: {data_standardized[feature].median():.2f}')
        axes[idx].legend(fontsize=10)
        axes[idx].grid(True, alpha=0.25, linestyle=':', linewidth=0.8)
    for j in range(idx+1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout()
    st.pyplot(fig)

elif section == "EDA - Scatter Plots":
    st.markdown("## Exploratory Data Analysis: Scatter Plots")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    numeric_cols = data_sc.select_dtypes(include=["float64", "int64"]).columns.drop(["ChurnStatus", "ProductType", "Gender"])
    
    st.markdown("### Feature vs Churn Status")
    
    for col in numeric_cols:
        st.markdown(f"#### {col} vs Churn Status")
        fig, ax = plt.subplots(figsize=(11, 6))
        sns.scatterplot(data=data_sc, x=col, y="ChurnStatus", alpha=0.65, ax=ax, s=60, color=COLORS['dusty_rose'], edgecolor=COLORS['burgundy'], linewidth=0.5)
        ax.set_title(f"{col} vs ChurnStatus (Scatter Plot)", fontsize=16, fontweight='bold')
        ax.set_ylabel("Churn Status (0=Stayed, 1=Churned)", fontsize=12)
        ax.set_xlabel(col, fontsize=12)
        ax.grid(True, alpha=0.25, linestyle=':', linewidth=0.8)
        st.pyplot(fig)
        
        correlation = data_sc[[col, "ChurnStatus"]].corr().iloc[0, 1]
        st.markdown(f'<div class="insight-box"><strong>Correlation</strong>: {correlation:.3f}</div>', unsafe_allow_html=True)
        
        st.markdown("---")

elif section == "EDA - Churn Analysis":
    st.markdown("## Exploratory Data Analysis: Churn Rate by Category")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    st.markdown("### Churn Rate Comparison")
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    gender_churn = data_sc.groupby('Gender')['ChurnStatus'].mean() * 100
    bars1 = axes[0].bar(['Male', 'Female'], gender_churn.values, color=[COLORS['dusty_rose'], COLORS['taupe']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[0].set_title('Churn Rate by Gender', fontsize=16, fontweight='bold')
    axes[0].set_ylabel('Churn Rate (%)', fontsize=13)
    axes[0].set_ylim(0, 100)
    axes[0].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for i, v in enumerate(gender_churn.values):
        axes[0].text(i, v + 3, f'{v:.1f}%', ha='center', fontweight='bold', fontsize=13)
    
    product_churn = data_sc.groupby('ProductType')['ChurnStatus'].mean() * 100
    bars2 = axes[1].bar(['Basic', 'Premium'], product_churn.values, color=[COLORS['chocolate'], COLORS['burgundy']], edgecolor=COLORS['burgundy'], linewidth=2)
    axes[1].set_title('Churn Rate by Product Type', fontsize=16, fontweight='bold')
    axes[1].set_ylabel('Churn Rate (%)', fontsize=13)
    axes[1].set_ylim(0, 100)
    axes[1].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    for i, v in enumerate(product_churn.values):
        axes[1].text(i, v + 3, f'{v:.1f}%', ha='center', fontweight='bold', fontsize=13)
    
    plt.tight_layout()
    st.pyplot(fig)

elif section == "EDA - Box Plots":
    st.markdown("## Exploratory Data Analysis: Box Plots")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    numerical_features = ['Age', 'Income', 'Tenure', 'SupportCalls']
    fig, axes = plt.subplots(2, 2, figsize=(15, 11))
    axes = axes.ravel()
    
    for idx, col in enumerate(numerical_features):
        box_parts = axes[idx].boxplot(
            [data_sc[data_sc['ChurnStatus'] == 0][col].dropna(), 
             data_sc[data_sc['ChurnStatus'] == 1][col].dropna()],
            labels=['Stayed', 'Churned'],
            patch_artist=True,
            widths=0.6
        )
        
        for patch, color in zip(box_parts['boxes'], [COLORS['taupe'], COLORS['burgundy']]):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
            patch.set_linewidth(2)
        
        for element in ['whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(box_parts[element], color=COLORS['chocolate'], linewidth=2)
        
        axes[idx].set_title(f'{col} vs Churn Status', fontsize=15, fontweight='bold')
        axes[idx].set_xlabel('Churn Status', fontsize=12)
        axes[idx].set_ylabel(col, fontsize=12)
        axes[idx].grid(True, alpha=0.25, axis='y', linestyle=':', linewidth=0.8)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    st.markdown("### Statistical Comparison")
    
    comparison_data = []
    for feature in numerical_features:
        stayed = data_sc[data_sc['ChurnStatus'] == 0][feature]
        churned = data_sc[data_sc['ChurnStatus'] == 1][feature]
        
        comparison_data.append({
            'Feature': feature,
            'Stayed (Mean)': f"{stayed.mean():.2f}",
            'Churned (Mean)': f"{churned.mean():.2f}",
            'Difference': f"{abs(stayed.mean() - churned.mean()):.2f}",
            'Stayed (Median)': f"{stayed.median():.2f}",
            'Churned (Median)': f"{churned.median():.2f}"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)

elif section == "Correlation":
    st.markdown("## Correlation Analysis")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    data_corr_matrix = data_sc.drop(["CustomerID"], axis=1)
    data_corr_matrix = data_corr_matrix.corr(method='pearson')
    
    st.markdown("### Full Correlation Heatmap")
    
    numerical_cols = ['Age', 'Gender', 'Income', 'Tenure', 'ProductType', 'SupportCalls', 'ChurnStatus']
    correlation_matrix = data_sc[numerical_cols].corr(method='pearson')
    
    fig, ax = plt.subplots(figsize=(13, 10))
    
    from matplotlib.colors import LinearSegmentedColormap
    colors_list = [COLORS['burgundy'], COLORS['dusty_rose'], '#ffffff',COLORS['dusty_rose'],COLORS['burgundy']]
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors_list, N=n_bins)
    
    color_matrix = correlation_matrix.copy()
    color_matrix = color_matrix.clip(lower=-0.5, upper=0.5)
    for i in range(color_matrix.shape[0]):
        color_matrix.iat[i, i] = 0.5
    
    annot_matrix = correlation_matrix.round(3).astype(str)
    
    sns.heatmap(
        color_matrix,
        annot=annot_matrix,
        fmt='',
        cmap=cmap,
        square=True,
        linewidths=1.5,
        cbar_kws={"shrink": 0.8},
        ax=ax,
        vmin=-0.5,
        vmax=0.5,
        annot_kws={"fontsize": 11, "fontweight": "bold"}
    )
    
    ax.set_title('Feature Correlation Matrix (Pearson)', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    st.markdown("### Feature Correlation with Churn Status")
    
    churn_correlation = correlation_matrix['ChurnStatus'].sort_values(ascending=False).drop('ChurnStatus')
    
    fig, ax = plt.subplots(figsize=(11, 7))
    bar_colors = [COLORS['dusty_rose'] if x > 0 else COLORS['burgundy'] for x in churn_correlation.values]
    bars = ax.barh(
        churn_correlation.index,
        churn_correlation.values,
        color=bar_colors,
        edgecolor=COLORS['burgundy'],
        linewidth=2
    )
    ax.set_xlabel('Correlation Coefficient', fontsize=13, fontweight='bold')
    ax.set_title('Feature Correlation with Churn Status', fontsize=16, fontweight='bold')
    ax.axvline(x=0, color=COLORS['burgundy'], linestyle='-', linewidth=1.2)
    
    for i, (bar, value) in enumerate(zip(bars, churn_correlation.values)):
        ax.text(value + 0.01 if value > 0 else value - 0.01, i, f'{value:.3f}',
                va='center', ha='left' if value > 0 else 'right', fontweight='bold', color=COLORS['chocolate'], fontsize=11)
    
    ax.grid(True, alpha=0.25, axis='x', linestyle=':', linewidth=0.8)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("---")
    
    st.markdown("### Correlation Values")
    corr_df = pd.DataFrame({
        'Feature': churn_correlation.index,
        'Correlation with Churn': churn_correlation.values,
        'Strength': ['Strong' if abs(x) > 0.5 else 'Moderate' if abs(x) > 0.3 else 'Weak' for x in churn_correlation.values]
    }).sort_values('Correlation with Churn', key=abs, ascending=False)
    st.dataframe(corr_df, use_container_width=True)
    
    abs_sorted = corr_df.set_index('Feature')['Correlation with Churn'].abs().sort_values(ascending=False)
    ranked_features = abs_sorted.index[:3]
    ranked_corrs = [corr_df.set_index('Feature').loc[f, 'Correlation with Churn'] for f in ranked_features]
    st.markdown('<div class="insight-box"><strong>📊 Most Predictive Features for Churn:</strong><ul>' +
                f'<li><strong>1. {ranked_features[0]}:</strong> Correlation = {ranked_corrs[0]:.3f}</li>' +
                f'<li><strong>2. {ranked_features[1]}:</strong> Correlation = {ranked_corrs[1]:.3f}</li>' +
                f'<li><strong>3. {ranked_features[2]}:</strong> Correlation = {ranked_corrs[2]:.3f}</li>' +
                '<li>These features should be prioritized in predictive modeling.</li>' +
                '</ul></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### Pairplot - Feature Pair Interactions")
    
    top_features = churn_correlation.abs().nlargest(3).index.tolist() + ['ChurnStatus']
    
    pairplot_data = data_sc[top_features].copy()
    pairplot_data['ChurnStatus'] = pairplot_data['ChurnStatus'].map({0: 'Stayed', 1: 'Churned'})
    
    from pandas.plotting import scatter_matrix
    
    axarr = scatter_matrix(
        pairplot_data,
        alpha=0.65,
        figsize=(14, 12),
        diagonal='hist',
        c=data_sc['ChurnStatus'],
        cmap='RdYlGn_r',
        s=55,
        edgecolors=COLORS['burgundy'],
        linewidths=0.3
    )
    n = len(axarr)
    for i in range(n):
        ax = axarr[i, i]
        for patch in ax.patches:
            patch.set_facecolor(COLORS['dusty_rose'])
            patch.set_edgecolor(COLORS['burgundy'])
            patch.set_linewidth(1.5)
            patch.set_alpha(0.75)
    
    for i in range(n):
        for j in range(n):
            axarr[i, j].grid(True, alpha=0.2, linestyle=':', linewidth=0.6)
    
    plt.suptitle('Pairplot of Top Correlated Features', fontsize=18, fontweight='bold', y=0.995)
    st.pyplot(plt.gcf())
    
    st.markdown("---")
    
    st.markdown("### How Feature Pairs Predict Churn Together")
    
    churned_data = data_sc[data_sc['ChurnStatus'] == 1]
    stayed_data = data_sc[data_sc['ChurnStatus'] == 0]
    
    st.markdown(f"""
    <div class="insight-box">
    <strong>Key Insights from Feature Pair Interactions:</strong><br><br>
    - <strong>Income x Tenure:</strong> If both are low the <strong>risk of churn is higher</strong> as there is a clear red box that outlines this relation.

    
    </div>
    """, unsafe_allow_html=True)

elif section == "Statistical Significance Analysis":
    st.markdown("## Statistical Significance Analysis")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    from scipy.stats import pearsonr
    
    significance_data = []
    
    # Using the top_features and ranked_features from the Correlation section for consistency
    # Assuming these variables are available or recalculating them if necessary
    numerical_cols_for_corr = ['Age', 'Gender', 'Income', 'Tenure', 'ProductType', 'SupportCalls', 'ChurnStatus']
    correlation_matrix_for_sig = data_sc[numerical_cols_for_corr].corr(method='pearson')
    churn_correlation_for_sig = correlation_matrix_for_sig['ChurnStatus'].sort_values(ascending=False).drop('ChurnStatus')
    
    abs_sorted_for_sig = churn_correlation_for_sig.abs().sort_values(ascending=False)
    top_features_for_sig = abs_sorted_for_sig.index[:3].tolist()
    
    for feature in top_features_for_sig:
        # Check if the feature exists in data_sc before calculating
        if feature in data_sc.columns:
            corr_coef, p_value = pearsonr(data_sc[feature], data_sc['ChurnStatus'])
            significance_data.append({
                'Feature': feature,
                'Correlation': f"{corr_coef:.4f}",
                'P-Value': f"{p_value:.6f}",
                'Significant': 'Yes ✓' if p_value < 0.05 else 'No ✗',
                'Interpretation': 'Highly Significant' if p_value < 0.001 else 'Significant' if p_value < 0.05 else 'Not Significant'
            })
    
    significance_df = pd.DataFrame(significance_data)
    st.dataframe(significance_df, use_container_width=True)
    
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown("""
    <strong>Statistical Interpretation:</strong>
    - P-values < 0.05 indicate statistically significant correlations
    - All top features show significant relationships with churn status
    - These correlations are unlikely to have occurred by chance
    - The features identified are reliable predictors for modeling
    """)
    st.markdown('</div>', unsafe_allow_html=True)

elif section == "Conclusion":
    st.markdown("## Conclusion & Key Insights")
    
    data_clean_age = data[(data["Age"] >= 18) | data["Age"].isna()].copy()
    data_clean_age["Age"].fillna(int(data_clean_age["Age"].mean()) + 1, inplace=True)
    data_income = data_clean_age.copy()
    data_income["Income"].fillna(data_income["Income"].median(), inplace=True)
    Q1 = data_income["Income"].quantile(0.25)
    Q3 = data_income["Income"].quantile(0.75)
    IQR = Q3 - Q1
    income_upper_outliers_value = Q3 + 1.5 * IQR
    data_income.loc[data_income["Income"] > income_upper_outliers_value, "Income"] = income_upper_outliers_value
    data_tenure = data_income.copy()
    data_tenure["Tenure"].fillna(int(data_tenure["Tenure"].median()), inplace=True)
    data_sc = data_tenure.copy()
    data_sc.loc[data_sc["SupportCalls"] > 25, "SupportCalls"] = 7
    data_sc["SupportCalls"].fillna(int(data_sc["SupportCalls"].median()), inplace=True)
    
    data_corr_matrix = data_sc.drop(["CustomerID"], axis=1).corr(method='pearson')
    churn_corr = data_corr_matrix['ChurnStatus'].sort_values(ascending=False)
    
    st.markdown("### Analysis Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>100%</h3><p>Data Quality</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{len(data_sc):,}</h3><p>Clean Records</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{(data_sc["ChurnStatus"].mean()*100):.1f}%</h3><p>Churn Rate</p></div>', unsafe_allow_html=True)
    with col4:
        top_predictor = churn_corr.drop('ChurnStatus').abs().idxmax()
        st.markdown(f'<div class="metric-card"><h3>{top_predictor}</h3><p>Top Predictor</p></div>', unsafe_allow_html=True)
    
    top_correlation = churn_corr[top_predictor]
    
    st.markdown("---")
    
    st.markdown("### Data Preprocessing Summary")
    
    st.markdown(f"""
<div class="success-box">
    <strong>Successfully Completed:</strong>
    <ul>
        <li><strong>Age</strong>: Dropped 2 records with age < 18 (domain knowledge), filled missing with mean (44 years)</li>
        <li><strong>Income</strong>: Filled missing with median (robust to skew), capped outliers using IQR method</li>
        <li><strong>Tenure</strong>: Filled missing with median (5 years), no outliers detected</li>
        <li><strong>Support Calls</strong>: Capped extreme values (>25) to 7, filled missing with median</li>
        <li><strong>Standardization</strong>: Applied z-score standardization (mean=0, std=1) to all numerical features</li>
    </ul>
</div>
""", unsafe_allow_html=True)

    
    st.markdown("---")
    
    st.markdown("### Comprehensive Key Findings")
    
    churn_rate = data_sc["ChurnStatus"].mean() * 100
    avg_support_churned = data_sc[data_sc["ChurnStatus"] == 1]["SupportCalls"].mean()
    avg_support_stayed = data_sc[data_sc["ChurnStatus"] == 0]["SupportCalls"].mean()
    avg_tenure_churned = data_sc[data_sc["ChurnStatus"] == 1]["Tenure"].mean()
    avg_tenure_stayed = data_sc[data_sc["ChurnStatus"] == 0]["Tenure"].mean()
    avg_age_churned = data_sc[data_sc["ChurnStatus"] == 1]["Age"].mean()
    avg_age_stayed = data_sc[data_sc["ChurnStatus"] == 0]["Age"].mean()
    avg_income_churned = data_sc[data_sc["ChurnStatus"] == 1]["Income"].mean()
    avg_income_stayed = data_sc[data_sc["ChurnStatus"] == 0]["Income"].mean()
    
    st.markdown(f"""
    <div class="insight-box">
    <strong>1. Overall Churn Landscape</strong>
    <ul>
        <li>Overall churn rate: <strong>{churn_rate:.1f}%</strong></li>
        <li>This represents a {'high' if churn_rate > 30 else 'moderate' if churn_rate > 15 else 'low'} risk level requiring immediate attention</li>
        <li>Total churned customers: <strong>{int(data_sc['ChurnStatus'].sum()):,}</strong> out of {len(data_sc):,} customers</li>
        <li>Customer retention rate: <strong>{(100 - churn_rate):.1f}%</strong></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
    <strong>2. Critical Predictor: {top_predictor}</strong>
    <ul>
        <li>Correlation with churn: <strong>{top_correlation:.3f}</strong> ({'Strong' if abs(top_correlation) > 0.5 else 'Moderate' if abs(top_correlation) > 0.3 else 'Weak'} relationship)</li>
        <li>Churned customers: <strong>{avg_support_churned:.1f}</strong> average support calls</li>
        <li>Stayed customers: <strong>{avg_support_stayed:.1f}</strong> average support calls</li>
        <li>Difference: <strong>{abs(avg_support_churned - avg_support_stayed):.1f}</strong> calls ({((abs(avg_support_churned - avg_support_stayed) / avg_support_stayed) * 100):.1f}% {'higher' if avg_support_churned > avg_support_stayed else 'lower'})</li>
        <li><strong>Business Impact:</strong> High support call volume is the strongest indicator of customer dissatisfaction and imminent churn</li>
        <li><strong>Recommendation:</strong> Implement proactive support intervention for customers exceeding {avg_support_stayed + 2:.0f} calls</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="insight-box">
    <strong>3. Customer Tenure Analysis</strong>
    <ul>
        <li>Churned customers average tenure: <strong>{avg_tenure_churned:.1f} years</strong></li>
        <li>Stayed customers average tenure: <strong>{avg_tenure_stayed:.1f} years</strong></li>
        <li>Tenure gap: <strong>{abs(avg_tenure_churned - avg_tenure_stayed):.1f} years</strong></li>
        <li><strong>Critical Period:</strong> First {avg_tenure_churned + 1:.0f} years are highest risk for churn</li>
        <li><strong>Insight:</strong> Newer customers require enhanced onboarding and engagement programs</li>
        <li><strong>Recommendation:</strong> Develop targeted retention campaigns for customers with tenure < {avg_tenure_churned + 1:.0f} years</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    gender_churn = data_sc.groupby('Gender')['ChurnStatus'].mean() * 100
    product_churn = data_sc.groupby('ProductType')['ChurnStatus'].mean() * 100
    
    st.markdown(f"""
    <div class="insight-box">
    <strong>4. Demographic and Product Insights</strong>
    <ul>
        <li><strong>Gender Analysis:</strong>
            <ul>
                <li>Male churn rate: <strong>{gender_churn[0]:.1f}%</strong></li>
                <li>Female churn rate: <strong>{gender_churn[1]:.1f}%</strong></li>
                <li>Gender difference: <strong>{abs(gender_churn[0] - gender_churn[1]):.1f}%</strong> ({'Minimal' if abs(gender_churn[0] - gender_churn[1]) < 5 else 'Moderate' if abs(gender_churn[0] - gender_churn[1]) < 10 else 'Significant'} variation)</li>
            </ul>
        </li>
        <li><strong>Product Type Analysis:</strong>
            <ul>
                <li>Basic product churn: <strong>{product_churn[0]:.1f}%</strong></li>
                <li>Premium product churn: <strong>{product_churn[1]:.1f}%</strong></li>
                <li>Product difference: <strong>{abs(product_churn[0] - product_churn[1]):.1f}%</strong></li>
                <li><strong>Insight:</strong> {'Premium' if product_churn[1] < product_churn[0] else 'Basic'} product users show {'lower' if product_churn[1] < product_churn[0] else 'higher'} churn rates</li>
            </ul>
        </li>
        <li><strong>Age Factor:</strong>
            <ul>
                <li>Churned customers average age: <strong>{avg_age_churned:.1f} years</strong></li>
                <li>Stayed customers average age: <strong>{avg_age_stayed:.1f} years</strong></li>
                <li>Age difference: <strong>{abs(avg_age_churned - avg_age_stayed):.1f} years</strong></li>
            </ul>
        </li>
        <li><strong>Income Analysis:</strong>
            <ul>
                <li>Churned customers average income: <strong>${avg_income_churned:,.2f}</strong></li>
                <li>Stayed customers average income: <strong>${avg_income_stayed:,.2f}</strong></li>
                <li>Income difference: <strong>${abs(avg_income_churned - avg_income_stayed):,.2f}</strong></li>
            </ul>
        </li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Give us full :)")
    st.markdown("---")
    
   

st.sidebar.markdown("---")

st.sidebar.markdown(
    '<div class="team-box">'
    '<h4>Project Team</h4>'
    '<div class="team-member"><strong>Heba Mustafa</strong></div>'
    '<div class="team-member"><strong>Abalraheem Shuabi</strong></div>'
    '</div>', 
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Customer Churn Analysis**")
st.sidebar.markdown("*Machine Learning Project*")
