from http.server import BaseHTTPRequestHandler 
from urllib import parse
import requests 
import json


class handler(BaseHTTPRequestHandler):
    """ A simple HTTP request handler that fetches trivia questions."""

    def do_GET(self):
        """ Handles GET requests."""

        # Extracting query parameters from the request URL
        url_component = parse.urlsplit(self.path)
        query_params = dict(parse.parse_qsl(url_component.query))

        # Base URL for the trivia API
        base_url = "https://opentdb.com/api.php"

        # List to store fetched questions
        questions = []

        # Counter for question numbering
        question_count = 1

        # Handling the special case for category ID 33
        if 'category' in query_params and int(query_params['category']) == 33:
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            response_msg = "You have just 32 category.\n\n"
            self.wfile.write(response_msg.encode())
            return

        # Handling the 'amount' parameter
        elif 'amount' in query_params: 
            try:
                amount = int(query_params['amount'])
                if amount > 50:
                    amount = 50

                # Fetching questions from the API
                response = requests.get(f"{base_url}?amount={amount}")
                data = response.json()

                # Checking if 'result' key exists in the response
                if 'results' in data:
                    # Including amount in the response
                    questions.append(f"Amount: {amount}\n\n")

                    # Parsing the response and formatting questions
                    for q in data['results']:
                        question = q['question']
                        correct_answer = q['correct_answer']
                        questions.append(f"{question_count}. {question} - {correct_answer}\n\n")
                        question_count += 1  


            except ValueError:
                # Handling invalid amount parameter
                self.send_error(400, "Invalid amount parameter")
                return
            
        elif 'category' in query_params:
            try:
                category = int(query_params['category'])
                # Fetching category data from the API
                response = requests.get("https://opentdb.com/api_category.php")
                categories = response.json()['trivia_categories']

                category_name = next((c['name'] for c in categories if c['id'] == category), "")
                if category_name:
                    # Fetching questions based on category
                    response = requests.get(f"{base_url}?amount=10&category={category}")
                    data = response.json()
                    
                    # Checking if 'results' key exists in the response
                    if 'results' in data:
                        # Including category name in the response
                        questions.append(f"Category: {category_name}\n\n")

                        # Parsing the response and formatting questions
                        for q in data['results']:
                            question = q['question']
                            correct_answer = q['correct_answer']
                            questions.append(f"{question_count}. {question} - {correct_answer}\n\n")
                            question_count += 1  
                    else:
                        questions.append("No questions found for this category.")
                
            except ValueError:
                # Handling invalid category parameter
                self.send_error(400, "Invalid category parameter")
                return
            
        elif url_component.path == "/api/questions":
            # Handling requests to /api/questions without any query parameters
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Welcome to the trivia API!")
            return
            
        else:
            # Handling missing required parameters
            self.send_error(400, "Missing required parameters")
            return
        
        # sending the response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        
        if questions:
            response_msg = "\n".join(questions)
            self.wfile.write(response_msg.encode())
        else:
            self.wfile.write(b"No questions found")


        return