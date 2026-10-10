import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Retail Demand Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={},
)

# --------------------------------------------------
# RETAIL ANALYTICS UI THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
    :root {
        --navy: #12213B;
        --navy-2: #1B3154;
        --ink: #17243B;
        --muted: #5D6B82;
        --canvas: #F4F7FB;
        --card: #FFFFFF;
        --border: #E0E7F0;
        --blue: #2563EB;
    }

    .stApp {
        background: var(--canvas);
        color: var(--ink);
        font-family: "Segoe UI", Inter, Arial, sans-serif;
    }

    .main .block-container {
        max-width: 1440px;
        padding: 1.5rem 2rem 3rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--navy) 0%, var(--navy-2) 100%);
        border-right: 1px solid #263B5B;
    }

    section[data-testid="stSidebar"] * {
        color: #F1F5F9;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #D7E3F4;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #F1F5F9 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stAlert"] {
        background: rgba(15, 118, 110, 0.28);
        border: 1px solid rgba(110, 231, 183, 0.22);
        border-radius: 12px;
    }

    /* Collapsed sidebar: one visible hamburger toggle. */
    [data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        position: fixed !important;
        top: 0.75rem !important;
        left: 0.75rem !important;
        z-index: 999999 !important;
        background: #FFFFFF !important;
        border: 1px solid var(--border) !important;
        border-radius: 9px !important;
        box-shadow: 0 2px 8px rgba(18, 33, 59, 0.10);
    }

    [data-testid="collapsedControl"] button {
        min-width: 42px !important;
        min-height: 42px !important;
        width: 42px !important;
        height: 42px !important;
        border-radius: 9px !important;
    }

    [data-testid="collapsedControl"] button svg {
        display: none !important;
    }

    [data-testid="collapsedControl"] button::after {
        content: "☰";
        color: #12213B;
        font-size: 23px;
        line-height: 1;
        font-weight: 700;
    }

    /* Keep Streamlit's native expanded-sidebar collapse control intact. */
    section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button::after,
    section[data-testid="stSidebar"] button[kind="header"]::after,
    section[data-testid="stSidebar"] button[aria-label*="Collapse"]::after {
        content: none !important;
        display: none !important;
    }

    [data-testid="collapsedControl"]:hover {
        border-color: #2563EB !important;
        box-shadow: 0 3px 12px rgba(37, 99, 235, 0.16);
    }

    header[data-testid="stHeader"] {
        background: rgba(244, 247, 251, 0.94);
    }

    h1, h2, h3 {
        color: var(--ink) !important;
        letter-spacing: -0.025em;
    }

    h1 {
        font-size: clamp(1.8rem, 3vw, 2.45rem) !important;
        line-height: 1.2 !important;
        font-weight: 750 !important;
        margin-bottom: 0.35rem !important;
    }

    h2 {
        font-size: 1.55rem !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 1.18rem !important;
        font-weight: 650 !important;
    }

    .main p,
    .main label,
    .main [data-testid="stWidgetLabel"],
    .main [data-testid="stMarkdownContainer"],
    .main .stCaption {
        color: var(--muted);
    }

    .main [data-testid="stWidgetLabel"] p,
    .main [data-testid="stSlider"] label,
    .main [data-testid="stSlider"] [data-testid="stMarkdownContainer"] {
        color: #34445E !important;
        font-weight: 600;
    }

    .main [data-testid="stSlider"] {
        padding: 0.4rem 0 0.8rem;
    }

    div[data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 4px 14px rgba(24, 36, 58, 0.045);
        min-height: 112px;
    }

    div[data-testid="stMetricLabel"] {
        color: #64748B !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: var(--navy) !important;
        font-weight: 750 !important;
    }

    div[data-testid="stExpander"] {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 12px;
        overflow: hidden;
    }

    hr {
        border-color: var(--border);
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 9px;
        border: 1px solid #D5DFEB;
        font-weight: 650;
        transition: all 0.18s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: var(--blue);
        color: var(--blue);
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 9px;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem 0.9rem 2rem;
        }
        h1 {
            font-size: 1.7rem !important;
        }
        div[data-testid="stMetric"] {
            padding: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

    for col in ["actual", "predicted"]:
        lightgbm[col] = pd.to_numeric(lightgbm[col], errors="coerce")
    prophet["yhat"] = pd.to_numeric(prophet["yhat"], errors="coerce")

    for col in ["MAE", "RMSE", "WMAPE (%)"]:
        comparison[col] = pd.to_numeric(comparison[col], errors="coerce")

    lightgbm = lightgbm.dropna(subset=["date", "actual", "predicted"]).copy()
    prophet = prophet.dropna(subset=["ds", "yhat"]).copy()
    comparison = comparison.dropna(subset=["Model", "MAE", "RMSE", "WMAPE (%)"]).copy()

    if lightgbm.empty or prophet.empty or comparison.empty:
        raise ValueError("One or more forecast CSVs contain no usable rows.")

    return lightgbm, prophet, comparison


# --------------------------------------------------
# APP HEADER AND NAVIGATION
# --------------------------------------------------
st.title("📊 Retail Demand Forecasting & Inventory Optimization")
st.caption("DEMAND ANALYTICS  /  FORECASTING • MODEL EVALUATION • INVENTORY PLANNING")
st.divider()

st.sidebar.title("Retail Analytics")
st.sidebar.caption("DEMAND PLANNING WORKSPACE")
page = st.sidebar.radio(
    "Navigate",
    [
        "Dashboard",
        "Executive Report",
        "Data Quality & Monitoring",
        "Alerts & Recommendations",
        "Demand Forecasting",
        "Model Comparison",
        "Forecast Diagnostics",
        "Inventory Optimization",
        "What-if Analysis",
    ],
    key="retail_page_navigation",
)

try:
    lightgbm, prophet, comparison = load_data()
    st.sidebar.success("Forecast data loaded")

    best_model = comparison.loc[comparison["WMAPE (%)"].idxmin(), "Model"]
    best_wmape = float(comparison["WMAPE (%)"].min())

    # --------------------------------------------------
    # DATA QUALITY & MONITORING
    # --------------------------------------------------
    if page == "Data Quality & Monitoring":
        st.subheader("Data Quality & Monitoring")
        st.caption("Validate forecast inputs before using results for reporting or inventory planning.")

        file_specs = [
            ("LightGBM forecast", DATA_DIR / "lightgbm_forecast_FOODS_3_090_CA_3.csv", ["date", "actual", "predicted"]),
            ("Prophet forecast", DATA_DIR / "prophet_forecast_FOODS_3_090_CA_3.csv", ["ds", "yhat"]),
            ("Model comparison", DATA_DIR / "model_comparison.csv", ["Model", "MAE", "RMSE", "WMAPE (%)"]),
        ]
        quality_rows = []
        for display_name, file_path, required_columns in file_specs:
            if not file_path.exists():
                quality_rows.append({"Dataset": display_name, "Status": "MISSING", "Rows": 0,
                                     "Columns": 0, "Missing cells": "—", "Duplicate rows": "—",
                                     "Date coverage": "—", "Required columns": "Missing file"})
                continue
            try:
                raw_df = pd.read_csv(file_path)
                missing_cells = int(raw_df.isna().sum().sum())
                duplicate_rows = int(raw_df.duplicated().sum())
                missing_required = [col for col in required_columns if col not in raw_df.columns]
                date_coverage = "N/A"
                date_col = "date" if "date" in raw_df.columns else ("ds" if "ds" in raw_df.columns else None)
                if date_col:
                    dates = pd.to_datetime(raw_df[date_col], errors="coerce").dropna()
                    if not dates.empty:
                        date_coverage = f"{dates.min().date()} to {dates.max().date()}"
                status = "PASS" if not missing_required and missing_cells == 0 else "REVIEW"
                quality_rows.append({"Dataset": display_name, "Status": status, "Rows": len(raw_df),
                                     "Columns": len(raw_df.columns), "Missing cells": missing_cells,
                                     "Duplicate rows": duplicate_rows, "Date coverage": date_coverage,
                                     "Required columns": "All present" if not missing_required else "Missing: " + ", ".join(missing_required)})
            except Exception as exc:
                quality_rows.append({"Dataset": display_name, "Status": "ERROR", "Rows": "—",
                                     "Columns": "—", "Missing cells": "—", "Duplicate rows": "—",
                                     "Date coverage": "—", "Required columns": str(exc)})

        quality_df = pd.DataFrame(quality_rows)
        pass_count = int((quality_df["Status"] == "PASS").sum()) if not quality_df.empty else 0
        review_count = int((quality_df["Status"] != "PASS").sum()) if not quality_df.empty else 0
        q1, q2, q3 = st.columns(3)
        q1.metric("Datasets checked", len(quality_df))
        q2.metric("Passed", pass_count)
        q3.metric("Need review", review_count)
        st.markdown("### Dataset health summary")
        st.dataframe(quality_df, hide_index=True, width="stretch")
        st.download_button(
            "Download data quality report CSV",
            data=quality_df.to_csv(index=False).encode("utf-8"),
            file_name="retail_data_quality_report.csv",
            mime="text/csv",
        )

        st.markdown("### Forecast-specific checks")
        if not lightgbm.empty:
            duplicate_dates = int(lightgbm["date"].duplicated().sum())
            negative_actuals = int((lightgbm["actual"] < 0).sum())
            negative_predictions = int((lightgbm["predicted"] < 0).sum())
            checks = pd.DataFrame([
                {"Check": "Duplicate LightGBM dates", "Count": duplicate_dates, "Interpretation": "Review repeated dates if one row per day is expected."},
                {"Check": "Negative actual demand values", "Count": negative_actuals, "Interpretation": "Demand is usually non-negative; verify returns or adjustments."},
                {"Check": "Negative LightGBM predictions", "Count": negative_predictions, "Interpretation": "Forecasts may need a non-negative business constraint."},
            ])
            st.dataframe(checks, hide_index=True, width="stretch")
            if review_count == 0 and duplicate_dates == 0 and negative_actuals == 0 and negative_predictions == 0:
                st.success("No issues were detected by these basic checks. This does not guarantee the source data is error-free.")
            else:
                st.warning("Review the findings above. Some findings may be expected depending on the dataset's business rules.")
        else:
            st.warning("Forecast data is empty, so forecast-specific checks could not run.")

        with st.expander("What these checks mean"):
            st.markdown("""
            - **PASS** means the file exists, required columns are present, and the raw file has no missing cells.
            - Duplicate rows are reported separately; they do not automatically fail the dataset.
            - Negative predictions are flagged, not silently changed, so model behavior remains visible.
            - These are lightweight validation checks, not a full statistical or business-rule audit.
            """)

    # --------------------------------------------------
    # EXECUTIVE REPORT
    # --------------------------------------------------
    elif page == "Executive Report":
        st.subheader("Executive Report")
        st.caption("A concise, exportable summary for project reviews and demand-planning discussions.")

        report_data = lightgbm[["date", "actual", "predicted"]].copy().sort_values("date")
        report_min = report_data["date"].min().date()
        report_max = report_data["date"].max().date()
        report_range = st.date_input(
            "Report evaluation period",
            value=(report_min, report_max),
            min_value=report_min,
            max_value=report_max,
            key="executive_report_date_range",
        )
        if isinstance(report_range, (tuple, list)) and len(report_range) == 2:
            report_start, report_end = report_range
            report_data = report_data[report_data["date"].dt.date.between(report_start, report_end)].copy()

        if report_data.empty:
            st.warning("No evaluation records are available for the selected period.")
        else:
            report_data["error"] = report_data["predicted"] - report_data["actual"]
            report_data["absolute_error"] = report_data["error"].abs()
            demand_total = float(report_data["actual"].sum())
            demand_avg = float(report_data["actual"].mean())
            report_mae = float(report_data["absolute_error"].mean())
            report_rmse = float((report_data["error"].pow(2).mean()) ** 0.5)
            denom = float(report_data["actual"].abs().sum())
            report_wmape = float(report_data["absolute_error"].sum() / denom * 100) if denom else float("nan")
            report_bias = float(report_data["error"].mean())
            selected_days = int(report_data["date"].nunique())
            best_row = comparison.loc[comparison["WMAPE (%)"].idxmin()]
            best_name = str(best_row["Model"])
            best_error = float(best_row["WMAPE (%)"])

            st.markdown("### Performance at a glance")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Evaluation Days", f"{selected_days:,}")
            k2.metric("Actual Demand", f"{demand_total:,.0f} units")
            k3.metric("Average Daily Demand", f"{demand_avg:,.1f} units")
            k4.metric("LightGBM WMAPE", f"{report_wmape:.2f}%" if pd.notna(report_wmape) else "N/A")

            st.markdown("### Key findings")
            f1, f2 = st.columns(2)
            with f1:
                st.metric("Best Model in Comparison File", best_name)
                st.caption(f"Comparison-file WMAPE: {best_error:.2f}%")
            with f2:
                st.metric("LightGBM Forecast Bias", f"{report_bias:+.2f} units/day")
                if report_bias > 0.5:
                    st.caption("Tendency: over-forecasting in the selected evaluation period.")
                elif report_bias < -0.5:
                    st.caption("Tendency: under-forecasting in the selected evaluation period.")
                else:
                    st.caption("Tendency: average bias is close to zero.")

            st.markdown("### Model comparison")
            st.dataframe(comparison.sort_values("WMAPE (%)"), hide_index=True, width="stretch")
            st.markdown("### Actual demand vs LightGBM")
            report_chart = report_data[["date", "actual", "predicted"]].rename(
                columns={"actual": "Actual Demand", "predicted": "LightGBM Forecast"}
            ).set_index("date")
            st.line_chart(report_chart, x_label="Date", y_label="Units", width="stretch")

            st.markdown("### Planning recommendations")
            recommendations = []
            if report_wmape <= 15:
                recommendations.append("Forecast error is relatively low for this evaluation window; continue monitoring as new actuals arrive.")
            elif report_wmape <= 25:
                recommendations.append("Forecast error is moderate; review high-error dates and use safety stock for demand uncertainty.")
            else:
                recommendations.append("Forecast error is high; review outlier dates, demand shifts, and feature quality before relying on the forecast for replenishment.")
            if report_bias > 0.5:
                recommendations.append("Average bias is positive, so check for excess-stock risk and review the model's over-forecasting dates.")
            elif report_bias < -0.5:
                recommendations.append("Average bias is negative, so check for stockout risk and review the model's under-forecasting dates.")
            else:
                recommendations.append("Average bias is close to zero, but individual-day errors can still be large; keep monitoring absolute errors.")
            recommendations.append("Treat this report as historical holdout evaluation, not a guarantee of future performance. Inventory settings should reflect supplier lead time and business service-level targets.")
            for rec in recommendations:
                st.markdown(f"- {rec}")

            report_text = (
                "RETAIL DEMAND FORECASTING — EXECUTIVE REPORT\n"
                f"Product: FOODS_3_090 | Store: CA_3\n"
                f"Period: {report_data['date'].min().date()} to {report_data['date'].max().date()}\n"
                f"Evaluation days: {selected_days}\n"
                f"Actual demand: {demand_total:.2f} units\n"
                f"Average daily demand: {demand_avg:.2f} units\n"
                f"LightGBM MAE: {report_mae:.2f} units\n"
                f"LightGBM RMSE: {report_rmse:.2f} units\n"
                f"LightGBM WMAPE: {report_wmape:.2f}%\n"
                f"LightGBM forecast bias: {report_bias:+.2f} units/day\n"
                f"Best model in comparison file: {best_name} (WMAPE {best_error:.2f}%)\n\n"
                "RECOMMENDATIONS\n- " + "\n- ".join(recommendations) + "\n"
            )
            st.download_button(
                "Download Executive Report (.txt)",
                data=report_text.encode("utf-8"),
                file_name="retail_demand_executive_report.txt",
                mime="text/plain",
            )
            st.download_button(
                "Download Evaluation Data (.csv)",
                data=report_data.to_csv(index=False).encode("utf-8"),
                file_name="retail_demand_executive_evaluation.csv",
                mime="text/csv",
            )
            st.caption("Model-comparison scores come from the supplied comparison CSV; selected-period diagnostics are recalculated from the LightGBM holdout records.")

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------
    # --------------------------------------------------
    # ALERTS & RECOMMENDATIONS
    # --------------------------------------------------
    elif page == "Alerts & Recommendations":
        st.subheader("Alerts & Recommendations")
        st.caption(
            "Rule-based planning signals generated from the available historical holdout forecasts. "
            "These are decision-support prompts, not live alerts or guaranteed outcomes."
        )

        alert_data = lightgbm[["date", "actual", "predicted"]].copy().sort_values("date")
        alert_data["Error"] = alert_data["predicted"] - alert_data["actual"]
        alert_data["Absolute Error"] = alert_data["Error"].abs()
        total_actual = float(alert_data["actual"].abs().sum())
        alert_wmape = float(alert_data["Absolute Error"].sum() / total_actual * 100) if total_actual else float("nan")
        alert_mae = float(alert_data["Absolute Error"].mean())
        alert_bias = float(alert_data["Error"].mean())
        demand_mean = float(alert_data["actual"].mean())
        demand_std = float(alert_data["actual"].std(ddof=1)) if len(alert_data) > 1 else 0.0
        demand_cv = demand_std / demand_mean * 100 if demand_mean > 0 else float("nan")
        over_days = int((alert_data["Error"] > 0).sum())
        under_days = int((alert_data["Error"] < 0).sum())
        large_error_threshold = max(10.0, alert_mae * 1.5)
        large_error_days = int((alert_data["Absolute Error"] > large_error_threshold).sum())

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Holdout WMAPE", f"{alert_wmape:.2f}%" if pd.notna(alert_wmape) else "N/A")
        m2.metric("Average absolute error", f"{alert_mae:.2f} units")
        m3.metric("Forecast bias", f"{alert_bias:+.2f} units")
        m4.metric("Demand variability (CV)", f"{demand_cv:.1f}%" if pd.notna(demand_cv) else "N/A")

        alerts = []
        recommendations = []
        if pd.notna(alert_wmape) and alert_wmape > 30:
            alerts.append({"Priority": "High", "Signal": "Forecast error is high", "Evidence": f"WMAPE is {alert_wmape:.2f}%", "Recommended action": "Review outlier dates, promotions, holidays, and data completeness before relying on the forecast."})
            recommendations.append("Investigate periods with the largest misses and add relevant calendar or promotion features where reliable data exists.")
        elif pd.notna(alert_wmape) and alert_wmape > 20:
            alerts.append({"Priority": "Medium", "Signal": "Forecast accuracy needs monitoring", "Evidence": f"WMAPE is {alert_wmape:.2f}%", "Recommended action": "Compare errors by week and continue tracking accuracy on later holdout periods."})
        else:
            alerts.append({"Priority": "Low", "Signal": "No high-error threshold triggered", "Evidence": f"WMAPE is {alert_wmape:.2f}%" if pd.notna(alert_wmape) else "WMAPE unavailable", "Recommended action": "Continue evaluating on new periods; current holdout performance is not a guarantee."})

        if alert_bias > 0.5:
            alerts.append({"Priority": "Medium", "Signal": "Over-forecasting tendency", "Evidence": f"Average bias is +{alert_bias:.2f} units; {over_days} days over-forecasted", "Recommended action": "Check whether demand has declined or whether recent high-demand days are skewing predictions."})
            recommendations.append("If over-forecasting persists in future periods, review replenishment quantities to reduce excess-stock risk.")
        elif alert_bias < -0.5:
            alerts.append({"Priority": "High", "Signal": "Under-forecasting tendency", "Evidence": f"Average bias is {alert_bias:.2f} units; {under_days} days under-forecasted", "Recommended action": "Review stockout history, promotions, and demand increases that may not be captured by the model."})
            recommendations.append("If under-forecasting persists, consider a cautious temporary buffer while validating the cause.")
        else:
            alerts.append({"Priority": "Low", "Signal": "Average bias is near zero", "Evidence": f"Average bias is {alert_bias:+.2f} units", "Recommended action": "Still inspect individual high-error days; positive and negative errors can cancel out in the average."})

        if pd.notna(demand_cv) and demand_cv >= 50:
            alerts.append({"Priority": "Medium", "Signal": "Demand is variable", "Evidence": f"Demand coefficient of variation is {demand_cv:.1f}%", "Recommended action": "Use a demand-aware safety-stock policy and review variability regularly."})
            recommendations.append("Avoid setting safety stock from average demand alone when demand varies substantially.")
        if large_error_days:
            alerts.append({"Priority": "Medium", "Signal": "Large daily forecast misses found", "Evidence": f"{large_error_days} days exceed {large_error_threshold:.1f} units absolute error", "Recommended action": "Review the worst-error dates for special events, data issues, or unusual demand patterns."})

        alert_df = pd.DataFrame(alerts)
        st.markdown("### Detected signals")
        st.dataframe(alert_df, hide_index=True, width="stretch")

        st.markdown("### Recommended next actions")
        for idx, recommendation in enumerate(dict.fromkeys(recommendations), start=1):
            st.markdown(f"{idx}. {recommendation}")
        if not recommendations:
            st.info("No additional action was triggered by the current rules. Continue routine monitoring.")

        st.markdown("### Forecast error pattern")
        error_view = alert_data[["date", "actual", "predicted", "Error", "Absolute Error"]].copy()
        error_view = error_view.rename(columns={"actual": "Actual demand", "predicted": "Forecast"}).set_index("date")
        st.line_chart(error_view[["Actual demand", "Forecast"]], x_label="Date", y_label="Units", width="stretch")
        st.bar_chart(alert_data.set_index("date")[["Error"]], x_label="Date", y_label="Forecast − actual (units)", width="stretch")

        st.download_button(
            "Download alerts and recommendations CSV",
            data=alert_df.to_csv(index=False).encode("utf-8"),
            file_name="retail_forecast_alerts_recommendations.csv",
            mime="text/csv",
        )
        st.caption(
            "Thresholds are configurable planning heuristics. Signals are calculated from the supplied historical holdout data; "
            "they are not real-time production monitoring and should be reviewed alongside business context."
        )

    elif page == "Dashboard":
        st.subheader("Retail Demand Overview")
        st.caption("A quick view of the selected product-store evaluation period.")

        total_demand = float(lightgbm["actual"].sum())
        avg_demand = float(lightgbm["actual"].mean())
        period_days = int(lightgbm["date"].nunique())

        c1, c2 = st.columns(2)
        with c1:
            st.metric("Test Period Demand", f"{total_demand:,.0f}")
        with c2:
            st.metric("Average Daily Demand", f"{avg_demand:,.1f}")

        c3, c4 = st.columns(2)
        with c3:
            st.metric("Best Model", str(best_model))
        with c4:
            st.metric("Best WMAPE", f"{best_wmape:.2f}%")

        st.subheader("Actual vs LightGBM")
        trend = (
            lightgbm[["date", "actual", "predicted"]]
            .copy()
            .sort_values("date")
            .rename(
                columns={
                    "actual": "Actual Demand",
                    "predicted": "LightGBM Forecast",
                }
            )
            .set_index("date")
        )
        st.line_chart(
            trend,
            x_label="Date",
            y_label="Units Sold",
            width="stretch",
        )

        st.subheader("Model Performance")
        st.dataframe(comparison, hide_index=True, width="stretch")

        with st.expander("View latest forecast rows"):
            st.dataframe(
                lightgbm.sort_values("date", ascending=False).head(10),
                hide_index=True,
                width="stretch",
            )

        st.caption(
            f"Product: FOODS_3_090 | Store: CA_3 | Evaluation period: {period_days} days. "
            "These are historical holdout results, not live future predictions."
        )

    # --------------------------------------------------
    # DEMAND FORECASTING
    # --------------------------------------------------
    elif page == "Demand Forecasting":
        st.subheader("Demand Forecasting")
        st.caption(
            "Explore actual demand and compare Prophet and LightGBM predictions "
            "across the historical evaluation period."
        )

        lgb_plot = (
            lightgbm[["date", "actual", "predicted"]]
            .copy()
            .sort_values("date")
        )
        prophet_plot = prophet[["ds", "yhat"]].copy().rename(
            columns={"ds": "date", "yhat": "Prophet Forecast"}
        )

        chart_data = (
            lgb_plot.merge(prophet_plot, on="date", how="left")
            .rename(
                columns={
                    "actual": "Actual Demand",
                    "predicted": "LightGBM Forecast",
                }
            )
            .sort_values("date")
        )

        min_date = chart_data["date"].min().date()
        max_date = chart_data["date"].max().date()
        date_range = st.date_input(
            "Evaluation date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="forecast_date_range",
        )

        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range
            visible = chart_data[
                (chart_data["date"].dt.date >= start_date)
                & (chart_data["date"].dt.date <= end_date)
            ].copy()
        else:
            visible = chart_data.copy()

        if visible.empty:
            st.warning("No data is available for this date range.")
        else:
            total_actual = float(visible["Actual Demand"].sum())
            average_actual = float(visible["Actual Demand"].mean())
            days = int(visible["date"].nunique())

            k1, k2, k3 = st.columns(3)
            k1.metric("Actual Units Sold", f"{total_actual:,.0f}")
            k2.metric("Average Daily Demand", f"{average_actual:,.1f}")
            k3.metric("Days Selected", str(days))

            st.subheader("Actual vs Predicted Demand")
            st.line_chart(
                visible.set_index("date")[
                    [
                        "Actual Demand",
                        "Prophet Forecast",
                        "LightGBM Forecast",
                    ]
                ],
                x_label="Date",
                y_label="Units Sold",
                width="stretch",
            )

            st.subheader("Forecast Records")
            st.dataframe(visible, hide_index=True, width="stretch")
            st.download_button(
                "Download displayed forecast CSV",
                data=visible.to_csv(index=False).encode("utf-8"),
                file_name="retail_forecast_displayed.csv",
                mime="text/csv",
            )

        st.caption(
            "Product: FOODS_3_090 | Store: CA_3 | "
            "This is a historical holdout evaluation, not a live future forecast."
        )

    # --------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------
    elif page == "Model Comparison":
        st.subheader("Model Performance Comparison")
        st.caption("Both models are evaluated on the same 30-day historical holdout period.")

        st.dataframe(comparison, hide_index=True, width="stretch")

        selected_metric = st.selectbox(
            "Metric to compare",
            ["WMAPE (%)", "MAE", "RMSE"],
            index=0,
            key="comparison_metric",
        )
        metric_help = {
            "WMAPE (%)": "Weighted absolute percentage error; lower is better.",
            "MAE": "Mean absolute error in units; lower is better.",
            "RMSE": "Root mean squared error in units; lower is better.",
        }
        st.caption(metric_help[selected_metric])
        st.bar_chart(
            comparison[["Model", selected_metric]].set_index("Model"),
            y=selected_metric,
            x_label="Model",
            y_label=selected_metric,
            width="stretch",
        )

        st.subheader("Model Scorecards")
        model_options = comparison["Model"].astype(str).tolist()
        default_model = str(best_model) if str(best_model) in model_options else model_options[0]
        selected_model = st.selectbox(
            "Choose a model to inspect",
            model_options,
            index=model_options.index(default_model),
            key="comparison_model_detail",
        )
        selected_rows = comparison[comparison["Model"].astype(str) == selected_model]
        if not selected_rows.empty:
            row = selected_rows.iloc[0]
            m1, m2, m3 = st.columns(3)
            m1.metric("Mean Absolute Error (MAE)", f"{float(row['MAE']):.2f}")
            m2.metric("Root Mean Squared Error (RMSE)", f"{float(row['RMSE']):.2f}")
            m3.metric(
                "Weighted Absolute Percentage Error",
                f"{float(row['WMAPE (%)']):.2f}%",
            )

        st.success(
            f"{best_model} has the lowest WMAPE ({best_wmape:.2f}%) on this holdout period."
        )
        st.caption(
            "Lower error indicates better performance on this particular holdout period; "
            "it does not guarantee performance on future data."
        )

    # --------------------------------------------------
    # FORECAST DIAGNOSTICS
    # --------------------------------------------------
    elif page == "Forecast Diagnostics":
        st.subheader("Forecast Diagnostics")
        st.caption(
            "Inspect where the LightGBM forecast over- or under-predicts demand. "
            "Diagnostics are based on the historical holdout data."
        )

        diagnostics = lightgbm[["date", "actual", "predicted"]].copy().sort_values("date")
        diagnostics["Error"] = diagnostics["predicted"] - diagnostics["actual"]
        diagnostics["Absolute Error"] = diagnostics["Error"].abs()
        diagnostics["Absolute Percentage Error (%)"] = (
            diagnostics["Absolute Error"] / diagnostics["actual"].abs().replace(0, pd.NA) * 100
        )

        d_min = diagnostics["date"].min().date()
        d_max = diagnostics["date"].max().date()
        diag_range = st.date_input(
            "Diagnostics date range",
            value=(d_min, d_max),
            min_value=d_min,
            max_value=d_max,
            key="diagnostics_date_range",
        )
        if isinstance(diag_range, (tuple, list)) and len(diag_range) == 2:
            d_start, d_end = diag_range
            diagnostics = diagnostics[
                diagnostics["date"].dt.date.between(d_start, d_end)
            ].copy()

        if diagnostics.empty:
            st.warning("No diagnostic records are available for this date range.")
        else:
            actual_values = diagnostics["actual"]
            predicted_values = diagnostics["predicted"]
            errors = diagnostics["Error"]
            mae_value = float(diagnostics["Absolute Error"].mean())
            rmse_value = float((errors.pow(2).mean()) ** 0.5)
            denominator = float(actual_values.abs().sum())
            wmape_value = (
                float(diagnostics["Absolute Error"].sum() / denominator * 100)
                if denominator > 0 else float("nan")
            )
            bias_value = float(errors.mean())
            within_10 = float((diagnostics["Absolute Error"] <= 10).mean() * 100)

            a, b, c, d = st.columns(4)
            a.metric("MAE", f"{mae_value:.2f} units")
            b.metric("RMSE", f"{rmse_value:.2f} units")
            c.metric("WMAPE", f"{wmape_value:.2f}%" if pd.notna(wmape_value) else "N/A")
            d.metric("Forecast Bias", f"{bias_value:+.2f} units")

            if bias_value > 0.5:
                st.warning("The model tends to over-forecast in this selected period.")
            elif bias_value < -0.5:
                st.warning("The model tends to under-forecast in this selected period.")
            else:
                st.success("Average forecast bias is close to zero in this selected period.")

            st.subheader("Actual Demand vs Forecast")
            trend = diagnostics[["date", "actual", "predicted"]].rename(
                columns={"actual": "Actual Demand", "predicted": "LightGBM Forecast"}
            ).set_index("date")
            st.line_chart(trend, x_label="Date", y_label="Units", width="stretch")

            st.subheader("Forecast Error Over Time")
            st.caption("Error = forecast − actual. Positive values mean over-forecasting; negative values mean under-forecasting.")
            error_trend = diagnostics[["date", "Error"]].set_index("date")
            st.line_chart(error_trend, x_label="Date", y_label="Error (units)", width="stretch")

            left, right = st.columns(2)
            with left:
                st.metric("Days Within 10 Units Error", f"{within_10:.1f}%")
            with right:
                st.metric("Largest Absolute Error", f"{diagnostics['Absolute Error'].max():.2f} units")

            st.subheader("Largest Forecast Misses")
            worst = diagnostics.sort_values("Absolute Error", ascending=False).head(10).copy()
            worst["date"] = worst["date"].dt.strftime("%Y-%m-%d")
            st.dataframe(worst, hide_index=True, width="stretch")
            st.download_button(
                "Download diagnostics CSV",
                data=diagnostics.to_csv(index=False).encode("utf-8"),
                file_name="lightgbm_forecast_diagnostics.csv",
                mime="text/csv",
            )

            with st.expander("How to interpret these metrics"):
                st.markdown(
                    "- **MAE:** average absolute forecast error in units; lower is better.\n"
                    "- **RMSE:** penalizes large misses more heavily; lower is better.\n"
                    "- **WMAPE:** total absolute error divided by total actual demand; lower is better.\n"
                    "- **Forecast bias:** average forecast minus actual. Positive means over-forecasting; negative means under-forecasting.\n"
                    "- **Days within 10 units:** percentage of selected days where absolute error is at most 10 units."
                )
            st.caption("This diagnostic view evaluates the provided historical holdout file; it does not guarantee future accuracy.")

    # --------------------------------------------------
    # INVENTORY OPTIMIZATION
    # --------------------------------------------------
    elif page == "Inventory Optimization":
        st.subheader("Inventory Optimization")
        st.caption(
            "Plan replenishment using historical demand, supplier lead time, "
            "and your target service level."
        )

        st.markdown("### Inventory Planning Inputs")
        c1, c2, c3 = st.columns(3)

        with c1:
            lead_time = st.number_input(
                "Supplier Lead Time (days)", min_value=1, max_value=90,
                value=5, step=1,
            )
        with c2:
            current_stock = st.number_input(
                "Current Inventory (units)", min_value=0, value=500, step=10,
            )
        with c3:
            service_level = st.selectbox(
                "Target Service Level", ["90%", "95%", "99%"], index=1,
            )

        # Preserve the existing inventory calculations.
        daily = lightgbm["actual"].astype(float)
        avg = float(daily.mean())
        std = float(daily.std(ddof=1)) if len(daily) > 1 else 0.0
        z = {"90%": 1.282, "95%": 1.645, "99%": 2.326}[service_level]

        safety = z * std * (lead_time ** 0.5)
        lead_time_demand = avg * lead_time
        reorder = lead_time_demand + safety
        recommended = avg * 30 + safety
        additional = max(0.0, recommended - current_stock)

        st.divider()
        st.markdown("### Recommended Inventory Metrics")
        k1, k2, k3 = st.columns(3)
        with k1:
            st.metric("Average Daily Demand", f"{avg:.1f} units")
        with k2:
            st.metric("Safety Stock", f"{safety:.0f} units")
        with k3:
            st.metric("Reorder Point", f"{reorder:.0f} units")

        k4, k5 = st.columns(2)
        with k4:
            st.metric("30-Day Stock Requirement", f"{recommended:.0f} units")
        with k5:
            st.metric("Additional Stock Needed", f"{additional:.0f} units")

        st.divider()
        st.markdown("### Current Stock Assessment")
        if current_stock <= reorder:
            st.error(
                "Replenishment recommended: current stock is at or below "
                "the calculated reorder point."
            )
            status_text = "Replenishment needed"
        elif current_stock < recommended:
            st.warning(
                "Stock is above the reorder point but below the calculated "
                "30-day stock requirement."
            )
            status_text = "Below 30-day target"
        else:
            st.success(
                "Current stock meets or exceeds the calculated "
                "30-day stock requirement."
            )
            status_text = "30-day target met"

        coverage = (
            min(100.0, current_stock / recommended * 100)
            if recommended > 0 else 100.0
        )
        st.markdown(f"**Stock target coverage: {coverage:.1f}%**")
        st.progress(coverage / 100)

        a, b = st.columns(2)
        with a:
            st.metric("Current Inventory", f"{current_stock:,.0f} units")
        with b:
            st.metric("Inventory Status", status_text)

        st.caption(
            "Coverage compares current stock with the calculated 30-day stock "
            "requirement. It is not a guarantee of product availability."
        )

        with st.expander("Calculation details and assumptions"):
            st.markdown(
                f"""
                - **Average daily demand:** {avg:.2f} units
                - **Lead-time demand:** Average daily demand × {lead_time} days
                  = {lead_time_demand:.2f} units
                - **Safety stock:** Z-score × demand standard deviation × √lead time
                  = {safety:.2f} units
                - **Reorder point:** Lead-time demand + safety stock
                  = {reorder:.2f} units
                - **30-day stock requirement:** Average daily demand × 30 + safety stock
                  = {recommended:.2f} units

                **Data limitation:** Calculations use the 30-day historical evaluation
                observations currently loaded by the app, rather than the complete
                historical demand series. Validate using longer demand history before
                operational use.
                """
            )

    # --------------------------------------------------
    # WHAT-IF ANALYSIS
    # --------------------------------------------------
    elif page == "What-if Analysis":
        st.subheader("What-if Scenario Simulator")
        st.caption(
            "Adjust scenario assumptions and immediately compare demand and inventory "
            "requirements with the baseline. These controls do not retrain either model."
        )

        st.markdown("### 1. Configure your scenario")
        left, right = st.columns([1, 1])
        with left:
            demand_change = st.slider(
                "Other Demand Change (%)", min_value=-20, max_value=20,
                value=0, step=5,
                help="Represents a hypothetical change from factors other than price.",
            )
            price_change = st.slider(
                "Price Change (%)", min_value=-10, max_value=10,
                value=0, step=5,
                help="A scenario input, not a price change observed in the dataset.",
            )
        with right:
            scenario_lead_time = st.slider(
                "Supplier Lead Time (days)", min_value=1, max_value=30, value=5,
            )
            elasticity = st.select_slider(
                "Assumed Price Elasticity",
                options=[-2.0, -1.75, -1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0.0],
                value=-1.0,
                help="Assumed scenario parameter only; it is not estimated or validated from sales data.",
            )

        daily = lightgbm["actual"].astype(float)
        base_daily = float(daily.mean())
        base_std = float(daily.std(ddof=1)) if len(daily) > 1 else 0.0

        # Constant-elasticity scenario. Forecasting models are not retrained.
        price_ratio = 1 + price_change / 100
        price_factor = price_ratio ** elasticity
        other_factor = 1 + demand_change / 100
        scenario_daily = max(0.0, base_daily * price_factor * other_factor)
        scenario_std = max(0.0, base_std * price_factor * other_factor)

        z = 1.645  # Approximate 95% service level.
        scenario_safety = z * scenario_std * (scenario_lead_time ** 0.5)
        scenario_lead_demand = scenario_daily * scenario_lead_time
        scenario_reorder = scenario_lead_demand + scenario_safety
        scenario_30_day = scenario_daily * 30 + scenario_safety

        # Baseline uses the same lead time and service-level assumption.
        baseline_safety = z * base_std * (scenario_lead_time ** 0.5)
        baseline_lead_demand = base_daily * scenario_lead_time
        baseline_reorder = baseline_lead_demand + baseline_safety
        baseline_30_day = base_daily * 30 + baseline_safety

        demand_delta_pct = ((scenario_daily / base_daily) - 1) * 100 if base_daily else 0.0
        price_only_pct = (price_factor - 1) * 100

        st.caption(
            "Product: FOODS_3_090  |  Store: CA_3  |  "
            "Baseline uses the 30-day historical evaluation period."
        )
        st.divider()
        st.markdown("### 2. Scenario impact")

        k1, k2, k3 = st.columns(3)
        k1.metric(
            "Scenario Daily Demand", f"{scenario_daily:.1f} units",
            delta=f"{scenario_daily - base_daily:+.1f} units/day vs baseline",
        )
        k2.metric(
            "Scenario Reorder Point", f"{scenario_reorder:.0f} units",
            delta=f"{scenario_reorder - baseline_reorder:+.0f} units vs baseline",
        )
        k3.metric(
            "30-Day Stock Requirement", f"{scenario_30_day:.0f} units",
            delta=f"{scenario_30_day - baseline_30_day:+.0f} units vs baseline",
        )

        p1, p2 = st.columns(2)
        p1.metric("Demand Change vs Baseline", f"{demand_delta_pct:+.1f}%")
        p2.metric("Price Effect Under Assumption", f"{price_only_pct:+.1f}%")

        st.markdown("### 3. Baseline vs scenario")
        scenario_comparison = pd.DataFrame(
            [
                {
                    "Metric": "Average daily demand (units)",
                    "Baseline": round(base_daily, 2),
                    "Scenario": round(scenario_daily, 2),
                    "Change": round(scenario_daily - base_daily, 2),
                },
                {
                    "Metric": "Lead-time demand (units)",
                    "Baseline": round(baseline_lead_demand, 2),
                    "Scenario": round(scenario_lead_demand, 2),
                    "Change": round(scenario_lead_demand - baseline_lead_demand, 2),
                },
                {
                    "Metric": "Safety stock (units)",
                    "Baseline": round(baseline_safety, 2),
                    "Scenario": round(scenario_safety, 2),
                    "Change": round(scenario_safety - baseline_safety, 2),
                },
                {
                    "Metric": "Reorder point (units)",
                    "Baseline": round(baseline_reorder, 2),
                    "Scenario": round(scenario_reorder, 2),
                    "Change": round(scenario_reorder - baseline_reorder, 2),
                },
                {
                    "Metric": "30-day stock requirement (units)",
                    "Baseline": round(baseline_30_day, 2),
                    "Scenario": round(scenario_30_day, 2),
                    "Change": round(scenario_30_day - baseline_30_day, 2),
                },
            ]
        )
        st.dataframe(scenario_comparison, hide_index=True, width="stretch")

        chart_data = pd.DataFrame(
            {
                "Baseline": [base_daily, baseline_reorder, baseline_30_day],
                "Scenario": [scenario_daily, scenario_reorder, scenario_30_day],
            },
            index=["Daily demand", "Reorder point", "30-day stock"],
        )
        st.markdown("### Visual comparison")
        st.bar_chart(
            chart_data,
            x_label="Metric",
            y_label="Units",
            width="stretch",
        )

        st.download_button(
            "Download scenario comparison CSV",
            data=scenario_comparison.to_csv(index=False).encode("utf-8"),
            file_name="retail_what_if_scenario.csv",
            mime="text/csv",
        )

        st.info(
            "Interpretation note: price elasticity is user-assumed, not a measured causal effect. "
            "The exploratory historical price regression was unstable and is not used here. "
            "This scenario is for planning exploration, not a validated future-demand forecast."
        )
        with st.expander("Scenario assumptions and formulas"):
            st.markdown(
                """
                - **Price demand factor:** (1 + price change) raised to assumed price elasticity.
                - **Scenario demand:** Baseline average demand × price factor × other demand factor.
                - **Safety stock:** 1.645 × adjusted demand standard deviation × √lead time.
                - **Reorder point:** Lead-time demand + safety stock.
                - **30-day stock requirement:** Scenario daily demand × 30 + safety stock.
                - The baseline and scenario use the same supplier lead time and approximately 95% service level.
                - Price changes do not retrain Prophet or LightGBM.
                """
            )

except FileNotFoundError as e:
    st.error(f"Required CSV file not found: {e}")
    st.info("Check that the forecast and comparison CSV files exist inside DATA/PROCESSED.")
except (KeyError, ValueError, IndexError) as e:
    st.error(f"Could not load or interpret the forecast data: {e}")
    st.info("Check the column names and model names in the Week 3 CSV files.")
