"""
Credit Worthiness Data Generator

Generates realistic synthetic data with meaningful patterns:
- High-risk indicators (gambling, missed payments) → higher default probability
- Good financial health (savings, stable income) → lower default probability
- Realistic Nigerian context (states, salary ranges, etc.)
"""

import json
import random
import numpy as np

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Nigerian states
STATES = [
    "Lagos", "Kano", "Rivers", "Kaduna", "Oyo", "Anambra", "Delta",
    "Enugu", "Abuja", "Ogun", "Imo", "Edo", "Kwara", "Osun", "Katsina",
    "Borno", "Akwa Ibom", "Bauchi", "Plateau", "Cross River"
]

EMPLOYMENT_STATUS = ["Employed", "Self-employed", "Unemployed"]
GENDER = ["Male", "Female"]
REPAYMENT_STATUS = ["On-time", "Late", "N/A"]


def generate_realistic_record(record_id):
    """
    Generate a single record with realistic correlations.

    Key patterns:
    - Unemployed → lower income, higher default risk
    - High gambling → higher default risk
    - Missed payments → higher default risk
    - Low savings (balance/income ratio) → higher default risk
    - High debt burden → higher default risk
    """

    # Step 1: Determine base risk profile (this drives everything)
    # 0 = Low risk, 1 = Medium risk, 2 = High risk
    base_risk = random.choices([0, 1, 2], weights=[0.55, 0.30, 0.15])[0]

    # Step 2: Generate employment (correlated with risk)
    if base_risk == 0:  # Low risk
        employment_status = random.choices(EMPLOYMENT_STATUS, weights=[0.70, 0.28, 0.02])[0]
    elif base_risk == 1:  # Medium risk
        employment_status = random.choices(EMPLOYMENT_STATUS, weights=[0.50, 0.35, 0.15])[0]
    else:  # High risk
        employment_status = random.choices(EMPLOYMENT_STATUS, weights=[0.25, 0.35, 0.40])[0]

    # Step 3: Generate income based on employment
    if employment_status == "Employed":
        total_monthly_inflow = int(np.random.normal(350000, 150000))
        total_monthly_inflow = max(80000, min(1500000, total_monthly_inflow))
        salary_payment_detected = random.choices(["Yes", "No"], weights=[0.95, 0.05])[0]
    elif employment_status == "Self-employed":
        total_monthly_inflow = int(np.random.normal(280000, 180000))
        total_monthly_inflow = max(50000, min(2000000, total_monthly_inflow))
        salary_payment_detected = random.choices(["Yes", "No"], weights=[0.15, 0.85])[0]
    else:  # Unemployed
        total_monthly_inflow = int(np.random.normal(60000, 30000))
        total_monthly_inflow = max(10000, min(150000, total_monthly_inflow))
        salary_payment_detected = "No"

    # Step 4: Generate spending based on income and risk
    if base_risk == 0:
        spending_ratio = np.random.uniform(0.50, 0.75)  # Saves 25-50%
    elif base_risk == 1:
        spending_ratio = np.random.uniform(0.70, 0.90)  # Saves 10-30%
    else:
        spending_ratio = np.random.uniform(0.85, 1.10)  # Overspends sometimes

    total_monthly_outflow = int(total_monthly_inflow * spending_ratio)
    total_monthly_outflow = max(10000, total_monthly_outflow)

    # Step 5: End of month balance
    end_of_month_balance = max(0, total_monthly_inflow - total_monthly_outflow)
    # Add some randomness and savings
    if base_risk == 0:
        end_of_month_balance += int(np.random.uniform(20000, 200000))
    elif base_risk == 1:
        end_of_month_balance += int(np.random.uniform(5000, 50000))
    else:
        end_of_month_balance = int(end_of_month_balance * np.random.uniform(0.3, 0.8))

    # Step 6: Transaction patterns
    transaction_frequency = int(np.random.normal(35, 15))
    transaction_frequency = max(5, min(100, transaction_frequency))

    highest_credit_amount = int(total_monthly_inflow * np.random.uniform(0.3, 0.8))
    highest_debit_amount = int(total_monthly_outflow * np.random.uniform(0.2, 0.6))

    # Step 7: Risk indicators (gambling, loan transactions)
    if base_risk == 0:
        gambling_transactions_count = random.choices([0, 1, 2], weights=[0.85, 0.12, 0.03])[0]
        loan_related_transactions_count = random.choices([0, 1, 2], weights=[0.70, 0.25, 0.05])[0]
    elif base_risk == 1:
        gambling_transactions_count = random.choices([0, 1, 2, 3, 4], weights=[0.50, 0.25, 0.15, 0.07, 0.03])[0]
        loan_related_transactions_count = random.choices([0, 1, 2, 3, 4], weights=[0.30, 0.30, 0.25, 0.10, 0.05])[0]
    else:
        gambling_transactions_count = random.choices([0, 1, 2, 3, 4, 5, 6], weights=[0.20, 0.15, 0.20, 0.20, 0.12, 0.08, 0.05])[0]
        loan_related_transactions_count = random.choices([0, 1, 2, 3, 4, 5], weights=[0.10, 0.15, 0.25, 0.25, 0.15, 0.10])[0]

    # Step 8: Previous loan history
    if base_risk == 0:
        previous_loan_taken = random.choices(["Yes", "No"], weights=[0.40, 0.60])[0]
    elif base_risk == 1:
        previous_loan_taken = random.choices(["Yes", "No"], weights=[0.65, 0.35])[0]
    else:
        previous_loan_taken = random.choices(["Yes", "No"], weights=[0.80, 0.20])[0]

    if previous_loan_taken == "Yes":
        previous_loan_amount = int(total_monthly_inflow * np.random.uniform(1, 6))

        if base_risk == 0:
            repayment_status = random.choices(["On-time", "Late"], weights=[0.90, 0.10])[0]
            missed_payment_count = random.choices([0, 1], weights=[0.85, 0.15])[0]
        elif base_risk == 1:
            repayment_status = random.choices(["On-time", "Late"], weights=[0.55, 0.45])[0]
            missed_payment_count = random.choices([0, 1, 2, 3], weights=[0.40, 0.30, 0.20, 0.10])[0]
        else:
            repayment_status = random.choices(["On-time", "Late"], weights=[0.20, 0.80])[0]
            missed_payment_count = random.choices([0, 1, 2, 3, 4, 5], weights=[0.10, 0.15, 0.25, 0.25, 0.15, 0.10])[0]
    else:
        previous_loan_amount = 0
        repayment_status = "N/A"
        missed_payment_count = 0

    # Step 9: Behavioral data (airtime, data)
    airtime_spend = int(np.random.normal(4000, 2000))
    airtime_spend = max(500, min(15000, airtime_spend))

    data_subscription = int(np.random.normal(5000, 3000))
    data_subscription = max(500, min(25000, data_subscription))

    # Step 10: Demographics
    age = int(np.random.normal(32, 8))
    age = max(18, min(65, age))

    gender = random.choice(GENDER)
    state_of_residence = random.choice(STATES)

    # Step 11: Calculate DEFAULT probability based on all factors
    # This is the key - creating meaningful relationship between features and target

    default_score = 0

    # Employment impact
    if employment_status == "Unemployed":
        default_score += 25
    elif employment_status == "Self-employed":
        default_score += 8

    # Savings ratio impact
    savings_ratio = end_of_month_balance / max(total_monthly_inflow, 1)
    if savings_ratio < 0.05:
        default_score += 20
    elif savings_ratio < 0.15:
        default_score += 10
    elif savings_ratio > 0.40:
        default_score -= 10

    # Gambling impact
    default_score += gambling_transactions_count * 8

    # Missed payments impact (strong signal)
    default_score += missed_payment_count * 12

    # Late repayment impact
    if repayment_status == "Late":
        default_score += 15

    # Loan burden (debt to income)
    if previous_loan_amount > 0:
        debt_ratio = previous_loan_amount / (total_monthly_inflow * 12)
        if debt_ratio > 0.5:
            default_score += 15
        elif debt_ratio > 0.3:
            default_score += 8

    # Age impact (very young = slightly higher risk)
    if age < 23:
        default_score += 5
    elif age > 40:
        default_score -= 3

    # Income stability
    if salary_payment_detected == "Yes":
        default_score -= 10

    # Loan transactions (indicator of multiple loans)
    if loan_related_transactions_count >= 3:
        default_score += 10

    # Add some randomness to avoid perfect prediction
    default_score += np.random.normal(0, 10)

    # Convert score to probability
    default_probability = 1 / (1 + np.exp(-0.08 * (default_score - 25)))

    # Determine if defaulted (with some randomness)
    loan_defaulted = 1 if random.random() < default_probability else 0

    # Build the record (only retained variables)
    record = {
        "age": age,
        "gender": gender,
        "employment_status": employment_status,
        "state_of_residence": state_of_residence,
        "total_monthly_inflow": total_monthly_inflow,
        "total_monthly_outflow": total_monthly_outflow,
        "transaction_frequency": transaction_frequency,
        "salary_payment_detected": salary_payment_detected,
        "end_of_month_balance": end_of_month_balance,
        "highest_credit_amount": highest_credit_amount,
        "highest_debit_amount": highest_debit_amount,
        "gambling_transactions_count": gambling_transactions_count,
        "loan_related_transactions_count": loan_related_transactions_count,
        "previous_loan_taken": previous_loan_taken,
        "previous_loan_amount": previous_loan_amount,
        "repayment_status": repayment_status,
        "missed_payment_count": missed_payment_count,
        "airtime_spend_per_month": airtime_spend,
        "data_subscription_spend": data_subscription,
        "loan_defaulted": loan_defaulted
    }

    return record


