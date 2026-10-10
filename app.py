import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Retail Demand Forecasting", page_icon="📊", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA" / "PROCESSED"


@st.cache_data
def load_data():
    lightgbm = pd.read_csv(DATA_DIR / "lightgbm_forecast_FOODS_3_090_CA_3.csv")
    prophet = pd.read_csv(DATA_DIR / "prophet_forecast_FOODS_3_090_CA_3.csv")
    comparison = pd.read_csv(DATA_DIR / "model_comparison.csv")

    required_lgb = {"date", "actual", "predicted"}
    required_prophet = {"ds", "yhat"}
    required_comparison = {"Model", "MAE", "RMSE", "WMAPE (%)"}
    if not required_lgb.issubset(lightgbm.columns):
        raise ValueError(f"LightGBM CSV must contain {sorted(required_lgb)}")
    if not required_prophet.issubset(prophet.columns):
        raise ValueError(f"Prophet CSV must contain {sorted(required_prophet)}")
    if not required_comparison.issubset(comparison.columns):
        raise ValueError(f"Model comparison CSV must contain {sorted(required_comparison)}")

    lightgbm["date"] = pd.to_datetime(lightgbm["date"], errors="coerce")
    prophet["ds"] = pd.to_datetime(prophet["ds"], errors="coerce")
    lightgbm = lightgbm.dropna(subset=["date", "actual", "predicted"])
    prophet = prophet.dropna(subset=["ds", "yhat"])
    return lightgbm, prophet, comparison


st.title("📊 Retail Demand Forecasting & Inventory Optimization")
st.caption("Week 4 | Demand Analytics Dashboard")
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a module",
    ["Dashboard", "Demand Forecasting", "Model Comparison",
     "Inventory Optimization", "What-if Analysis"],
)

