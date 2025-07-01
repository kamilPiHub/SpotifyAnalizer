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
        <div>
          <h1>Not logged in</h1>
          <button onClick={handleLogin}>Login with Spotify</button>
        </div>
      )}
    </div>
  );
}

export default App;