import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const AuthCallback = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    // Pobieramy parametry z adresu URL
    const params = new URLSearchParams(location.search);
    const accessToken = params.get('access_token');
    const refreshToken = params.get('refresh_token');
    const expiresIn = params.get('expires_in');

    if (accessToken) {
      // Obliczamy czas wygaśnięcia i zapisujemy wszystko w localStorage
      const expirationTime = new Date().getTime() + expiresIn * 1000;
      localStorage.setItem('spotify_access_token', accessToken);
      localStorage.setItem('spotify_refresh_token', refreshToken);
      localStorage.setItem('spotify_token_expires_in', expirationTime);
      
      // Przekierowujemy na główny panel
      navigate('/dashboard');
    } else {
      // Jeśli nie ma tokenu, wracamy do logowania
      navigate('/');
    }
  }, [location, navigate]);

  return <div>Przetwarzanie autoryzacji...</div>;
};

export default AuthCallback;