// Validation rules for each form step

export const validationRules = {
  // Step 0: Demographics
  0: {
    required: ['age', 'gender', 'employment_status'],
    optional: ['full_name', 'occupation', 'state_of_residence'],
  },
  // Step 1: Financial Data
  1: {
    required: [
      'total_monthly_inflow',
      'total_monthly_outflow',
      'transaction_frequency',
      'salary_payment_detected',
      'end_of_month_balance',
      'highest_credit_amount',
      'highest_debit_amount',
    ],
    optional: ['bank_statement', 'gambling_transactions_count', 'loan_related_transactions_count'],
  },
  // Step 2: Loan History
  2: {
    required: ['previous_loan_taken'],
    conditionalRequired: {
      // If previous_loan_taken === 'Yes', these become required
      previous_loan_taken: {
        Yes: ['previous_loan_amount', 'repayment_status', 'missed_payment_count'],
      },
    },
    optional: [],
  },
  // Step 3: Behaviour
  3: {
    required: ['airtime_spend_per_month', 'data_subscription_spend'],
    optional: [],
  },
};

// Field labels for error messages
export const fieldLabels = {
  age: 'Age',
  gender: 'Gender',
  employment_status: 'Employment Status',
  full_name: 'Full Name',
  occupation: 'Occupation',
  state_of_residence: 'State of Residence',
  total_monthly_inflow: 'Total Monthly Inflow',
  total_monthly_outflow: 'Total Monthly Outflow',
  transaction_frequency: 'Transaction Frequency',
  salary_payment_detected: 'Salary Payment Detected',
  end_of_month_balance: 'End of Month Balance',
  highest_credit_amount: 'Highest Credit Amount',
  highest_debit_amount: 'Highest Debit Amount',
  gambling_transactions_count: 'Gambling Transactions',
  loan_related_transactions_count: 'Loan-Related Transactions',
  previous_loan_taken: 'Previous Loan Taken',
  previous_loan_amount: 'Previous Loan Amount',
  repayment_status: 'Repayment Status',
  missed_payment_count: 'Missed Payment Count',
  airtime_spend_per_month: 'Airtime Spend per Month',
  data_subscription_spend: 'Data Subscription Spend',
};

// Check if a value is empty
const isEmpty = (value) => {
  if (value === null || value === undefined) return true;
  if (typeof value === 'string' && value.trim() === '') return true;
  if (typeof value === 'number' && isNaN(value)) return true;
  return false;
};

// Validate a specific step
export const validateStep = (step, formData) => {
  const rules = validationRules[step];
  const errors = {};

  // Check required fields
  rules.required.forEach((field) => {
    if (isEmpty(formData[field])) {
      errors[field] = `${fieldLabels[field]} is required`;
    }
  });

  // Check conditional required fields
  if (rules.conditionalRequired) {
    Object.entries(rules.conditionalRequired).forEach(([triggerField, conditions]) => {
      const triggerValue = formData[triggerField];
      if (conditions[triggerValue]) {
        conditions[triggerValue].forEach((field) => {
          if (isEmpty(formData[field])) {
            errors[field] = `${fieldLabels[field]} is required`;
          }
        });
      }
    });
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
};

// Get required fields for a step (including conditional)
export const getRequiredFields = (step, formData) => {
  const rules = validationRules[step];
  const requiredFields = [...rules.required];

  // Add conditional required fields
  if (rules.conditionalRequired) {
    Object.entries(rules.conditionalRequired).forEach(([triggerField, conditions]) => {
      const triggerValue = formData[triggerField];
      if (conditions[triggerValue]) {
        requiredFields.push(...conditions[triggerValue]);
      }
    });
  }

  return requiredFields;
};

// Check if a field is required
export const isFieldRequired = (field, step, formData) => {
  const requiredFields = getRequiredFields(step, formData);
  return requiredFields.includes(field);
};
