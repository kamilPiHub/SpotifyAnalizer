import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [userData, setUserData] = useState(null);

  const handleLogin = async () => {
    try {
      const response = await axios.get('http://localhost:5000/login'); // Update URL if needed
      setUserData(response.data);
      setLoggedIn(true);
    } catch (error) {
      console.error('Error logging in:', error);
    }
  };

  return (
    <div>
      {loggedIn ? (
        <div>
          <h1>Welcome, {userData?.user_info?.display_name}</h1>
          <p>ID: {userData?.user_info?.id}</p>
          <p>URI: {userData?.user_info?.uri}</p>
          <a href={userData?.user_info?.profile_url}>Profile Link</a>
        </div>
      ) : (
        <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh",
        width: "100vw",
        backgroundColor: "#191414",
        color: "white",
      }}
    >
      <h1 style={{ fontSize: "3rem", marginBottom: "2rem" }}>
        Spotify Analyzer
      </h1>
      <p style={{ marginBottom: "2.5rem" }}>
        Zaloguj się, aby zobaczyć swoje statystyki.
      </p>
      <button
        onClick={handleLogin}
        style={{
          padding: "15px 30px",
          borderRadius: "50px",
          backgroundColor: "#1DB954",
          color: "white",
          border: "none",
          textDecoration: "none",
          fontWeight: "bold",
          fontSize: "1rem",
          cursor: "pointer",
        }}
      >
        ZALOGUJ SIĘ PRZEZ SPOTIFY
      </button>
    </div>
      )}
    </div>
  );
}

export default App;