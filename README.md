# ELT Project - Brasileirão 2025 🏆⚽

This project aims to build a complete ELT (Extract, Load, Transform) pipeline to collect, organize, and make available the match data for each **round of the Brazilian Football Championship - Série A (2025)**.

The goal is to go from raw data extraction to structured storage in an AWS S3 bucket using **Apache Airflow**. The final output will serve as the foundation for future dashboards and data visualizations.

---

## 📌 Goals

- Build a full data pipeline from scratch using Airflow.
- Collect match data for each **round** of Brasileirão 2025.
- Store the data as `.csv` files, organized by week, in **Amazon S3**.
- Set up a solid base for later analytics and visualizations.
- Automate the entire workflow with **Airflow DAGs**.

---

## 🛠️ Technologies Used

- **Apache Airflow**: Workflow orchestration tool to schedule and manage ELT tasks.
- **Python**: Main language for scripts (ETL logic).
- **Amazon S3**: Cloud storage for weekly match data.
- **Pandas**: Data manipulation before uploading.
- *(Optional)*: Future visualizations using Power BI, Superset, or Dash.

---

## 📂 Project Structure

```bash
.
├── dags/
│   ├── brasileirao_etl.py           # Main Airflow DAG
│   └── etl_utils.py                 # Utility functions (extraction, S3 upload, etc.)
├── data/
│   └── (optional temporary storage)                # Project dependencies
└── README.md                        