try:
    lightgbm, prophet, comparison = load_data()
    st.sidebar.success("Forecast data loaded")
    best_model = comparison.loc[comparison["WMAPE (%)"].idxmin(), "Model"]
    best_wmape = float(comparison["WMAPE (%)"].min())

    if page == "Dashboard":
        st.subheader("Retail Demand Overview")
        total_demand = lightgbm["actual"].sum()
        avg_demand = lightgbm["actual"].mean()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Test Period Demand", f"{total_demand:,.0f}")
        c2.metric("Average Daily Demand", f"{avg_demand:,.1f}")
        c3.metric("Best Model", str(best_model))
        c4.metric("Best WMAPE", f"{best_wmape:.2f}%")
        st.subheader("Model Performance")
        st.dataframe(comparison, width="stretch")
        st.subheader("Recent Forecast Results")
        st.dataframe(lightgbm.sort_values("date").tail(10), width="stretch")

    elif page == "Demand Forecasting":
        st.subheader("📈 Actual vs Predicted Demand")
        lgb_plot = lightgbm[["date", "actual", "predicted"]].copy().sort_values("date")
        prophet_plot = prophet[["ds", "yhat"]].copy().rename(
            columns={"ds": "date", "yhat": "Prophet Forecast"}
        )
        chart_data = lgb_plot.merge(prophet_plot, on="date", how="left").rename(
            columns={"actual": "Actual Demand", "predicted": "LightGBM Forecast"}
        ).set_index("date")
        st.caption("Product: FOODS_3_090 | Store: CA_3 | Historical holdout period: 30 days")
        st.line_chart(
            chart_data[["Actual Demand", "Prophet Forecast", "LightGBM Forecast"]],
            x_label="Date", y_label="Units Sold",
        )
        st.subheader("Forecast Data")
        st.dataframe(chart_data.reset_index(), width="stretch")

    elif page == "Model Comparison":
        st.subheader("🤖 Prophet vs LightGBM")
        st.caption("Comparison on the same 30-day historical holdout period.")
        st.dataframe(comparison, width="stretch")
        columns = st.columns(2)
        for column, name in zip(columns, ["Prophet", "LightGBM"]):
            rows = comparison[comparison["Model"].str.casefold() == name.casefold()]
            with column:
                st.markdown(f"### {name}")
                if rows.empty:
                    st.warning(f"No {name} row found in model_comparison.csv.")
                else:
                    row = rows.iloc[0]
                    st.metric("MAE", f"{float(row['MAE']):.2f}")
                    st.metric("RMSE", f"{float(row['RMSE']):.2f}")
                    st.metric("WMAPE", f"{float(row['WMAPE (%)']):.2f}%")
        st.subheader("MAE Comparison")
        st.bar_chart(comparison.set_index("Model")[["MAE"]], x_label="Model", y_label="Mean Absolute Error")
        st.subheader("RMSE Comparison")
        st.bar_chart(comparison.set_index("Model")[["RMSE"]], x_label="Model", y_label="Root Mean Squared Error")
        st.subheader("WMAPE Comparison")
        st.bar_chart(comparison.set_index("Model")[["WMAPE (%)"]], x_label="Model", y_label="WMAPE (%)")
        st.success(f"{best_model} has the lowest WMAPE ({best_wmape:.2f}%) on this holdout period.")

    elif page == "Inventory Optimization":
        st.subheader("📦 Inventory Optimization")
        st.write("Estimate stock levels using demand observations from the 30-day historical evaluation period.")
        c1, c2, c3 = st.columns(3)
        with c1:
            lead_time = st.number_input("Supplier Lead Time (days)", min_value=1, max_value=90, value=5, step=1)
        with c2:
            current_stock = st.number_input("Current Inventory (units)", min_value=0, value=500, step=10)
        with c3:
            service_level = st.selectbox("Target Service Level", ["90%", "95%", "99%"], index=1)

        daily = lightgbm["actual"].astype(float)
        avg = float(daily.mean())
        std = float(daily.std(ddof=1)) if len(daily) > 1 else 0.0
        z = {"90%": 1.282, "95%": 1.645, "99%": 2.326}[service_level]
        safety = z * std * (lead_time ** 0.5)
        reorder = avg * lead_time + safety
        recommended = avg * 30 + safety
        additional = max(0, recommended - current_stock)

        st.divider()
        st.subheader("Recommended Inventory Metrics")
        a, b, c = st.columns(3)
        a.metric("Average Daily Demand", f"{avg:.1f} units")
        b.metric("Safety Stock", f"{safety:.0f} units")
        c.metric("Reorder Point", f"{reorder:.0f} units")
        d, e = st.columns(2)
        d.metric("30-Day Recommended Inventory", f"{recommended:.0f} units")
        e.metric("Additional Stock Needed", f"{additional:.0f} units")
        st.subheader("Inventory Status")
        if current_stock <= reorder:
            st.error("Critical: Current stock is at or below the reorder point. Consider replenishment.")
        elif current_stock < recommended:
            st.warning("Low: Current stock is below the recommended 30-day inventory level.")
        else:
            st.success("Sufficient: Current stock meets the recommended 30-day inventory level.")
        with st.expander("How are these values calculated?"):
            st.markdown("""
            - **Safety stock:** Z-score × demand standard deviation × √lead time
            - **Lead-time demand:** Average daily demand × lead time
            - **Reorder point:** Lead-time demand + safety stock
            - **Recommended inventory:** 30-day expected demand + safety stock

            **Limitation:** These estimates currently use the 30-day evaluation observations,
            not the full historical demand series. Validate with longer history before operational use.
            """)

    elif page == "What-if Analysis":
        st.subheader("🔄 What-if Analysis")
        st.write("Explore demand changes, assumed price sensitivity, and supplier lead time.")
        c1, c2, c3 = st.columns(3)
        with c1:
            demand_change = st.slider("Other Demand Change (%)", -20, 20, 0, step=5)
        with c2:
            price_change = st.slider("Price Change (%)", -10, 10, 0, step=5)
        with c3:
            scenario_lead_time = st.slider("Supplier Lead Time (days)", 1, 30, 5)

        elasticity = st.slider(
            "Assumed Price Elasticity", min_value=-2.0, max_value=0.0,
            value=-1.0, step=0.25,
            help="Scenario assumption only; it is not a measured causal estimate.",
        )
        daily = lightgbm["actual"].astype(float)
        base_daily = float(daily.mean())
        base_std = float(daily.std(ddof=1)) if len(daily) > 1 else 0.0

        # Constant-elasticity scenario. This does not retrain either forecasting model.
        price_ratio = 1 + price_change / 100
        price_factor = price_ratio ** elasticity
        other_factor = 1 + demand_change / 100
        scenario_daily = max(0.0, base_daily * price_factor * other_factor)

        z = 1.645  # Approximate 95% service level
        scenario_std = base_std * price_factor * other_factor
        safety = z * scenario_std * (scenario_lead_time ** 0.5)
        reorder = scenario_daily * scenario_lead_time + safety
        inventory = scenario_daily * 30 + safety


        # Baseline comparison: use the SAME lead time as the scenario.
        baseline_safety = z * base_std * (scenario_lead_time ** 0.5)

        baseline_reorder = (
            base_daily * scenario_lead_time + baseline_safety
        )

        baseline_inventory = (
            base_daily * 30 + baseline_safety
        )

        price_only_pct = (price_factor - 1) * 100

        st.caption("Product: FOODS_3_090 | Store: CA_3 | Baseline: 30-day historical evaluation period")
        st.divider()
        st.subheader("Scenario Results")
        a, b, c = st.columns(3)
        a.metric("Scenario Daily Demand", f"{scenario_daily:.1f} units", delta=f"{scenario_daily - base_daily:+.1f} units vs baseline")
        b.metric("Scenario Reorder Point", f"{reorder:.0f} units", delta=f"{reorder - baseline_reorder:+.0f} vs baseline")
        c.metric("30-Day Stock Requirement", f"{inventory:.0f} units", delta=f"{inventory - baseline_inventory:+.0f} vs baseline")
        d, e = st.columns(2)
        d.metric("Assumed Price Elasticity", f"{elasticity:.2f}")
        e.metric("Demand Change from Price Alone", f"{price_only_pct:+.1f}%", delta=f"Price change: {price_change:+d}%")
        st.info(
            "This is a transparent scenario calculation, not a validated price-demand forecast. "
            "The elasticity is user-assumed. The exploratory historical regression produced an "
            "unstable positive coefficient and is not used here. Validate price effects before business decisions."
        )
        with st.expander("Scenario assumptions and formulas"):
            st.markdown("""
            - **Price demand factor:** (1 + price change) raised to assumed price elasticity.
            - **Scenario demand:** Baseline demand × price factor × other demand factor.
            - **Safety stock:** 1.645 × adjusted demand standard deviation × √lead time (approximately 95% service level).
            - **Reorder point:** Scenario daily demand × lead time + safety stock.
            - **30-day stock requirement:** Scenario daily demand × 30 + safety stock.
            - The assumed elasticity is not a measured causal effect.
            - Price changes do not retrain Prophet or LightGBM.
            """)

except FileNotFoundError as e:
    st.error(f"Required CSV file not found: {e}")
    st.info("Check that the forecast and comparison CSV files exist inside DATA/PROCESSED.")
except (KeyError, ValueError, IndexError) as e:
    st.error(f"Could not load or interpret the forecast data: {e}")
    st.info("Check the column names and model names in the Week 3 CSV files.")
