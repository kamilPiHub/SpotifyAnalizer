import React from 'react';
import './LoginPage.css';

const LoginPage = () => {
  const SPOTIFY_LOGIN_URL = "http://localhost:5000/login";

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