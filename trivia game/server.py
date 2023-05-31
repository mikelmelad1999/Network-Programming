import socket
import threading
import time

# Predefined set of trivia questions
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Rome", "Madrid"],
        "correct_answer": "1"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["Pablo Picasso", "Vincent van Gogh", "Michelangelo","Leonardo da Vinci"],
        "correct_answer": "4"
    },
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["Saturn", "Neptune","Jupiter", "Mars"],
        "correct_answer": "3"
    },
    {
        "question": "55+110= ?",
        "options": ["165", "111", "206","164"],
        "correct_answer": "1"
    },
]

# List to store clients and their aliases
clients = []
aliases = []

# Locks for synchronization
answer_count = 0
results = {}  # Dictionary to store client results

# Function to handle client connections
def handle_client(client_socket):
    global answer_count

    while True:
        try:
            # Receive client's answer
            answer = client_socket.recv(1024).decode().strip()

            # Evaluate the answer
            evaluate_answer(client_socket, answer)

            # Wait until all clients have answered
            answer_count += 1
            if answer_count == len(clients):
                answer_count = 0
                time.sleep(2)  # Wait for 2 seconds before sending the next question
                if len(questions) > 0:
                    broadcast_question()
                else:
                    print_results_to_clients()
        except:
            # Client disconnected
            clients.remove(client_socket)
            client_socket.close()
            break

# Function to evaluate the client's answer
def evaluate_answer(client_socket, answer):
    question = current_question["question"]
    correct_answer = current_question["correct_answer"]

    response_time = time.time() - question_start_time

    if answer.lower() == correct_answer.lower():
        client_socket.send("Correct!".encode())
        print(f"Player {aliases[clients.index(client_socket)]} answered correctly in {response_time:.2f} seconds.")
        results[client_socket] = results.get(client_socket, 0) + 1
    else:
        client_socket.send("Incorrect!".encode())
        print(f"Player {aliases[clients.index(client_socket)]} answered incorrectly.")

# Function to broadcast the question to all connected clients
def broadcast_question():
    global current_question, question_start_time

    current_question = questions.pop(0)  # Remove the first question from the list

    question_start_time = time.time()

    question = current_question["question"]
    options = "\n".join(f"{i + 1}. {option}" for i, option in enumerate(current_question["options"]))

    message = f"{question}\n{options}\n"
    for client_socket in clients:
        client_socket.send(message.encode())

    print("Question broadcasted.")

# Function to print the results for all clients
def print_results_to_clients():
    global results

    message = "--- Results ---\n"

    for client_socket, score in results.items():
        alias = aliases[clients.index(client_socket)]
        message += f"{alias}: Score: {score}\n"

    message += "---------------\n"

    for client_socket in clients:
        client_socket.send(message.encode())

    print("Results broadcasted to clients.")

# Function to start the server
def start_server():
    host = '127.0.0.1'  # Server IP address
    port = 55555       # Server port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server started. Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()

        client_socket.send(''.encode('utf-8'))

        alias = client_socket.recv(1024).decode()

        aliases.append(alias)
        clients.append(client_socket)

        threading.Thread(target=handle_client, args=(client_socket,)).start()

        if len(clients) == 2:
            broadcast_question()  # Start with the first question

# Start the server
start_server()
