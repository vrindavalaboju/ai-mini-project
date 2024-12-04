import React from 'react';
import { Card, CardContent, CardMedia, Typography, Grid } from '@mui/material';

const RecipeList = ({ recipes, onSelect }) => {
  return (
    <Grid container spacing={3} style={{ marginTop: 20 }}>
      {recipes.map((recipe) => (
        <Grid item xs={12} sm={6} md={4} key={recipe.id}>
          <Card 
            onClick={() => onSelect(recipe)} 
            style={{ cursor: 'pointer', height: '100%', borderRadius: '20px' }}
          >
            
            <CardContent>
              <Typography variant="h5" component="div">
                {recipe.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                {recipe.description}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default RecipeList;
