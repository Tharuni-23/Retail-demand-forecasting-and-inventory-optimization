# 🚀 Week 4 — Dashboard & Inventory Optimization

Week 4 focuses on transforming the forecasting results from Week 3 into an interactive **Streamlit dashboard** and implementing **inventory optimization and what-if analysis**.

---

## 🏗️ Week 4 Architecture

```text
                    WEEK 3 OUTPUTS
                         │
                         ▼
              ┌──────────────────────┐
              │  Forecast Results    │
              │                      │
              │  Prophet Forecast    │
              │  LightGBM Forecast   │
              │  Model Comparison    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    STREAMLIT APP     │
              │       app.py         │
              └──────────┬───────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌────────────┐ ┌─────────────┐ ┌──────────────┐
   │    KPI     │ │  Forecast   │ │    Model     │
   │ Dashboard  │ │ Visualization│ │  Comparison │
   └────────────┘ └─────────────┘ └──────────────┘
          │              │              │
          └──────────────┼──────────────┘
                         ▼
              ┌──────────────────────┐
              │ Inventory Optimization│
              └──────────┬───────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   ┌────────────┐ ┌─────────────┐ ┌──────────────┐
   │   Safety   │ │   Reorder   │ │    Stock     │
   │   Stock    │ │    Point    │ │ Requirement  │
   └────────────┘ └─────────────┘ └──────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    What-If Analysis  │
              │                      │
              │  Demand Change       │
              │  Price Change        │
              │  Lead Time Change    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Business Insights   │
              │ & Recommendations    │
              └──────────────────────┘
