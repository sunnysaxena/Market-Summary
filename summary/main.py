import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from components.loader import show_loader
from utils.stock_data import get_stock_data, get_stock_info
from utils.constants import SAMPLE_SYMBOLS, SYMBOLS

# Page configuration
st.set_page_config(
    page_title="Stock OHLC Viewer",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title and description
st.title("📈 Market Summary Viewer")
st.markdown("""
<div class="custom-info-box">
    View historical OHLC (Open-High-Low-Close) data for stocks with an elegant interface.
    Select a stock symbol and date range to get started.
</div>
""", unsafe_allow_html=True)

# Add Stock Image Above "Configuration"
st.sidebar.image("data/image2.png", use_container_width=True)

# Add Space Between Image and Configuration Title
st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Two line breaks for spacing

# Sidebar configuration
st.sidebar.title("\nConfiguration")

selected_symbol = st.sidebar.selectbox(
    "Select Stock Symbol",
    options=SAMPLE_SYMBOLS,
    index=0,
    help="Choose a stock symbol to view its OHLC data"
)

# Date range selection
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30), max_value=datetime.now())
with col2:
    end_date = st.date_input("End Date", value=datetime.now(), max_value=datetime.now())

# Fetch and display data
try:
    # Show loading animation
    show_loader()

    # Get stock information
    stock_info = get_stock_info(SYMBOLS[selected_symbol])

    # Display stock information
    st.markdown(f"""
    ### {stock_info['name']} ({selected_symbol})
    **Sector:** {stock_info['sector']} | **Currency:** {stock_info['currency']}
    """)

    # Fetch OHLC data
    df = get_stock_data(SYMBOLS[selected_symbol], start_date, end_date)

    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)
    latest_data = df.iloc[-1]

    with col1:
        st.metric("Latest Close", f"{latest_data['Close']:.2f}")
    with col2:
        st.metric("Latest Open", f"{latest_data['Open']:.2f}")
    with col3:
        st.metric("Latest High", f"{latest_data['High']:.2f}")
    with col4:
        st.metric("Latest Low", f"{latest_data['Low']:.2f}")

    # 🟢 Candlestick Chart
    st.markdown("### Candlestick Chart")

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing=dict(line=dict(color='green')),
                decreasing=dict(line=dict(color='red')),
            )
        ]
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        template="plotly_white",
        height=400,
    )

    st.plotly_chart(fig, use_container_width=True)

    # 🟢 Styled Data Table
    st.markdown("### Historical OHLC Data")

    def style_dataframe(df):
        def highlight_cols(s):
            if s.name == 'MKT Change':
                return ['background-color: #d4edda; color: #155724;'] * len(s)  # Green
            elif s.name == 'Trend':
                return ['background-color: #cce5ff; color: #004085;'] * len(s)  # Blue
            elif s.name == 'Open Close':
                return ['background-color: #fff3cd; color: #856404;'] * len(s)  # Yellow
            else:
                return [''] * len(s)

        def highlight_values(val):
            color = 'background-color: #d4edda; color: #155724;' if val > 0 else \
                'background-color: #f8d7da; color: #721c24;' if val < 0 else ''
            return color

        return df.style.format({
            'Open': '{:.2f}',
            'High': '{:.2f}',
            'Low': '{:.2f}',
            'Close': '{:.2f}',
            'Open High': '{:.2f}',
            'Open Low': '{:.2f}',
            'Open Close': '{:.2f}',
            'Volume': '{:,.0f}'
        }).apply(highlight_cols, axis=0).set_table_styles([
            {'selector': 'thead th', 'props': [('font-weight', 'bold'), ('font-size', '14px')]}
        ]).map(highlight_values, subset=['Open Change', 'MKT Change', 'Open Close'])

    st.dataframe(style_dataframe(df), use_container_width=True, height=400)

    # 🟢 Download Data Button
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data",
        data=csv,
        file_name=f"{selected_symbol}_OHLC_data.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Error: {str(e)}")

# Footer
st.markdown("""
---
<div style="text-align: center; color: #666666; font-size: 0.8rem;">
    Data provided by Yahoo Finance | Created with Streamlit
</div>
""", unsafe_allow_html=True)
