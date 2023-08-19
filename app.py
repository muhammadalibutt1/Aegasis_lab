from flask import Flask, request, jsonify
import openai

class ChatGPTBotAPI:
    def __init__(self, api_key, model="text-davinci-003"):
        self.api_key = api_key
        self.model = model
        openai.api_key = self.api_key
    
    def initialize_gpt3(self):
        # No need to explicitly initialize the API here since we've set the API key in the constructor
        pass
    
    def create_prompt(self, prompt):
        # Store the user-provided prompt for later interactions
        self.prompt = prompt
    
    def get_response(self, prompt_index):
        if hasattr(self, "prompt"):
            response = openai.Completion.create(
                engine=self.model,
                prompt=self.prompt,
                max_tokens=50
            )
            return response.choices[0].text
        else:
            return "No prompt available."
    
    def update_prompt(self, prompt_index, new_prompt):
        if hasattr(self, "prompt"):
            self.prompt = new_prompt
            return "Prompt updated successfully."
        else:
            return "No prompt available."

app = Flask(__name__)
bot = ChatGPTBotAPI(api_key="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")

@app.route('/', methods=['GET'])
def initialize():
    bot.initialize_gpt3()
    return "GPT-3 initialized."

@app.route('/create_prompt', methods=['GET'])
def create_prompt():
    data = request.get_json()
    prompt = data.get('prompt')
    bot.create_prompt(prompt)
    return "Prompt created successfully."

@app.route('/get_response/<int:prompt_index>', methods=['GET'])
def get_response(prompt_index):
    response = bot.get_response(prompt_index)
    return jsonify({"response": response})

@app.route('/update_prompt/<int:prompt_index>', methods=['PUT'])
def update_prompt(prompt_index):
    data = request.get_json()
    new_prompt = data.get('new_prompt')
    result = bot.update_prompt(prompt_index, new_prompt)
    return result

@app.route('/delete_prompt/<int:prompt_index>', methods=['DELETE'])
def delete_prompt(prompt_index):
    bot.delete_prompt(prompt_index)
    return jsonify({"message": "Prompt deleted successfully."})


if __name__ == '__main__':
    app.run(debug=True)
