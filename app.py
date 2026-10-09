
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# 2. Project Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA" / "PROCESSED"

# --------------------------------------------------
# 3. Load Week 3 Results
# --------------------------------------------------
@st.cache_data
def load_data():
    lightgbm_path = DATA_DIR / "lightgbm_forecast_FOODS_3_090_CA_3.csv"
    prophet_path = DATA_DIR / "prophet_forecast_FOODS_3_090_CA_3.csv"
    comparison_path = DATA_DIR / "model_comparison.csv"

    lightgbm = pd.read_csv(lightgbm_path)
    prophet = pd.read_csv(prophet_path)
    comparison = pd.read_csv(comparison_path)

    # Standardize date columns
    lightgbm["date"] = pd.to_datetime(lightgbm["date"])
    prophet["ds"] = pd.to_datetime(prophet["ds"])

    return lightgbm, prophet, comparison


# --------------------------------------------------
# 4. Application Header and Sidebar
# --------------------------------------------------
st.title("📊 Retail Demand Forecasting & Inventory Optimization")
st.caption("Week 4 | Demand Analytics Dashboard")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select a module",
    [
        "Dashboard",
        "Demand Forecasting",
        "Model Comparison",
        "Inventory Optimization",
        "What-if Analysis"
    ]
)

# --------------------------------------------------
# 5. Load Data and Display Selected Page
# --------------------------------------------------
try:
    lightgbm, prophet, comparison = load_data()

    st.sidebar.success("Forecast data loaded")

    # Dashboard
    if page == "Dashboard":
        st.subheader("Retail Demand Overview")

        total_demand = lightgbm["actual"].sum()
        avg_demand = lightgbm["actual"].mean()

        best_model = comparison.loc[
            comparison["WMAPE (%)"].idxmin(), "Model"
        ]
        best_wmape = comparison["WMAPE (%)"].min()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Test Period Demand", f"{total_demand:,.0f}")
        col2.metric("Average Daily Demand", f"{avg_demand:,.1f}")
        col3.metric("Best Model", str(best_model))
        col4.metric("Best WMAPE", f"{best_wmape:.2f}%")

        st.subheader("Model Performance")
        st.dataframe(comparison, width="stretch")

        st.subheader("Recent Forecast Results")
        st.dataframe(
            lightgbm.sort_values("date").tail(10),
            width="stretch"
        )

    # Demand Forecasting
    elif page == "Demand Forecasting":
        st.subheader("📈 Actual vs Predicted Demand")

        # Prepare LightGBM results
        lgb_plot = lightgbm[
            ["date", "actual", "predicted"]
        ].copy()

        lgb_plot = lgb_plot.sort_values("date")

        # Prepare Prophet results
        prophet_plot = prophet[
            ["ds", "yhat"]
        ].copy()

        prophet_plot = prophet_plot.rename(
            columns={
                "ds": "date",
                "yhat": "Prophet Forecast"
            }
        )

        # Merge forecasts using the date
        chart_data = lgb_plot.merge(
            prophet_plot,
            on="date",
            how="left"
        )

        chart_data = chart_data.rename(
            columns={
                "actual": "Actual Demand",
                "predicted": "LightGBM Forecast"
            }
        )

        chart_data = chart_data.set_index("date")

        st.caption(
            "Product: FOODS_3_090 | Store: CA_3 | "
            "Historical test period: 30 days"
        )

        # Interactive time-series chart
        st.line_chart(
            chart_data[
                [
                    "Actual Demand",
                    "Prophet Forecast",
                    "LightGBM Forecast"
                ]
            ],
            x_label="Date",
            y_label="Units Sold"
        )

        st.subheader("Forecast Data")
        st.dataframe(
            chart_data.reset_index(),
            width="stretch"
        )

    # Model Comparison

    elif page == "Model Comparison":
        st.subheader("🤖 Prophet vs LightGBM")

        st.caption(
            "Performance comparison on the same 30-day historical test period."
        )

        # Display model metrics
        st.dataframe(comparison, width="stretch")

        # Display key metrics for both models
        prophet_row = comparison[
            comparison["Model"] == "Prophet"
        ].iloc[0]

        lightgbm_row = comparison[
            comparison["Model"] == "LightGBM"
        ].iloc[0]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Prophet")
            st.metric("MAE", f"{prophet_row['MAE']:.2f}")
            st.metric("RMSE", f"{prophet_row['RMSE']:.2f}")
            st.metric("WMAPE", f"{prophet_row['WMAPE (%)']:.2f}%")

        with col2:
            st.markdown("### LightGBM")
            st.metric("MAE", f"{lightgbm_row['MAE']:.2f}")
            st.metric("RMSE", f"{lightgbm_row['RMSE']:.2f}")
            st.metric("WMAPE", f"{lightgbm_row['WMAPE (%)']:.2f}%")

        # Metric comparison charts
        st.subheader("MAE Comparison")
        st.bar_chart(
            comparison.set_index("Model")[["MAE"]],
            x_label="Model",
            y_label="MAE"
        )

        st.subheader("RMSE Comparison")
        st.bar_chart(
            comparison.set_index("Model")[["RMSE"]],
            x_label="Model",
            y_label="RMSE"
        )

        st.subheader("WMAPE Comparison")
        st.bar_chart(
            comparison.set_index("Model")[["WMAPE (%)"]],
            x_label="Model",
            y_label="WMAPE (%)"
        )

        st.success(
            "LightGBM has lower error values across all three metrics "
            "for the evaluated test period."
        )


        st.subheader("MAE Comparison")
        st.bar_chart(
            comparison.set_index("Model")[["MAE"]],
            x_label="Model",
            y_label="Mean Absolute Error"
        )

        st.subheader("RMSE Comparison")
        st.bar_chart(
            comparison.set_index("Model")[["RMSE"]],
            x_label="Model",
            y_label="Root Mean Squared Error"
        )

        st.subheader("WMAPE Comparison")
        st.bar_chart(
            comparison.set_index("Model")[["WMAPE (%)"]],
            x_label="Model",
            y_label="WMAPE (%)"
        )

        st.info(
            f"{best_model if 'best_model' in locals() else comparison.loc[comparison['WMAPE (%)'].idxmin(), 'Model']} "
            "has the lowest WMAPE in the saved model comparison."
        )

    # Inventory Optimization

    elif page == "Inventory Optimization":
        st.subheader("📦 Inventory Optimization")

        st.write(
            "Calculate recommended stock levels using historical "
            "demand, demand variability, and supplier lead time."
        )

        # User inputs
        col1, col2, col3 = st.columns(3)

        with col1:
            lead_time = st.number_input(
                "Supplier Lead Time (days)",
                min_value=1,
                max_value=90,
                value=5,
                step=1
            )

        with col2:
            current_stock = st.number_input(
                "Current Inventory (units)",
                min_value=0,
                value=500,
                step=10
            )

        with col3:
            service_level = st.selectbox(
                "Target Service Level",
                ["90%", "95%", "99%"],
                index=1
            )

        # Calculate demand statistics from historical test observations
        daily_demand = lightgbm["actual"].astype(float)

        avg_daily_demand = daily_demand.mean()
        demand_std = daily_demand.std(ddof=1)

        # Z-scores for approximate normal service levels
        z_scores = {
            "90%": 1.282,
            "95%": 1.645,
            "99%": 2.326
        }

        z = z_scores[service_level]

        # Inventory calculations
        safety_stock = z * demand_std * (lead_time ** 0.5)

        lead_time_demand = avg_daily_demand * lead_time

        reorder_point = lead_time_demand + safety_stock

        # Planning stock: 30-day demand plus safety stock
        planning_days = 30
        recommended_inventory = (
            avg_daily_demand * planning_days + safety_stock
        )

        additional_stock = max(
            0,
            recommended_inventory - current_stock
        )

        # KPI cards
        st.divider()
        st.subheader("Recommended Inventory Metrics")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Average Daily Demand",
            f"{avg_daily_demand:.1f} units"
        )

        c2.metric(
            "Safety Stock",
            f"{safety_stock:.0f} units"
        )

        c3.metric(
            "Reorder Point",
            f"{reorder_point:.0f} units"
        )

        c4, c5 = st.columns(2)

        c4.metric(
            "30-Day Recommended Inventory",
            f"{recommended_inventory:.0f} units"
        )

        c5.metric(
            "Additional Stock Needed",
            f"{additional_stock:.0f} units"
        )

        # Inventory status
        st.subheader("Inventory Status")

        if current_stock <= reorder_point:
            st.error(
                "Critical: Current stock is at or below the reorder point. "
                "Consider placing a replenishment order."
            )
        elif current_stock < recommended_inventory:
            st.warning(
                "Low: Current stock is below the recommended "
                "30-day inventory level."
            )
        else:
            st.success(
                "Sufficient: Current stock meets the recommended "
                "30-day inventory level."
            )

        # Explanation
        with st.expander("How are these values calculated?"):
            st.markdown("""
            - **Safety Stock:** Z-score × demand standard deviation × √lead time
            - **Lead-Time Demand:** Average daily demand × lead time
            - **Reorder Point:** Lead-time demand + safety stock
            - **Recommended Inventory:** 30-day expected demand + safety stock

            These are baseline estimates. They assume demand variability
            is reasonably stable and daily demand observations are
            approximately independent for the safety-stock calculation.
            """)


    # What-if Analysis

    elif page == "What-if Analysis":
        st.subheader("🔄 What-if Analysis")

        st.write(
            "Explore how changes in demand, price, and supplier lead time "
            "affect your inventory requirements."
        )

        # Scenario inputs
        col1, col2, col3 = st.columns(3)

        with col1:
            demand_change = st.slider(
                "Demand Change (%)",
                min_value=-20,
                max_value=20,
                value=0,
                step=5
            )

        with col2:
            price_change = st.slider(
                "Price Change (%)",
                min_value=-10,
                max_value=10,
                value=0,
                step=5
            )

        with col3:
            scenario_lead_time = st.slider(
                "Supplier Lead Time (days)",
                min_value=1,
                max_value=30,
                value=5
            )

        # Baseline demand statistics
        base_daily_demand = lightgbm["actual"].astype(float).mean()
        base_demand_std = lightgbm["actual"].astype(float).std(ddof=1)

        # Scenario assumptions
        scenario_daily_demand = max(
            0,
            base_daily_demand * (1 + demand_change / 100)
        )

        # Price changes are displayed as a scenario assumption.
        # This does not retrain the model or estimate price elasticity.
        base_price_index = 100
        scenario_price_index = base_price_index * (
            1 + price_change / 100
        )

        z = 1.645  # Approximate 95% service level

        scenario_safety_stock = (
            z
            * base_demand_std
            * (1 + demand_change / 100)
            * (scenario_lead_time ** 0.5)
        )

        scenario_reorder_point = (
            scenario_daily_demand * scenario_lead_time
            + scenario_safety_stock
        )

        scenario_inventory = (
            scenario_daily_demand * 30
            + scenario_safety_stock
        )

        # Baseline metrics
        baseline_reorder_point = (
            base_daily_demand * 5
            + 1.645 * base_demand_std * (5 ** 0.5)
        )

        baseline_inventory = (
            base_daily_demand * 30
            + 1.645 * base_demand_std * (5 ** 0.5)
        )

        st.divider()
        st.subheader("Scenario Results")

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Scenario Daily Demand",
            f"{scenario_daily_demand:.1f} units",
            delta=f"{scenario_daily_demand - base_daily_demand:+.1f}"
        )

        c2.metric(
            "Scenario Reorder Point",
            f"{scenario_reorder_point:.0f} units",
            delta=f"{scenario_reorder_point - baseline_reorder_point:+.0f} vs baseline"
        )

        c3.metric(
            "30-Day Stock Requirement",
            f"{scenario_inventory:.0f} units",
            delta=f"{scenario_inventory - baseline_inventory:+.0f} vs baseline"
        )

        st.metric(
            "Scenario Price Index",
            f"{scenario_price_index:.0f}",
            delta=f"{price_change:+d}%"
        )

        st.info(
            "Interpretation: demand and lead-time changes affect the "
            "inventory calculations. Price change is shown as a scenario "
            "index only; demand is not automatically changed by price "
            "because price elasticity has not been estimated."
        )

        with st.expander("Scenario assumptions"):
            st.markdown("""
            - Baseline demand comes from the historical evaluation period.
            - The demand slider adjusts baseline daily demand proportionally.
            - Safety stock uses an approximate 95% service level.
            - Reorder point = lead-time demand + safety stock.
            - Stock requirement = 30-day demand + safety stock.
            - Price changes do not directly alter demand predictions in this version.
            """)


except FileNotFoundError as e:
    st.error(f"Required CSV file not found: {e}")
    st.info(
        "Check that the forecast and comparison CSV files exist "
        "inside DATA/PROCESSED."
    )

except (KeyError, ValueError) as e:
    st.error(f"Could not load or interpret the forecast data: {e}")
    st.info(
        "Check the column names in the three Week 3 CSV files."
    )
