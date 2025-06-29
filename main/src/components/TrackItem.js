import React from 'react';
import './TrackItem.css';

const TrackItem = ({ track, index }) => (
  <div className="track-item">
    <span className="track-index">{index}.</span>
    <img src={track.album.images[0]?.url} alt={track.name} className="track-image" />
    <div className="track-info">
      <span className="track-name">{track.name}</span>
      <span className="track-artist">{track.artists.map(a => a.name).join(', ')}</span>
    </div>
  </div>
);

export default TrackItem;