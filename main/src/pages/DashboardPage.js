import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './DashboardPage.css';
import TrackItem from '../components/TrackItem';
import ArtistCard from '../components/ArtistCard';

const apiClient = axios.create({
  baseURL: "http://localhost:5000",
  withCredentials: true,
});

const DashboardPage = () => {
  const [user, setUser] = useState(null);
  const [topTracks, setTopTracks] = useState([]);
  const [topArtists, setTopArtists] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [userRes, tracksRes, artistsRes] = await Promise.all([
          apiClient.get('/api/profile'),
          apiClient.get('/api/top-tracks?limit=10'),
          apiClient.get('/api/top-artists?limit=10'),
        ]);

        setUser(userRes.data);
        setTopTracks(tracksRes.data.items);
        setTopArtists(artistsRes.data.items);
      } catch (error) {
        console.error("Błąd podczas pobierania danych:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  if (loading) {
    return <div className="loading">Ładowanie danych...</div>;
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>{user ? `Witaj, ${user.display_name}!` : 'Witaj!'}</h1>
        <p>Oto Twoje podsumowanie Spotify.</p>
        <button onClick={handleLogout} className="logout-button">Wyloguj</button>
      </header>

      <div className="data-section">
        <section>
          <h2>Twoje Top 10 Utworów</h2>
          <div className="track-list">
            {topTracks.map((track, index) => (
              <TrackItem key={track.id} track={track} index={index + 1} />
            ))}
          </div>
        </section>
        
        <section>
          <h2>Twoi Top 10 Artyści</h2>
          <div className="artist-grid">
            {topArtists.map((artist) => (
              <ArtistCard key={artist.id} artist={artist} />
            ))}
          </div>
        </section>
      </div>
    </div>
  );
};

export default DashboardPage;