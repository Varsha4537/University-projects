import React, { useState } from 'react';
import axios from 'axios';
import './CatPicture.css';  // For styling

const CatPicture = () => {
  const [catImageUrl, setCatImageUrl] = useState('');

  const fetchCatPicture = () => {
    axios
      .get('https://api.thecatapi.com/v1/images/search')
      .then(response => {
        setCatImageUrl(response.data[0].url);
      })
      .catch(error => {
        console.error('Error fetching the cat picture:', error);
      });
  };

  return (
    <div className="cat-container">
      <h1>Get a Random Cat Picture</h1>
      <button className="cat-button" onClick={fetchCatPicture}>
        Show Me a Cat!
      </button>
      {catImageUrl && <img className="cat-image" src={catImageUrl} alt="A cute cat" />}
    </div>
  );
};

export default CatPicture;
