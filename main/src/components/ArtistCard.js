import React from 'react';
import './ArtistCard.css';

const ArtistCard = ({ artist }) => (
  <div className="artist-card">
    <img src={artist.images[0]?.url} alt={artist.name} className="artist-image" />
    <span className="artist-name">{artist.name}</span>
  </div>
);

export default ArtistCard;