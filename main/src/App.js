// Plik: frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './DashboardPage';
import AuthCallback from './AuthCallback';

const LoginView = () => {
  // Przycisk logowania bez zmian
  const LOGIN_URL = 'http://127.0.0.1:5000/login';
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', backgroundColor: '#191414', color: 'white' }}>
      <h1>Spotify Analyzer</h1>
      <a href={LOGIN_URL} style={{ padding: '15px 30px', borderRadius: '50px', backgroundColor: '#1DB954', color: 'white', textDecoration: 'none' }}>
        ZALOGUJ SIĘ PRZEZ SPOTIFY
      </a>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/auth/callback" element={<AuthCallback />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/" element={<LoginView />} />
      </Routes>
    </Router>
  );
}

export default App;