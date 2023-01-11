import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


is_loading = False

@app.route("/", methods=("GET", "POST"))
def index():
    global is_loading
    input_text=''
    instruction_text=''
    if request.method == "POST":
        is_loading = True # Show loading
        input_text = request.form["input"]
        instruction_text = request.form["instruction"]
        try:
            response = openai.Edit.create(
                model="text-davinci-edit-001",
                input=input_text,
                instruction = instruction_text,
                temperature=0.6,
            )
            result = response.choices[0].text
        except openai.exceptions.OpenAiError as e:
            result = str(e)        
        is_loading = False # Hide loading
        return redirect(url_for("index", result=result, input_text=input_text, instruction_text=instruction_text))    
    result = request.args.get("result")
    input_text = request.args.get("input_text")
    instruction_text = request.args.get("instruction_text")
    return render_template("index.html", result=result, is_loading=is_loading)


