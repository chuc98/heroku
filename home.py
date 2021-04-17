from os import name
from flask import Flask, render_template, request, json, url_for, redirect,send_from_directory, g, session
import os
#from PyPDF2 import PdfFileReader
from werkzeug.utils import secure_filename
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

import time
import re
import jinja2
import ctypes
app = Flask(__name__)

@app.route("/")
def index():
  
   return render_template("./index.html")

@app.route("/mapa")
def Visualizar():

   return render_template("./geo.html")




if __name__ == "__main__":
    app.run()   
