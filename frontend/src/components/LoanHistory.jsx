import React from 'react';
import { motion } from 'framer-motion';

const LoanHistory = ({ formData, setFormData, errors = {} }) => {
  const handleChange = (field, value) => {
    // Reset conditional fields when previous_loan_taken changes to "No"
    if (field === 'previous_loan_taken' && value === 'No') {
      setFormData({
        ...formData,
        [field]: value,
        previous_loan_amount: '',
        repayment_status: 'N/A',
        missed_payment_count: '0',
      });
    } else {
      setFormData({ ...formData, [field]: value });
    }
  };

  const inputClass = (field) => `w-full px-4 py-3 rounded-xl border-2 bg-off-white transition-all duration-300 focus:outline-none ${
    errors[field] ? 'border-red-400 focus:border-red-500' : 'border-light-tan focus:border-muted-gold'
  }`;

  const RequiredLabel = ({ children, field }) => (
    <label className="block text-sm font-semibold mb-2 text-deep-coffee">
      {children} <span className="text-red-500">*</span>
      {errors[field] && <span className="text-red-500 text-xs ml-2">({errors[field]})</span>}
    </label>
  );

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="space-y-6"
    >
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <RequiredLabel field="previous_loan_taken">Previous Loan Taken?</RequiredLabel>
          <select
            value={formData.previous_loan_taken}
            onChange={(e) => handleChange('previous_loan_taken', e.target.value)}
            className={inputClass('previous_loan_taken')}
          >
            <option value="">Select</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>

        {formData.previous_loan_taken === 'Yes' && (
          <>
            <div>
              <RequiredLabel field="previous_loan_amount">Previous Loan Amount (₦)</RequiredLabel>
              <input
                type="number"
                value={formData.previous_loan_amount}
                onChange={(e) => handleChange('previous_loan_amount', e.target.value)}
                className={inputClass('previous_loan_amount')}
                placeholder="Amount"
              />
            </div>

            <div>
              <RequiredLabel field="repayment_status">Repayment Status</RequiredLabel>
              <select
                value={formData.repayment_status}
                onChange={(e) => handleChange('repayment_status', e.target.value)}
                className={inputClass('repayment_status')}
              >
                <option value="">Select status</option>
                <option value="On Time">On Time</option>
                <option value="Late">Late</option>
                <option value="Defaulted">Defaulted</option>
              </select>
            </div>

            <div>
              <RequiredLabel field="missed_payment_count">Missed Payment Count</RequiredLabel>
              <input
                type="number"
                value={formData.missed_payment_count}
                onChange={(e) => handleChange('missed_payment_count', e.target.value)}
                className={inputClass('missed_payment_count')}
                placeholder="Number of missed payments"
                min="0"
              />
            </div>
          </>
        )}
      </div>

      {formData.previous_loan_taken === 'No' && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-sm text-medium-brown italic"
        >
          No previous loan history will be recorded for this assessment.
        </motion.p>
      )}
    </motion.div>
  );
};

export default LoanHistory;
