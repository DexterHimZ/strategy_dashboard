
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff
import os

st.set_page_config(page_title="Stock Strategy Visual Dashboard", layout="wide")

# === 🔥 Custom Landing Section ===
st.title("📈 Stock Strategy Visual Dashboard by Himz")
st.markdown("### Deep learning meets portfolio insights.")
st.markdown("🚀 This app visualizes LSTM-based stock forecasts, trend analytics, portfolio allocations, and correlation heatmaps.")
st.markdown("[📓 View My Original Colab Notebook](https://colab.research.google.com/drive/1AZPz8GJtjz19S8kya9hE5pUT6TlWbcPX#scrollTo=WAZYT21VvCXz)")

st.markdown("---")

# Load files
base_path = "strategy_dashboard_data"
tickers = sorted([f.replace("_data.csv", "") for f in os.listdir(base_path) if f.endswith("_data.csv")])

@st.cache_data
def load_data():
    ticker_data = {}
    ticker_forecasts = {}
    
    for ticker in tickers:
        df = pd.read_csv(f"{base_path}/{ticker}_data.csv", index_col=0, parse_dates=True)
        df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
        ticker_data[ticker] = df

        preds = pd.read_csv(f"{base_path}/{ticker}_forecast.csv")["Predicted"].values
        ticker_forecasts[ticker] = preds

    # Load and fix portfolio
    portfolio_df = pd.read_csv(f"{base_path}/portfolio.csv", index_col=0)
    portfolio = pd.to_numeric(portfolio_df.iloc[:, -1], errors="coerce").dropna()

    # Group small weights into "Others"
    threshold = 0.01
    large = portfolio[portfolio > threshold]
    small_sum = portfolio[portfolio <= threshold].sum()
    if small_sum > 0:
        large["Others"] = small_sum
    if large.sum() > 0:
        portfolio = large / large.sum()
    else:
        portfolio = large

    returns = pd.read_csv(f"{base_path}/returns.csv", index_col=0)

    return ticker_data, ticker_forecasts, portfolio, returns

data, forecasts, portfolio, returns = load_data()

# === App Functionality ===
ticker = st.selectbox("Select Ticker", tickers)

# Forecast Plot
df = data[ticker]
preds = forecasts[ticker]
test_idx = df.index[-len(preds):]

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Actual", line=dict(color="green")))
fig1.add_trace(go.Scatter(x=test_idx, y=preds, name="Predicted", line=dict(color="red", dash="dash")))
fig1.update_layout(title=f"{ticker}: Actual vs Predicted", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig1, use_container_width=True)

# Trend & Volatility
df["RollingMean"] = df["Close"].rolling(window=20).mean()
df["Volatility"] = df["Close"].rolling(window=20).std()

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close Price"))
fig2.add_trace(go.Scatter(x=df.index, y=df["RollingMean"], name="20D MA"))
fig2.add_trace(go.Scatter(x=df.index, y=df["Volatility"], name="Volatility"))
fig2.update_layout(title=f"{ticker}: Trend & Volatility", xaxis_title="Date")
st.plotly_chart(fig2, use_container_width=True)

# Portfolio Allocation
st.subheader("📊 Portfolio Allocation")
col1, col2 = st.columns(2)

with col1:
    if not portfolio.empty:
        fig3 = px.pie(values=portfolio.values, names=portfolio.index, title="Portfolio (Pie)")
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Portfolio is empty or filtered to nothing.")

with col2:
    if not portfolio.empty:
        bar_df = pd.DataFrame({"Ticker": portfolio.index, "Weight": portfolio.values})
        fig4 = px.bar(bar_df, x="Ticker", y="Weight", title="Portfolio (Bar)")
        st.plotly_chart(fig4, use_container_width=True)

# Correlation Heatmap
st.subheader("🔥 Correlation Heatmap")
corr = returns.corr().round(2)
fig5 = ff.create_annotated_heatmap(z=corr.values,
                                   x=corr.columns.tolist(),
                                   y=corr.index.tolist(),
                                   colorscale='Viridis')
fig5.update_layout(width=800, height=800)
st.plotly_chart(fig5, use_container_width=True)
