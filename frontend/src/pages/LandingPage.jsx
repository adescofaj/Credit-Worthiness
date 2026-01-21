import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Zap, Shield, TrendingUp, ArrowRight } from 'lucide-react';

const LandingPage = ({ onGetStarted }) => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const features = [
    { icon: Shield, title: 'Secure & Private', desc: 'Your data is encrypted and protected' },
    { icon: Zap, title: 'Instant Analysis', desc: 'Get results in seconds with AI' },
    { icon: TrendingUp, title: 'Accurate Scoring', desc: 'ML-powered credit assessment' }
  ];

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-off-white to-cream-bg">
      {/* Animated floating shapes */}
      <motion.div
        className="absolute w-96 h-96 rounded-full opacity-20 blur-3xl bg-medium-brown top-[10%] left-[5]"
        animate={{
          y: [0, 50, 0],
          x: [0, 30, 0],
        }}
        transition={{ duration: 20, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute w-80 h-80 rounded-full opacity-15 blur-3xl bg-muted-gold bottom-[10%] right-[10%]"
        animate={{
          y: [0, -40, 0],
          x: [0, -20, 0],
        }}
        transition={{ duration: 15, repeat: Infinity, ease: "easeInOut" }}
      />

      <div className="relative z-10 container mx-auto px-6 py-20 flex flex-col items-center justify-center min-h-screen">
        {/* Animated Badge */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8 px-6 py-3 rounded-full backdrop-blur-sm bg-muted-gold/10 border border-muted-gold/25"
        >
          <div className="flex items-center gap-2 text-medium-brown">
            <Zap size={18} />
            <span className="text-sm font-semibold">Powered by Advanced AI</span>
          </div>
        </motion.div>

        {/* Main Animated Headline */}
        <div className="text-center mb-6 max-w-4xl">
          <motion.h1 className="text-6xl md:text-7xl font-bold mb-4 leading-tight text-deep-coffee">
            <motion.span
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.8,
                delay: 0,
                ease: [0.6, -0.05, 0.01, 0.99]
              }}
              className="inline-block mr-4"
            >
              AI-Powered
            </motion.span>
            <motion.span
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.8,
                delay: 0.2,
                ease: [0.6, -0.05, 0.01, 0.99]
              }}
              className="inline-block mr-4 bg-gradient-to-r from-medium-brown to-muted-gold bg-clip-text text-transparent"
            >
              Credit Worthiness
            </motion.span>
            <motion.span
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.8,
                delay: 0.4,
                ease: [0.6, -0.05, 0.01, 0.99]
              }}
              className="inline-block"
            >
              Evaluation
            </motion.span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.8 }}
            className="text-xl md:text-2xl mb-12 text-medium-brown"
          >
            Get your creditworthiness assessed intelligently with machine learning
          </motion.p>
        </div>

        {/* Feature Cards */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 1 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12 w-full max-w-5xl"
        >
          {features.map((feature, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.05, y: -5 }}
              className="p-6 rounded-2xl backdrop-blur-sm transition-all duration-300 bg-off-white border border-light-tan/25 shadow-xl"
            >
              <feature.icon size={32} className="mb-4 text-muted-gold" />
              <h3 className="text-lg font-bold mb-2 text-deep-coffee">{feature.title}</h3>
              <p className="text-sm text-medium-brown">{feature.desc}</p>
            </motion.div>
          ))}
        </motion.div>

        {/* CTA Button */}
        <motion.button
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6, delay: 1.2 }}
          whileHover={{
            scale: 1.08,
            boxShadow: "0 0 30px rgba(123, 75, 42, 0.5), 0 0 60px rgba(212, 163, 115, 0.3)"
          }}
          whileTap={{ scale: 0.95 }}
          onClick={onGetStarted}
          className="group relative px-10 py-5 rounded-2xl text-white font-bold text-lg flex items-center gap-3 transition-all duration-300 shadow-2xl bg-gradient-to-r from-medium-brown to-deep-coffee overflow-hidden"
        >
          <span className="absolute inset-0 bg-gradient-to-r from-muted-gold to-medium-brown opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
          <span className="relative z-10 flex items-center gap-3">
            Get Started
            <motion.span
              className="inline-block"
              whileHover={{ x: 5 }}
              transition={{ type: "spring", stiffness: 400 }}
            >
              <ArrowRight size={24} />
            </motion.span>
          </span>
        </motion.button>
      </div>
    </div>
  );
};

export default LandingPage;