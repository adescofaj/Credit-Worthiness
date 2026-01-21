import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Upload, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { extractFinancialData } from '../services/api';

const FileUpload = ({ formData, setFormData, errors = {} }) => {
  const [fileName, setFileName] = useState('');
  const [isExtracting, setIsExtracting] = useState(false);
  const [extractionError, setExtractionError] = useState(null);
  const [extractionSuccess, setExtractionSuccess] = useState(false);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setFormData({ ...formData, bank_statement: file });
    setIsExtracting(true);
    setExtractionError(null);
    setExtractionSuccess(false);

    try {
      const extracted = await extractFinancialData(file);

      setFormData(prev => ({
        ...prev,
        bank_statement: file,
        total_monthly_inflow: extracted.total_monthly_inflow,
        total_monthly_outflow: extracted.total_monthly_outflow,
        transaction_frequency: extracted.transaction_frequency,
        salary_payment_detected: extracted.salary_payment_detected,
        end_of_month_balance: extracted.end_of_month_balance,
        highest_credit_amount: extracted.highest_credit_amount,
        highest_debit_amount: extracted.highest_debit_amount,
        gambling_transactions_count: extracted.gambling_transactions_count,
        loan_related_transactions_count: extracted.loan_related_transactions_count,
      }));

      setExtractionSuccess(true);
    } catch (error) {
      setExtractionError(error.message || 'Failed to extract data. Please fill manually.');
    } finally {
      setIsExtracting(false);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
  };

  const inputClass = (field) => `w-full px-4 py-2 rounded-lg border bg-white focus:outline-none focus:ring-2 focus:ring-muted-gold ${
    errors[field] ? 'border-red-400' : 'border-light-tan'
  }`;

  const RequiredLabel = ({ children, field }) => (
    <label className="block text-sm font-medium text-deep-coffee mb-1">
      {children} <span className="text-red-500">*</span>
      {errors[field] && <span className="text-red-500 text-xs ml-1">- Required</span>}
    </label>
  );

  const OptionalLabel = ({ children }) => (
    <label className="block text-sm font-medium text-deep-coffee mb-1">
      {children} <span className="text-medium-brown text-xs">(optional)</span>
    </label>
  );

  const hasErrors = Object.keys(errors).length > 0;

  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -50 }}
      className="space-y-6"
    >
      {/* File Upload Section */}
      <div className="p-8 rounded-2xl text-center bg-off-white border-2 border-dashed border-muted-gold">
        <Upload size={48} className="mx-auto mb-4 text-muted-gold" />
        <h3 className="text-xl font-bold mb-2 text-deep-coffee">Upload Your Bank Statement</h3>
        <p className="mb-6 text-medium-brown">
          Our AI engine will automatically extract your financial data
        </p>
        <label className={`cursor-pointer inline-block px-8 py-3 rounded-xl text-white font-semibold transition-all duration-300 ${isExtracting ? 'bg-gray-400' : 'hover:scale-105 bg-muted-gold'}`}>
          {isExtracting ? (
            <span className="flex items-center gap-2">
              <Loader2 size={20} className="animate-spin" />
              Extracting...
            </span>
          ) : (
            'Choose File (PDF or CSV)'
          )}
          <input
            type="file"
            accept=".pdf,.csv"
            onChange={handleFileChange}
            className="hidden"
            disabled={isExtracting}
          />
        </label>

        {fileName && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-4 flex items-center justify-center gap-2"
          >
            {extractionSuccess && <CheckCircle size={20} className="text-green-600" />}
            {extractionError && <AlertCircle size={20} className="text-red-500" />}
            <span className="font-semibold text-deep-coffee">{fileName}</span>
          </motion.div>
        )}

        {extractionError && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-2 text-red-500 text-sm"
          >
            {extractionError}
          </motion.p>
        )}
      </div>

      {/* Manual Entry / Extracted Data Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className={`p-6 rounded-2xl bg-cream-bg border ${hasErrors ? 'border-red-300' : 'border-light-tan'}`}
      >
        <h4 className="text-lg font-bold mb-4 text-deep-coffee flex items-center gap-2">
          {extractionSuccess ? (
            <>
              <CheckCircle size={20} className="text-green-600" />
              Extracted Financial Data
            </>
          ) : (
            'Financial Data'
          )}
        </h4>
        <p className="text-sm text-medium-brown mb-4">
          {extractionSuccess
            ? 'Review and correct if needed. Fields marked with * are required.'
            : 'Enter your financial data manually or upload a bank statement. Fields marked with * are required.'}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <RequiredLabel field="total_monthly_inflow">Total Monthly Inflow (₦)</RequiredLabel>
            <input
              type="number"
              value={formData.total_monthly_inflow}
              onChange={(e) => handleInputChange('total_monthly_inflow', e.target.value)}
              className={inputClass('total_monthly_inflow')}
              placeholder="0"
            />
          </div>

          <div>
            <RequiredLabel field="total_monthly_outflow">Total Monthly Outflow (₦)</RequiredLabel>
            <input
              type="number"
              value={formData.total_monthly_outflow}
              onChange={(e) => handleInputChange('total_monthly_outflow', e.target.value)}
              className={inputClass('total_monthly_outflow')}
              placeholder="0"
            />
          </div>

          <div>
            <RequiredLabel field="transaction_frequency">Transaction Frequency</RequiredLabel>
            <input
              type="number"
              value={formData.transaction_frequency}
              onChange={(e) => handleInputChange('transaction_frequency', e.target.value)}
              className={inputClass('transaction_frequency')}
              placeholder="Number of transactions"
            />
          </div>

          <div>
            <RequiredLabel field="salary_payment_detected">Salary Payment Detected</RequiredLabel>
            <select
              value={formData.salary_payment_detected}
              onChange={(e) => handleInputChange('salary_payment_detected', e.target.value)}
              className={inputClass('salary_payment_detected')}
            >
              <option value="">Select</option>
              <option value="Yes">Yes</option>
              <option value="No">No</option>
            </select>
          </div>

          <div>
            <RequiredLabel field="end_of_month_balance">End of Month Balance (₦)</RequiredLabel>
            <input
              type="number"
              value={formData.end_of_month_balance}
              onChange={(e) => handleInputChange('end_of_month_balance', e.target.value)}
              className={inputClass('end_of_month_balance')}
              placeholder="0"
            />
          </div>

          <div>
            <RequiredLabel field="highest_credit_amount">Highest Credit Amount (₦)</RequiredLabel>
            <input
              type="number"
              value={formData.highest_credit_amount}
              onChange={(e) => handleInputChange('highest_credit_amount', e.target.value)}
              className={inputClass('highest_credit_amount')}
              placeholder="0"
            />
          </div>

          <div>
            <RequiredLabel field="highest_debit_amount">Highest Debit Amount (₦)</RequiredLabel>
            <input
              type="number"
              value={formData.highest_debit_amount}
              onChange={(e) => handleInputChange('highest_debit_amount', e.target.value)}
              className={inputClass('highest_debit_amount')}
              placeholder="0"
            />
          </div>

          <div>
            <OptionalLabel>Gambling Transactions Count</OptionalLabel>
            <input
              type="number"
              value={formData.gambling_transactions_count}
              onChange={(e) => handleInputChange('gambling_transactions_count', e.target.value)}
              className={inputClass('gambling_transactions_count')}
              placeholder="0"
            />
          </div>

          <div>
            <OptionalLabel>Loan-Related Transactions</OptionalLabel>
            <input
              type="number"
              value={formData.loan_related_transactions_count}
              onChange={(e) => handleInputChange('loan_related_transactions_count', e.target.value)}
              className={inputClass('loan_related_transactions_count')}
              placeholder="0"
            />
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default FileUpload;
