import React, { useEffect } from 'react';
import './LoginPage.css';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const SPOTIFY_LOGIN_URL = "http://127.0.0.1:8081/login";
  const { isAuthenticated, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, isLoading, navigate]);

  return (
    <div className="login-container">
      <h1>Witaj w Spotify Analyzer</h1>
      <p>Zobacz swoje spersonalizowane statystyki Spotify.</p>
      <a href={SPOTIFY_LOGIN_URL} className="login-button">
        Zaloguj się przez Spotify
      </a>
    </div>
  );
};

export default LoginPage;