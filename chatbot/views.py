from django.http import HttpResponse
from django.shortcuts import render
from gpt_index import GPTSimpleVectorIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader
import os
from product.models import Product

os.environ["OPENAI_API_KEY"] = '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'

class CustomGPTSimpleVectorIndex(GPTSimpleVectorIndex):
    def register_document_types(self):
        self.register_document_type('list', ['text', 'doc_id', 'embedding', 'extra_info'])

def generate_training_data(request):
    products = Product.objects.all()

    training_data = []
    for product in products:
        training_data.append(product.to_json())

    # Save the training data to a file in the base folder
    training_data_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'training_data.txt')

    with open(training_data_filepath, 'w') as file:
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
    llm_predictor = LLMPredictor()

    # Load data from the training data file
    training_data_filepath = os.path.join('E:\\poultry_ready\\creative-poultry-main\\', 'training_data.txt')
    documents = SimpleDirectoryReader(input_dir=os.path.dirname(os.path.abspath(__file__))).__load_data_from_file__(training_data_filepath)

    # Initialize the index
    index = CustomGPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    # Save the index to disk in the base folder
    index_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.json')
    index.save_to_disk(index_filepath)

    return render(request, 'chatbot.html', {'message': 'Index created successfully'})



from django.http import JsonResponse
def ask_bot(request):
    if request.method == 'POST':
        query = request.POST['msg']
        print('------------------------------------------>')
        print(query)
        index_filepath = os.path.join('E:\\poultry_ready\\creative-poultry-main\\', 'index.json')
        print(index_filepath)
        index = GPTSimpleVectorIndex.load_from_disk(index_filepath)
        response = index.query(query, response_mode="compact")
        resp_data = response.response
        print(resp_data)
        # return None
        return JsonResponse({'response':resp_data})






# def ask_bot(request):
#     if request.method == 'POST':
#         query = request.POST['query']
#         index_filepath = os.path.join('E:\\poultry_ready\\creative-poultry-main\\', 'index.json')
#         index = GPTVectorStoreIndex.load_from_disk(index_filepath)
#         response = index.query(query, response_mode="compact")

#         # Retrieve the chat history from the session
#         chat_history = request.session.get('chat_history', [])

#         # Add the current query and response to the chat history
#         chat_history.append({'user': 'You', 'message': query})
#         chat_history.append({'user': 'Chatbot', 'message': response.response})

#         # Store the updated chat history in the session
#         request.session['chat_history'] = chat_history

#         return render(request, 'chatbot.html', {'response': response.response, 'chat_history': chat_history})

#     # Retrieve the chat history from the session
#     chat_history = request.session.get('chat_history', [])

#     return render(request, 'chatbot.html', {'chat_history': chat_history})
