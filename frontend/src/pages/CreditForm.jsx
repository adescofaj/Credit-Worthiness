import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Stepper from '../components/Stepper';
import ResultCard from '../components/ResultCard';
import { ArrowLeft, ArrowRight, CheckCircle, Loader2, AlertCircle } from 'lucide-react';
import { initialFormData, formSteps } from '../utils/formData';
import { predictCredit, getFeedback } from '../services/api';
import { validateStep } from '../utils/validation';

const CreditForm = ({ onBackToHome }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [showResults, setShowResults] = useState(false);
  const [formData, setFormData] = useState(initialFormData);
  const [results, setResults] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState(null);
  const [stepErrors, setStepErrors] = useState({});

  const handleNext = () => {
    // Validate current step before proceeding
    const { isValid, errors } = validateStep(currentStep, formData);

    if (!isValid) {
      setStepErrors(errors);
      return;
    }

    // Clear errors and move to next step
    setStepErrors({});
    if (currentStep < formSteps.length - 1) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    setStepErrors({});
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmit = async () => {
    // Validate final step before submitting
    const { isValid, errors } = validateStep(currentStep, formData);

    if (!isValid) {
      setStepErrors(errors);
      return;
    }

    setIsSubmitting(true);
    setSubmitError(null);
    setStepErrors({});

    try {
      // Prepare data for prediction API
      const predictionData = {
        age: parseInt(formData.age) || 0,
        gender: formData.gender,
        employment_status: formData.employment_status,
        total_monthly_inflow: parseFloat(formData.total_monthly_inflow) || 0,
        total_monthly_outflow: parseFloat(formData.total_monthly_outflow) || 0,
        transaction_frequency: parseInt(formData.transaction_frequency) || 0,
        salary_payment_detected: formData.salary_payment_detected || 'No',
        end_of_month_balance: parseFloat(formData.end_of_month_balance) || 0,
        highest_credit_amount: parseFloat(formData.highest_credit_amount) || 0,
        highest_debit_amount: parseFloat(formData.highest_debit_amount) || 0,
        gambling_transactions_count: parseInt(formData.gambling_transactions_count) || 0,
        loan_related_transactions_count: parseInt(formData.loan_related_transactions_count) || 0,
        previous_loan_taken: formData.previous_loan_taken || 'No',
        previous_loan_amount: parseFloat(formData.previous_loan_amount) || 0,
        repayment_status: formData.repayment_status || 'N/A',
        missed_payment_count: parseInt(formData.missed_payment_count) || 0,
        airtime_spend_per_month: parseFloat(formData.airtime_spend_per_month) || 0,
        data_subscription_spend: parseFloat(formData.data_subscription_spend) || 0,
      };

      const response = await predictCredit(predictionData);

      // Map response to expected format
      const predictionResults = {
        loan_defaulted: response.loan_defaulted,
        credit_score_generated: response.credit_score,
        risk_category: response.risk_category,
        default_probability: response.default_probability,
      };
      setResults(predictionResults);

      // Fetch AI-generated feedback
      try {
        const feedbackData = {
          name: formData.full_name || '',
          age: parseInt(formData.age) || 0,
          employment_status: formData.employment_status,
          total_monthly_inflow: parseFloat(formData.total_monthly_inflow) || 0,
          total_monthly_outflow: parseFloat(formData.total_monthly_outflow) || 0,
          end_of_month_balance: parseFloat(formData.end_of_month_balance) || 0,
          salary_payment_detected: formData.salary_payment_detected || 'No',
          transaction_frequency: parseInt(formData.transaction_frequency) || 0,
          gambling_transactions_count: parseInt(formData.gambling_transactions_count) || 0,
          previous_loan_taken: formData.previous_loan_taken || 'No',
          repayment_status: formData.repayment_status || 'N/A',
          missed_payment_count: parseInt(formData.missed_payment_count) || 0,
          credit_score: response.credit_score,
          risk_category: response.risk_category,
          default_probability: response.default_probability,
        };
        const feedbackResponse = await getFeedback(feedbackData);
        setFeedback(feedbackResponse.feedback);
      } catch (feedbackError) {
        console.error('Failed to get feedback:', feedbackError);
        // Don't fail the whole submission if feedback fails
        setFeedback(null);
      }

      setShowResults(true);
    } catch (error) {
      setSubmitError(error.message || 'Failed to get prediction. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNewAssessment = () => {
    setShowResults(false);
    setCurrentStep(0);
    setFormData(initialFormData);
    setResults(null);
    setFeedback(null);
    setStepErrors({});
  };

  const CurrentStepComponent = formSteps[currentStep].component;
  const hasErrors = Object.keys(stepErrors).length > 0;

  if (showResults && results) {
    return (
      <div className="min-h-screen py-20 px-6 bg-gradient-to-br from-off-white to-cream-bg">
        <ResultCard results={results} userName={formData.full_name} feedback={feedback} />
        <div className="text-center mt-8 space-x-4">
          <button
            onClick={handleNewAssessment}
            className="px-8 py-3 rounded-xl text-white font-semibold transition-all duration-300 hover:scale-105 bg-medium-brown"
          >
            New Assessment
          </button>
          <button
            onClick={onBackToHome}
            className="px-8 py-3 rounded-xl font-semibold transition-all duration-300 hover:scale-105 bg-light-tan text-deep-coffee"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-20 px-6 bg-gradient-to-br from-off-white to-cream-bg">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold mb-2 text-deep-coffee">Credit Assessment Form</h1>
          <p className="text-medium-brown">Complete all sections for accurate evaluation</p>
        </motion.div>

        <Stepper currentStep={currentStep} steps={formSteps} />

        <div className="p-8 rounded-3xl shadow-xl mb-8 bg-off-white">
          <CurrentStepComponent
            formData={formData}
            setFormData={setFormData}
            errors={stepErrors}
          />
        </div>

        {hasErrors && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-4 p-4 rounded-xl bg-red-50 border border-red-200 text-red-600 flex items-center gap-2"
          >
            <AlertCircle size={20} />
            <span>Please fill in all required fields before proceeding.</span>
          </motion.div>
        )}

        {submitError && (
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-4 p-4 rounded-xl bg-red-50 border border-red-200 text-red-600 text-center"
          >
            {submitError}
          </motion.div>
        )}

        <div className="flex justify-between max-w-4xl mx-auto">
          <button
            onClick={handlePrevious}
            disabled={currentStep === 0}
            className={`px-8 py-3 rounded-xl font-semibold flex items-center gap-2 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed hover:scale-105 ${
              currentStep === 0
                ? 'bg-light-tan text-deep-coffee'
                : 'bg-medium-brown text-off-white'
            }`}
          >
            <ArrowLeft size={20} />
            Previous
          </button>

          {currentStep === formSteps.length - 1 ? (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className={`px-8 py-3 rounded-xl text-white font-semibold flex items-center gap-2 transition-all duration-300 ${isSubmitting ? 'bg-gray-400' : 'hover:scale-105 bg-gradient-to-r from-medium-brown to-deep-coffee'}`}
            >
              {isSubmitting ? (
                <>
                  <Loader2 size={20} className="animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  Submit Assessment
                  <CheckCircle size={20} />
                </>
              )}
            </button>
          ) : (
            <button
              onClick={handleNext}
              className="px-8 py-3 rounded-xl text-white font-semibold flex items-center gap-2 transition-all duration-300 hover:scale-105 bg-muted-gold"
            >
              Next
              <ArrowRight size={20} />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default CreditForm;
