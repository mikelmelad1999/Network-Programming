import socket
import threading
import tkinter as tk

# Create a Tkinter GUI window
window = tk.Tk()
window.title("Trivia Game")
window.geometry("400x200")

# Create a label to display the question
question_label = tk.Label(window, text="question", wraplength=350)
question_label.pack()

# Create an entry field for the answer
answer_entry = tk.Entry(window)
answer_entry.pack()

# Function to handle receiving and displaying server messages
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            question_label.config(text=message)  # Update the question label
        except:
            # Server disconnected
            client_socket.close()
            break

# Function to send the client's answer to the server
def send_answer(client_socket):
    def submit_answer():
        answer = answer_entry.get()
        client_socket.send(answer.encode())
        answer_entry.delete(0, tk.END)  # Clear the answer entry field

    submit_button = tk.Button(window, text="Submit", command=submit_answer)
    submit_button.pack()


# Function to start the client
def start_client():
    alias = input('Choose an alias >>> ')
    host = '127.0.0.1'  # Server IP address
    port = 55555       # Server port

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(alias.encode('utf-8'))
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    threading.Thread(target=send_answer, args=(client_socket,)).start()

    # Start the GUI main loop
    window.mainloop()

# Start the client
start_client()
