import os
import json
from flask import Flask, render_template, url_for, request, redirect, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from subprocess import call


server = Flask(__name__)

server.config["IMAGE_UPLOADS"] = "./uploads"

@server.route('/')
def hello():
	return jsonify({"response": "Hello from Docker!"})

@server.route('/upload', methods=['GET','POST'])
def upload():
	if request.method == 'POST':
		imagemFile = request.files["imagem"]
		larguraValue = request.form["largura"]
		alturaValue = request.form["altura"]
		imagemFile.save(os.path.join(server.config["IMAGE_UPLOADS"], imagemFile.filename))

		call("python3 alturaPasto.py --i ./uploads/"+imagemFile.filename+" --p ./images_results/"+imagemFile.filename+" --l "+larguraValue+" --a "+alturaValue, shell=True)
			
		try:
			return send_from_directory("./images_results", imagemFile.filename, as_attachment=True)
				
		except:
			return jsonify({"response": "Erro"})
	
	else:
		return jsonify({"response": "Erro"})


if __name__ == '__main__':
	server.run(debug=True, host='0.0.0.0', port=5000)
