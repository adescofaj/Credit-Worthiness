import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, MessageSquare } from 'lucide-react';

const ResultCard = ({ results, userName, feedback }) => {
  const getRiskColorClass = (risk) => {
    if (risk === 'Low') return 'bg-green-500';
    if (risk === 'Medium') return 'bg-muted-gold';
    return 'bg-red-500';
  };

  const getRiskTextClass = (risk) => {
    if (risk === 'Low') return 'text-green-500';
    if (risk === 'Medium') return 'text-muted-gold';
    return 'text-red-500';
  };

  const getRiskBorderClass = (risk) => {
    if (risk === 'Low') return 'border-green-200';
    if (risk === 'Medium') return 'border-muted-gold/30';
    return 'border-red-200';
  };

  const getRiskBgClass = (risk) => {
    if (risk === 'Low') return 'bg-green-50';
    if (risk === 'Medium') return 'bg-amber-50';
    return 'bg-red-50';
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="max-w-2xl mx-auto"
    >
      <div className="p-8 rounded-3xl shadow-2xl bg-off-white">
        <div className="text-center mb-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", duration: 0.8 }}
            className={`w-24 h-24 rounded-full mx-auto mb-4 flex items-center justify-center ${getRiskColorClass(results.risk_category)}`}
          >
            <CheckCircle size={48} className="text-white" />
          </motion.div>
          <h2 className="text-3xl font-bold mb-2 text-deep-coffee">
            {userName ? `${userName}'s Assessment Complete!` : 'Assessment Complete!'}
          </h2>
          <p className="text-medium-brown">Here's your creditworthiness analysis</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl text-center bg-cream-bg">
            <p className="text-sm mb-2 text-medium-brown">Credit Score</p>
            <p className="text-4xl font-bold text-deep-coffee">{results.credit_score_generated}</p>
          </div>

          <div className="p-6 rounded-2xl text-center bg-cream-bg">
            <p className="text-sm mb-2 text-medium-brown">Risk Category</p>
            <p className={`text-2xl font-bold ${getRiskTextClass(results.risk_category)}`}>{results.risk_category}</p>
          </div>

          <div className="p-6 rounded-2xl text-center bg-cream-bg">
            <p className="text-sm mb-2 text-medium-brown">Default Risk</p>
            <p className={`text-2xl font-bold ${results.loan_defaulted === 0 ? 'text-green-500' : 'text-red-500'}`}>
              {results.loan_defaulted === 0 ? 'Low' : 'High'}
            </p>
          </div>
        </div>

        {/* AI Feedback Section */}
        {feedback && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className={`mt-8 p-6 rounded-2xl border-2 ${getRiskBorderClass(results.risk_category)} ${getRiskBgClass(results.risk_category)}`}
          >
            <div className="flex items-start gap-3">
              <div className={`p-2 rounded-lg ${getRiskColorClass(results.risk_category)}`}>
                <MessageSquare size={20} className="text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-deep-coffee mb-2">AI Assessment</h3>
                <p className="text-medium-brown leading-relaxed">{feedback}</p>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
};

export default ResultCard;
