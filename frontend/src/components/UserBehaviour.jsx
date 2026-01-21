import React from 'react';
import { motion } from 'framer-motion';

const UserBehaviour = ({ formData, setFormData, errors = {} }) => {
  const handleChange = (field, value) => {
    setFormData({ ...formData, [field]: value });
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
          <RequiredLabel field="airtime_spend_per_month">Airtime Spend per Month (₦)</RequiredLabel>
          <input
            type="number"
            value={formData.airtime_spend_per_month}
            onChange={(e) => handleChange('airtime_spend_per_month', e.target.value)}
            className={inputClass('airtime_spend_per_month')}
            placeholder="Monthly airtime spend"
            min="0"
          />
        </div>

        <div>
          <RequiredLabel field="data_subscription_spend">Data Subscription Spend (₦)</RequiredLabel>
          <input
            type="number"
            value={formData.data_subscription_spend}
            onChange={(e) => handleChange('data_subscription_spend', e.target.value)}
            className={inputClass('data_subscription_spend')}
            placeholder="Monthly data spend"
            min="0"
          />
        </div>
      </div>

      <p className="text-sm text-medium-brown">
        This information helps us understand your spending patterns and financial behavior.
      </p>
    </motion.div>
  );
};

export default UserBehaviour;