def generate_dataset(num_records=1000):
    """Generate the full dataset."""
    data = []
    for i in range(num_records):
        record = generate_realistic_record(i + 1)
        data.append(record)
    return data


def analyze_dataset(data):
    """Print statistics about the generated data."""
    total = len(data)
    defaults = sum(1 for d in data if d["loan_defaulted"] == 1)

    print(f"\n{'='*50}")
    print("GENERATED DATA STATISTICS")
    print(f"{'='*50}")
    print(f"\nTotal Records: {total}")
    print(f"\nTarget Distribution:")
    print(f"  - loan_defaulted=0: {total - defaults} ({(total-defaults)/total*100:.1f}%)")
    print(f"  - loan_defaulted=1: {defaults} ({defaults/total*100:.1f}%)")

    # Employment breakdown
    emp_counts = {}
    for d in data:
        emp = d["employment_status"]
        emp_counts[emp] = emp_counts.get(emp, 0) + 1
    print(f"\nEmployment Status:")
    for emp, count in sorted(emp_counts.items()):
        print(f"  - {emp}: {count} ({count/total*100:.1f}%)")

    # Default rate by employment
    print(f"\nDefault Rate by Employment:")
    for emp in EMPLOYMENT_STATUS:
        emp_records = [d for d in data if d["employment_status"] == emp]
        emp_defaults = sum(1 for d in emp_records if d["loan_defaulted"] == 1)
        if emp_records:
            print(f"  - {emp}: {emp_defaults}/{len(emp_records)} ({emp_defaults/len(emp_records)*100:.1f}%)")

    # Default rate by gambling
    print(f"\nDefault Rate by Gambling Transactions:")
    for g in range(7):
        g_records = [d for d in data if d["gambling_transactions_count"] == g]
        g_defaults = sum(1 for d in g_records if d["loan_defaulted"] == 1)
        if g_records:
            print(f"  - Gambling={g}: {g_defaults}/{len(g_records)} ({g_defaults/len(g_records)*100:.1f}%)")

    # Feature list
    print(f"\n{'='*50}")
    print("FEATURES IN DATASET (19 + 1 target)")
    print(f"{'='*50}")
    for key in data[0].keys():
        print(f"  - {key}")


if __name__ == "__main__":
    # Generate 20000 records
    print("Generating 20,000 realistic credit records...")
    data = generate_dataset(20000)

    # Save to JSON
    output_path = "data.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\nData saved to {output_path}")

    # Show statistics
    analyze_dataset(data)
