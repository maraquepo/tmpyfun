from flask import Flask, render_template

app = Flask(__name__)

@app.get('/')
def home():
  return "Hello, World!"
