import React, { useState } from 'react';
import LandingPage from './pages/LandingPage';
import CreditForm from './pages/CreditForm';
import './App.css';

const App = () => {
  const [showLanding, setShowLanding] = useState(true);

  return (
    <>
      {showLanding ? (
        <LandingPage onGetStarted={() => setShowLanding(false)} />
      ) : (
        <CreditForm onBackToHome={() => setShowLanding(true)} />
      )}
    </>
  );
};

export default App;