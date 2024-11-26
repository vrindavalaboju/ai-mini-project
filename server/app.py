#!/usr/bin/env python
import os
import pandas as pd
import faiss
import requests
import numpy as np
import openai
from openai import OpenAI
from openai.types import CreateEmbeddingResponse
import time

# Load dataset
recipes_df = pd.read_csv("shortened_recipes.csv")  # Ensure it has an "ingredients" column

def textual_representation(row):
    textual_representation=f"""Recipe: {row['name']}
Cook time: {row['minutes']} minutes
Description: {row['description']}
Ingredients: {row['ingredients']}
"""
    return textual_representation



#test printing
print(recipes_df.iloc[:5].apply(textual_representation, axis=1).values[0])

#Save the textual representation as a column in the dataset
recipes_df["textual_representation"]=recipes_df.apply(textual_representation, axis=1)

#OpenAI API configs
os.environ['OPENAI_API_KEY']='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'
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)
index_file='index'
dim = 1536 #embedding dimension as returned by llama2
index = faiss.IndexFlatL2(dim)
batch_size = 50 #number of recipes to read in per batch

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

if os.path.exists(index_file):
    print("Index file exists, reading...")
    index=faiss.read_index('index')
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
    faiss.write_index(index, 'index')
    print(f"Index loaded with {index.ntotal} entries.")

    #check that the number of embeddings are the same as the number of recipes
    print(f"Number of embeddings in index: {index.ntotal}")
    print(f"Number of recipes: {len(recipes_df)}")
    if index.ntotal==len(recipes_df):
        print("All recipes are embedded correctly!")
    else:
        print(f"Some embeddings are missing! ({len(recipes_df)-index.ntotal} missing)")

