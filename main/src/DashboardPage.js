// Plik: frontend/src/Dashboard.js
import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [profile, setProfile] = useState(null);
  // ... inne stany ...

  useEffect(() => {
    const fetchData = async () => {
      // Pobieramy token z localStorage
      const accessToken = localStorage.getItem('spotify_access_token');

      if (!accessToken) {
        // Jeśli nie ma tokenu, przekieruj do logowania
        window.location.href = '/';
        return;
      }
      
      // Tworzymy nagłówek autoryzacyjny
      const headers = {
        'Authorization': `Bearer ${accessToken}`
      };

      try {
        // Wykonujemy zapytania z ręcznie dodanym nagłówkiem
        const profileRes = await fetch('/api/profile', { headers });
        if (!profileRes.ok) throw new Error('Błąd pobierania profilu');
        const profileData = await profileRes.json();
        setProfile(profileData);
        // ... (pobieranie top-tracks w ten sam sposób)
      } catch (error) {
        console.error(error);
        // Tutaj powinna być logika odświeżania tokenu, jeśli wystąpił błąd 401
      }
    };

    fetchData();
  }, []);

  // ... (reszta kodu do wyświetlania danych, podobnie jak wcześniej) ...

  const handleLogout = () => {
    // Wylogowanie w tym modelu to po prostu wyczyszczenie localStorage
    localStorage.removeItem('spotify_access_token');
    localStorage.removeItem('spotify_refresh_token');
    localStorage.removeItem('spotify_token_expires_in');
    window.location.href = '/';
  };

  if (!profile) return <div>Ładowanie...</div>;

  return (
    <div>
      <h1>Witaj, {profile.display_name}</h1>
      <button onClick={handleLogout}>Wyloguj</button>
      {/* ... wyświetlanie reszty danych ... */}
    </div>
  );
};

export default Dashboard;