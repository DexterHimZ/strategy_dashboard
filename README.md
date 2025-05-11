
# 📈 Stock Strategy Visual Dashboard

This is an interactive Streamlit web app for visualizing stock forecasting results, portfolio allocations, and correlation analysis — all powered by real backtested data.

---

## 🚀 Features

- 🔮 **Forecast Plot**: Visualize LSTM-predicted vs actual stock prices.
- 📉 **Trend & Volatility**: Rolling mean and standard deviation over time.
- 📊 **Portfolio Allocation**:
  - Pie chart with grouped "Others" for tiny weights
  - Bar chart for quick comparison
- 🔥 **Correlation Heatmap**: Diversification insights via return correlations.

---

## 📁 Project Structure

```
📦 strategy-dashboard/
├── stock_dashboard_grouped.py         # Streamlit app
├── requirements.txt                   # Required Python packages
├── README.md                          # This file
└── strategy_dashboard_data/           # Exported CSV data
    ├── RELIANCE.NS_data.csv
    ├── RELIANCE.NS_forecast.csv
    ├── ...
    ├── portfolio.csv
    └── returns.csv
```

---

## ⚙️ Setup

### 🐍 Install dependencies
```bash
pip install -r requirements.txt
```

### ▶️ Run the app locally
```bash
streamlit run stock_dashboard_grouped.py
```

---

## ☁️ Check out my deployed app
https://himz-strategy.streamlit.app/
---

## 🧠 Notes

- Portfolio weights are normalized and cleaned automatically.
- Tiny allocations (<1%) are grouped into "Others" for clarity.
- All plots are interactive and mobile-friendly.

---

Made by Himangshu with ❤️ using [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).
