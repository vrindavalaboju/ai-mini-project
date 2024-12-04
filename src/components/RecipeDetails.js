import React from 'react';

const RecipeDetails = ({ recipe, onClose }) => (
  <div>
    <h2>{recipe.name}</h2>
    <p>{recipe.instructions}</p>
    <button onClick={onClose}>Close</button>
  </div>
);

export default RecipeDetails;
