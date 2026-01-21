/**
 * API Service for Credit Worthiness Assessment
 */

const API_BASE_URL = 'http://localhost:8000';

/**
 * Extract financial data from bank statement
 * @param {File} file - PDF or CSV bank statement file
 * @returns {Promise<Object>} Extracted financial variables
 */
export const extractFinancialData = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/extract`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Extraction failed');
  }

  return response.json();
};

/**
 * Predict credit worthiness
 * @param {Object} data - Form data with all fields
 * @returns {Promise<Object>} Prediction results
 */
export const predictCredit = async (data) => {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Prediction failed');
  }

  return response.json();
};

/**
 * Get AI-generated personalized feedback
 * @param {Object} data - User data and assessment results
 * @returns {Promise<Object>} Feedback message
 */
export const getFeedback = async (data) => {
  const response = await fetch(`${API_BASE_URL}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Feedback generation failed');
  }

  return response.json();
};

/**
 * Health check
 * @returns {Promise<Object>} Health status
 */
export const healthCheck = async () => {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
};
