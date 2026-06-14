# TechStack Signals Pipeline: Spark and AI Risk Framework

I built this project to develop an end-to-end data pipeline focused on corporate credit risk analysis. The core idea was to apply the Medallion Architecture (Bronze, Silver, and Gold) to structure the data workflow. I used Apache Spark (PySpark) to clean and aggregate the raw data, saved the final output in the optimized Parquet format, and connected an AI Agent to automatically validate financial metrics, generating a ready-to-use JSON report.

---

## Pipeline Architecture

I divided the data flow into clear steps to ensure clean organization and solid processing performance:

1. **Bronze Layer:** The starting point of the project, where I ingest the original raw file (`company_data.csv`) containing historical financial data and market signals.
2. **Silver Layer:** This is where I handled the heavy cleaning with PySpark. I stripped trailing spaces from the original column headers, cast proper data types, and filtered only the essential metrics needed for the analysis, such as ROA and net income ratios.
3. **Gold Layer:** Once the data was clean, I performed statistical aggregations by grouping companies based on their bankruptcy status. Instead of saving this to a standard CSV, I exported the results into the `gold_market_intelligence_summary` directory using the Parquet format, which is much faster to read and highly compressed.
4. **AI Layer:** I developed a validation script that acts as an automated audit. It reads the Gold layer Parquet files, applies specific financial business rules, and outputs a consolidated risk report.

---

## Tech Stack Used

* **Language:** Python (versions 3.11 / 3.14)
* **Big Data Processing:** Apache Spark 3.5.1 (PySpark)
* **Storage and Performance:** PyArrow and Parquet
* **Data Manipulation:** Pandas
* **AI Framework:** LangChain (Integrated architecture ready for LLM model calls)

---

## Final Output Example (JSON Report)

After execution, this is the structured report format generated to analyze the financial health of the target segments:

```json
[
    {
        "segment": "Bankrupt",
        "analyzed_metrics": {
            "avg_roa": 0.4185,
            "avg_net_income_ratio": 0.7381
        },
        "ai_insight": "CRITICAL: Bankrupt companies show a concerning average ROA of 0.4185.",
        "qa_status": "REJECTED - High Credit Risk"
    },
    {
        "segment": "Solvent",
        "analyzed_metrics": {
            "avg_roa": 0.5081,
            "avg_net_income_ratio": 0.8101
        },
        "ai_insight": "NORMAL: Metrics for Solvent companies are operating within stable statistical boundaries.",
        "qa_status": "APPROVED - Stability Pattern Mapped"
    }
]