import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FinancialChat from './chat/FinancialChat';
import Dashboard from './components/dashboard/Dashboard';
import ChatIcon from './components/ChatIcon';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/chatbot" element={<FinancialChat />} />
      </Routes>
      <ChatIcon />
    </Router>
  );
}

export default App;
