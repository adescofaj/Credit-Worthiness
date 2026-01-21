import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle } from 'lucide-react';

const Stepper = ({ currentStep, steps }) => {
  return (
    <div className="flex items-center justify-between mb-12 max-w-2xl mx-auto">
      {steps.map((step, index) => (
        <div key={index} className="flex items-center flex-1">
          <div className="flex flex-col items-center flex-1">
            <motion.div
              className={`w-12 h-12 rounded-full flex items-center justify-center font-bold transition-all duration-300 ${
                currentStep >= index
                  ? 'bg-muted-gold text-off-white'
                  : 'bg-light-tan text-medium-brown'
              } ${currentStep === index ? 'shadow-[0_0_20px_rgba(212,163,115,0.5)]' : ''}`}
              animate={{ scale: currentStep === index ? 1.1 : 1 }}
            >
              {currentStep > index ? <CheckCircle size={24} /> : index + 1}
            </motion.div>
            <span className="text-xs mt-2 text-center text-medium-brown">
              {step.icon} {step.label}
            </span>
          </div>
          {index < steps.length - 1 && (
            <div
              className={`flex-1 h-1 mx-2 rounded ${
                currentStep > index ? 'bg-muted-gold' : 'bg-light-tan'
              }`}
            />
          )}
        </div>
      ))}
    </div>
  );
};

export default Stepper;
