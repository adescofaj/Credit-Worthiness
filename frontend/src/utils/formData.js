import UserDemographics from '../components/UserDemographics';
import FileUpload from '../components/FileUpload';
import LoanHistory from '../components/LoanHistory';
import UserBehaviour from '../components/UserBehaviour';

export const initialFormData = {
  // Demographics (Step 1)
  full_name: '', // optional - for personalization only
  age: '',
  gender: '',
  employment_status: '',

  // Financial Data (Step 2) - extracted from bank statement or manual entry
  bank_statement: null, // optional - file object
  total_monthly_inflow: '',
  total_monthly_outflow: '',
  transaction_frequency: '',
  salary_payment_detected: '',
  end_of_month_balance: '',
  highest_credit_amount: '',
  highest_debit_amount: '',
  gambling_transactions_count: '', // optional - defaults to 0
  loan_related_transactions_count: '', // optional - defaults to 0

  // Loan History (Step 3)
  previous_loan_taken: '',
  previous_loan_amount: '', // conditional - required if previous_loan_taken === 'Yes'
  repayment_status: '', // conditional - required if previous_loan_taken === 'Yes'
  missed_payment_count: '', // conditional - required if previous_loan_taken === 'Yes'

  // Behaviour (Step 4)
  airtime_spend_per_month: '',
  data_subscription_spend: ''
};

export const formSteps = [
  {
    label: 'Demographics',
    icon: '👤',
    component: UserDemographics
  },
  {
    label: 'Financial Data',
    icon: '📊',
    component: FileUpload
  },
  {
    label: 'Loan History',
    icon: '📜',
    component: LoanHistory
  },
  {
    label: 'Behaviour',
    icon: '📱',
    component: UserBehaviour
  }
];
