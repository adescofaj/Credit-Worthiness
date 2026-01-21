import React from 'react';
import { motion } from 'framer-motion';

const UserDemographics = ({ formData, setFormData, errors = {} }) => {
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

  const OptionalLabel = ({ children }) => (
    <label className="block text-sm font-semibold mb-2 text-deep-coffee">
      {children} <span className="text-medium-brown text-xs">(optional)</span>
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
          <OptionalLabel>Full Name</OptionalLabel>
          <input
            type="text"
            value={formData.full_name}
            onChange={(e) => handleChange('full_name', e.target.value)}
            className={inputClass('full_name')}
            placeholder="Enter your full name"
          />
        </div>

        <div>
          <RequiredLabel field="age">Age</RequiredLabel>
          <input
            type="number"
            value={formData.age}
            onChange={(e) => handleChange('age', e.target.value)}
            className={inputClass('age')}
            placeholder="Your age"
            min="18"
            max="100"
          />
        </div>

        <div>
          <RequiredLabel field="gender">Gender</RequiredLabel>
          <select
            value={formData.gender}
            onChange={(e) => handleChange('gender', e.target.value)}
            className={inputClass('gender')}
          >
            <option value="">Select gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>

        <div>
          <RequiredLabel field="employment_status">Employment Status</RequiredLabel>
          <select
            value={formData.employment_status}
            onChange={(e) => handleChange('employment_status', e.target.value)}
            className={inputClass('employment_status')}
          >
            <option value="">Select status</option>
            <option value="Employed">Employed</option>
            <option value="Self-employed">Self-employed</option>
            <option value="Unemployed">Unemployed</option>
          </select>
        </div>
      </div>
    </motion.div>
  );
};

export default UserDemographics;
