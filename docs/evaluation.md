# Evaluation Framework & Business Metrics

## Measured Financial Metrics (Batch Analysis)
RecoveryOS evaluates performance across a batch of 1,500 synthetic payment failure records generated with realistic Razorpay ground-truth characteristics.

- **Total Revenue at Risk:** Sum of amounts across all failed payments in the batch.
- **Total Revenue Recovered:** Sum of amounts successfully recovered via policy-approved interventions.
- **Batch Recovery Rate (%):** `(Total Revenue Recovered / Total Revenue at Risk) * 100`
- **Escalation & Stop Efficiency:** Percentage of cases safely halted or escalated to prevent unnecessary gateway friction and fee waste.

## ML Performance Metrics
The ML risk model (`RandomForestClassifier`) is evaluated on an 80/20 train-test split using the following metrics:
- **ROC-AUC Score:** Evaluates probability ranking quality.
- **Precision:** Measures accuracy of positive recovery predictions.
- **Recall:** Measures coverage of actual recoverable payments.
- **F1-Score:** Harmonic mean of precision and recall.
- **Confusion Matrix:** Measures false-positive and false-negative tradeoffs.