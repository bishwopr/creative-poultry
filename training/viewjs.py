import json
from django.http import HttpResponse
from django.shortcuts import render
from gpt_index import GPTSimpleVectorIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI
import os
from product.models import Product
import csv
import ast

class CustomGPTSimpleVectorIndex(GPTSimpleVectorIndex):
    def register_document_types(self):
        self.register_document_type('list', ['text', 'doc_id', 'embedding', 'extra_info'])

def train_and_create_index(request):
    # Generate training data
    products = Product.objects.all()

    # Save the training data to a CSV file
    filepath = "./training_data.csv"
    with open(filepath, 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "title", "ingredients", "directions", "link", "source", "ner"])
        for product in products:
            writer.writerow([product.id, product.title, product.ingredients, product.directions, product.link, product.source, product.ner])

    # Process the dataset
    training_data = []
    with open(filepath, encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)
        for idx, row in enumerate(csv_reader):
            if idx == 0:
                continue
            training_data.append({
                "text": row[1],
                "extra_info": {
                    "id": row[0],
                    "ingredients": ast.literal_eval(row[2]),
                    "directions": ast.literal_eval(row[3]),
                    "link": row[4],
                    "source": row[5],
                    "ner": ast.literal_eval(row[6]),
                }
            })

    # Set maximum input size
    max_input_size = 4096
    # Set number of output tokens
    num_outputs = 256
    # Set maximum chunk overlap
    max_chunk_overlap = 20
    # Set chunk size limit
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    # Define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    # Initialize the index
    index = CustomGPTSimpleVectorIndex(training_data, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return HttpResponse("Training data generated and index created successfully.")
