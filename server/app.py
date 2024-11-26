#!/usr/bin/env python
import os
import pandas as pd
import faiss
import numpy as np
from openai import OpenAI
from flask import Flask, request, jsonify

app=Flask(__name__)
# Load dataset
recipes_df = pd.read_csv("shortened_recipes.csv")  # Ensure it has an "ingredients" column

def textual_representation(row):
    textual_representation=f"""Recipe: {row['name']}
Cook time: {row['minutes']} minutes
Description: {row['description']}
Ingredients: {row['ingredients']}
"""
    return textual_representation

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data=request.json
        if not data or "ingredients" not in data:
            return jsonify({"error": "Invalid input. 'ingredients' field is required."})

        # Generate embedding for user input
        ingredients=data["ingredients"]
        user_embedding = get_embedding(ingredients).reshape(1, -1)

        # Query Faiss index
        distances, indices = index.search(user_embedding, 5)  # Retrieve top 5 results

        # Fetch matching recipes
        matching_recipes = recipes_df.iloc[indices[0]].to_dict(orient="records")

        return jsonify({"recipes": matching_recipes})
    except Exception as e:
        return jsonify({"error":f"An error occurred: {str(e)}"}),500


#test printing
print(recipes_df.iloc[:5].apply(textual_representation, axis=1).values[0])

#Save the textual representation as a column in the dataset
recipes_df["textual_representation"]=recipes_df.apply(textual_representation, axis=1)

#OpenAI API configs
os.environ['OPENAI_API_KEY']='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'
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)
index_file='index.faiss'
dim = 1536 #embedding dimension as returned by OpenAi
index = faiss.IndexFlatL2(dim)
batch_size = 50 #number of recipes to read in per batch

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   response=client.embeddings.create(input = [text], model=model)
   return np.array(response.data[0].embedding, dtype="float32")

if os.path.exists(index_file):
    print("Index file exists, reading...")
    index=faiss.read_index('index.faiss')
else:
    print("Index not found, creating...")

    # Initialize Faiss index
    index=faiss.IndexFlatL2(dim)
    X = np.zeros((len(recipes_df), dim), dtype='float32')

    for i in range(0, len(recipes_df), batch_size):
        batch=recipes_df.iloc[i:i+batch_size]
        embeddings=[]

        for j, text in enumerate(batch["textual_representation"]):
            try:
                #getting the embeddings from OpenAI
                embedding=get_embedding(text, model="text-embedding-3-small")
                embeddings.append(embedding)

            except Exception as e:
                print(f"Error fetching embedding for recipe {i + j}: {e}")
        if embeddings:
            embeddings_np=np.array(embeddings, dtype="float32")
            index.add(embeddings_np)
            print(f"Batch{i// batch_size+1} processed and added to index.")

    # save the index
    print("Saving index")
    faiss.write_index(index, 'index.faiss')
    print(f"Index loaded with {index.ntotal} entries.")

    #check that the number of embeddings are the same as the number of recipes
    print(f"Number of embeddings in index: {index.ntotal}")
    print(f"Number of recipes: {len(recipes_df)}")
    if index.ntotal==len(recipes_df):
        print("All recipes are embedded correctly!")
    else:
        print(f"Some embeddings are missing! ({len(recipes_df)-index.ntotal} missing)")
    
    index=faiss.read_index("index.faiss")
    

# Start Flask server
if __name__ == '__main__':
    app.run(debug=True)