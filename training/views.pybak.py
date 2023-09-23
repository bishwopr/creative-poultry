from django.http import HttpResponse
from django.shortcuts import render
from gpt_index import GPTSimpleVectorIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader
from langchain.chat_models import ChatOpenAI
import os
from product.models import Product
import json

class CustomGPTSimpleVectorIndex(GPTSimpleVectorIndex):
    def register_document_types(self):
        self.register_document_type('list', ['text', 'doc_id', 'embedding', 'extra_info'])

def generate_training_data(request):
    products = Product.objects.all()

    training_data = []
    for product in products:
        training_data.append(product.to_json())

    # Save the training data to a file
    with open('training_data.txt', 'w') as file:
        file.write('\n'.join(training_data))

    return HttpResponse("Training data generated successfully.")

def create_index(request):
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

    # Get the absolute path of the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the relative path to the directory containing the training data
    training_data_directory = os.path.join(current_directory, 'data')

    # Load data from the training data directory
    documents = SimpleDirectoryReader(input_dir=training_data_directory).load_data()

    # Initialize the index
    index = CustomGPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return render(request, 'chatbot.html', {'message': 'Index created successfully'})

def ask_bot(request):
    if request.method == 'POST':
        query = request.POST['query']

        # Load the index
        index = GPTSimpleVectorIndex.load_from_disk('index.json')

        # Read the JSON file containing the product information
        with open('index.json', 'r') as file:
            products = file.readlines()

        # Search for products matching the query and extract their information
        matching_products = []
        for product in products:
            product_info = json.loads(product)
            if query.lower() in product_info.get('name', '').lower():
                matching_products.append(product_info)

        print("Matching Products:", matching_products)  # Debugging statement

        # Generate responses for the matching products
        responses = []
        for product in matching_products:
            response = index.query(product['name'], response_mode='complete')
            responses.append(response.response)

        # Concatenate all the responses into a single string
        concatenated_responses = "\n".join(responses)

        print("Concatenated Responses:", concatenated_responses)  # Debugging statement

        return render(request, 'chatbot.html', {'response': concatenated_responses})

    return render(request, 'chatbot.html')
