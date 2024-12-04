#!/usr/bin/env python
import os
import pandas as pd
import faiss
import numpy as np
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import time

app = Flask(__name__)
"""
To test, first launch app.py:
./app.py

Then use a curl command:
curl -X POST http://127.0.0.1:5000/recommend \
-H "Content-Type: application/json" \
-d '{"ingredients": "spinach", "tags": "vegan"}'
"""

# Load dataset
recipes_df = pd.read_csv("shortened_recipes.csv")  # Ensure it has a "tags" column

# Add textual representation including tags
def textual_representation(row):
    tags = row.get("tags", "no tags available")
    return f"""Recipe: {row['name']}
Cook time: {row['minutes']} minutes
Description: {row['description']}
Ingredients: {row['ingredients']}
Tags: {tags}
"""

# Generate textual representation
recipes_df["textual_representation"] = recipes_df.apply(textual_representation, axis=1)

# OpenAI API configs
os.environ['OPENAI_API_KEY'] = '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'
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
EMBEDDING_MODEL = "text-embedding-3-small"

# Load or create Faiss index
index_file = 'index.faiss'
dim = 1536  # Embedding dimension
index = faiss.IndexFlatL2(dim)

if os.path.exists(index_file):
    print("Index file exists, reading...")
    index = faiss.read_index(index_file)
else:
    print("Index not found, creating...")
    index = faiss.IndexFlatL2(dim)
    embeddings = np.zeros((len(recipes_df), dim), dtype="float32")

    for i, text in enumerate(recipes_df["textual_representation"]):
        try:
            embedding = client.embeddings.create(input=[text], model=EMBEDDING_MODEL).data[0].embedding
            embeddings[i] = np.array(embedding, dtype="float32")
        except Exception as e:
            print(f"Error fetching embedding for recipe {i}: {e}")

    index.add(embeddings)
    faiss.write_index(index, index_file)
    print(f"Index saved with {index.ntotal} entries.")

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        # Parse the input JSON
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input. JSON payload is required."}), 400

        ingredients = data.get("ingredients", "")
        tags = data.get("tags", "")

        # Create a descriptive query prompt to improve embeddings
        query_prompt = f"Find a recipe that includes: {ingredients}"
        if tags:
            query_prompt += f" and matches the tags: {tags}"

        # Generate embedding for user input
        user_embedding = np.array(
            client.embeddings.create(input=[query_prompt], model=EMBEDDING_MODEL).data[0].embedding,
            dtype="float32"
        ).reshape(1, -1)

        # Query Faiss index for top 5 similar recipes
        distances, indices = index.search(user_embedding, 5)

        # Check if any matches were found
        if indices[0][0] == -1:
            return jsonify({"message": "No matching recipes found."}), 404

        # Fetch matching recipes
        matching_recipes = recipes_df.iloc[indices[0]].to_dict(orient="records")

        # Filter results by tags if tags are specified
        if tags:
            filtered_recipes = [recipe for recipe in matching_recipes if all(tag in recipe["tags"] for tag in tags.split(","))]
        else:
            filtered_recipes = matching_recipes

        # Extract recipe names and details
        results = [
            {"name": recipe["name"], "distance": float(dist), "details": recipe}
            for recipe, dist in zip(filtered_recipes, distances[0])
        ]

        return jsonify({
            "recipes": results,
            "recipe_names": [recipe["name"] for recipe in filtered_recipes]
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



if __name__ == '__main__':
    app.run(debug=True)
