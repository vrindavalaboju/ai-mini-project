import React from 'react';
import { Card, CardContent, CardMedia, Typography, Grid } from '@mui/material';
import { Chip } from '@mui/material';


const RecipeList = ({ recipes, onSelect }) => {
  return (
    <Grid container spacing={3} style={{ marginTop: 20 }}>
      {recipes.map((recipe) => (
        <Grid item xs={12} sm={6} md={4} key={recipe.id}>
          <Card 
            onClick={() => onSelect(recipe)} 
            style={{ cursor: 'pointer', height: '100%', borderRadius: '20px', backgroundColor: '#cbd5c0',
              color: '#0A5C36' }}
          >
            
            <CardContent>
              <Typography variant="h5" component="div">
                {recipe.name}
              </Typography>
              <Typography variant="body2" color="text.secondary" style={{color: '#344e41'}}>
                <em>
                {recipe.details.description}
                </em>
              
              <br />
              <br />
              <strong>Ingredients: </strong> 
                {recipe.details.ingredients
                  .replace(/[\[\]']/g, '') // Remove square brackets and single quotes
                  .trim()}
              <br />
              <br />
              <strong>Steps:</strong> {recipe.details.steps
                .replace(/[\[\]']/g, '') // Remove brackets and quotes
                .replace(/,\s*/g, '\n') // Replace commas with line breaks
                .trim()} 
              <br />
              <br />
              <strong>Tags:</strong>
                <div>
                  {recipe.details.tags.replace(/[\[\]']/g, '').replace(/,\s*/g, ',').trim().split(',').map((tag, index) => (
                    <Chip
                      key={index}
                      label={tag.trim()}
                      style={{
                        margin: '2px',
                        backgroundColor: 'rgba(58, 90, 64, 0.55)', // Sage green with 80% opacity
                        color: '#DAD7CD', // Off-white text
                        borderRadius: '16px', // Rounded corners
                      }}
                    />
                  ))}
                </div>
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default RecipeList;
