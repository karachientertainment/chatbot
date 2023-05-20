import os
from flask import Flask, request
import openai

app = Flask(__name__)
openai.api_key = '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'

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Facebook Messenger webhook verification
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if verify_token == 'EAALg7qtKXSMBAMYQ174ce1ZBLBNexKmDUZCx29EZC2jsFObnCljBvKXLKrqNPWGciiCbIgZBSMqoctgW396sAfym39YdhZAb82uQOLYXdPUOn84FxOkduAZCSn3QKKj0v7HRHaFqcmZCO8Ti6yxe6Y1Dh5JggCfyUoZAwZBEF8Yi37LVBDvNTZCZC8OzNGo9qzYPz9SIKK1w17TNgZDZD':
            return challenge
        return "Invalid verification token"
    elif request.method == 'POST':
        # Handle incoming messages from Facebook Messenger
        data = request.json
        message = data['entry'][0]['messaging'][0]['message']['text']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']

        # Generate a response using OpenAI API
        response = generate_response(message)

        # Send the response back to the user
        send_message(sender_id, response)

        return "OK"

def generate_response(message):
    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def send_message(recipient_id, message):
    # Send a message to the user using Facebook Messenger API
    # Implement your own code here to send the message

if __name__ == '__main__':
    app.run()
