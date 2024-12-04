import React, { useState } from 'react';
import IngredientInput from './components/IngredientInput';
import RecipeList from './components/RecipeList';
import RecipeDetails from './components/RecipeDetails';
import { fetchRecipes } from './services/api';
import MealsAILogo from './assets/MealsAIBG.png';


const App = () => {
  const [recipes, setRecipes] = useState([]);
  const [selectedRecipe, setSelectedRecipe] = useState(null);

  const handleSearch = async (ingredients) => {
    const results = await fetchRecipes(ingredients);
    setRecipes(results);
  };

  return (
    <div>
      <div className='logo-cont'>
        <img 
          src={MealsAILogo}  
          alt="Recipe Recommendation System Logo" 
          style={{ maxWidth: '300px', height: 'auto', marginBottom: '10px'}}
        />
        <IngredientInput onSearch={handleSearch} />
      </div>
      <div>
        <RecipeList recipes={recipes} onSelect={setSelectedRecipe} />
        {selectedRecipe && (
          <RecipeDetails recipe={selectedRecipe} onClose={() => setSelectedRecipe(null)} />
        )}
      </div>
    </div>

  );
};

export default App;
