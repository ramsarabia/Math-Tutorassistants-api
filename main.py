import openai
import os
import time

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create a client instance
client = openai.Client()

# Use the client to create an assistant
assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

# Create a thread
thread = client.beta.threads.create()
print(f"Thread created with ID: {thread.id}")

#ask user for input
user_input = input("Ask me an algebra problem, I bet I can answer it!")

# Add a message to the thread
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=user_input
)
print(f"Message added with ID: {message.id}")

# Create a run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
print(f"Run created with ID: {run.id}")

# Wait for the run to complete
while True:
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id,
    )
    if run_status.status == 'completed':
        print("Run completed.")
        break
    elif run_status.status == 'failed':
        print("Run failed.")
        break
    print("Waiting for run to complete...")
    time.sleep(1)  # Sleep for 1 second before checking again

# Retrieve all the messages inside of this run
messages = client.beta.threads.messages.list(
    thread_id=thread.id,
)

# Print all messages in the thread
for message in reversed(messages.data):
    # Adjust the way of accessing message content based on the actual structure of the message object
    print(f"{message.role}: {message.content}")