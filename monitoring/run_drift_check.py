import os
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

def check_data_drift():
    reference_path = os.path.join("data", "housing_data.csv")
    production_path = os.path.join("models", "prediction_log.csv")
    
    if not os.path.exists(production_path):
        print("❌ No production data logged yet. Run predictions first.")
        return

    # Load baseline training data and live logged data
    reference_df = pd.read_csv(reference_path)[["sqft", "bedrooms"]]
    production_df = pd.read_csv(production_path)

    # Run Evidently Data Drift analysis
    drift_report = Report(metrics=[DataDriftPreset()])
    drift_report.run(reference_data=reference_df, production_data=production_df)
    
    # Save results as a clean dashboard file
    report_html_path = os.path.join("models", "drift_report.html")
    drift_report.save_html(report_html_path)
    print(f"📊 Data drift evaluation completed. Report saved to {report_html_path}")

if __name__ == "__main__":
    check_data_drift()
