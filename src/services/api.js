import axios from 'axios';

// Set up a base URL for your backend (adjust as needed)
axios.defaults.baseURL = 'http://localhost:5000'; // Replace with your backend URL

// Function to fetch recipes from the backend
// export const fetchRecipes = async (ingredients) => {
//   try {
//     const response = await axios.post('/api/recipes', { ingredients });
//     return response.data; // Assuming the backend returns an array of recipes
//   } catch (error) {
//     console.error('Error fetching recipes:', error);
//     return []; // Return an empty array on error
//   }
// };

export const fetchRecipes = async (ingredients) => {
    console.log('Mock API called with ingredients:', ingredients);
  
    // Simulate a delay for the API call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: 1,
            name: 'Tomato Basil Pasta',
            description: 'A delicious pasta kadlfkalsdkjflkshdlkfjhljsdhflkjhasldkfjhlakjshdflkjh akdjhflkajhsdlfkjhsldjfhl recipe with tomato and basil.',
            instructions: 'Cook pasta, make tomato sauce, mix together, and serve.'
          },
          {
            id: 2,
            name: 'Caprese Salad',
            description: 'Fresh salad with tomatoes, mozzarella, and basil.',
            instructions: 'Slice ingredients, layer them, and drizzle with olive oil.'
          },
        ]);
      }, 1000); // Simulate a 1-second delay
    });
  };