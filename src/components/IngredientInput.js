import React, { useState } from 'react';
import SearchIcon from '@mui/icons-material/Search';


const IngredientInput = ({ onSearch }) => {
  const [ingredients, setIngredients] = useState('');

  const handleSearch = () => {
    if (ingredients.trim()) {
      onSearch(ingredients.split(',').map(ing => ing.trim()));
    }
  };

  return (
    <div className="search-container">
      <input
        className="search-bar"
        type="text"
        placeholder="Enter ingredients, e.g., tomato, basil"
        value={ingredients}
        onChange={(e) => setIngredients(e.target.value)}
      />
      <button className="circular-button" onClick={handleSearch}>
        <SearchIcon className="search-icon" />
      </button>
    </div>
  );
};

export default IngredientInput;
