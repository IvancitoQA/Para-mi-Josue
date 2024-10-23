from flask import Flask, render_template, request, jsonify
import subprocess



app = Flask(_name_)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/edit')
def edit():
    return render_template('edit_template.html')

@app.route('/api/containers', methods=['POST'])
def create_container():
    container_name = request.json.get('name')
    if not container_name:
        return jsonify({"error": "El nombre del contenedor es requerido."}), 400

    try:
        subprocess.run(['docker-compose', 'up', '-d', container_name], check=True)
        return jsonify({"message": "Contenedor creado", "name": container_name}), 201
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"No se pudo crear el contenedor: {str(e)}"}), 500

@app.route('/api/containers/<name>', methods=['DELETE'])
def delete_container(name):
    try:
        subprocess.run(['docker-compose', 'down', name], check=True)
        return jsonify({"message": "Contenedor eliminado", "name": name}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"No se pudo eliminar el contenedor: {str(e)}"}), 500

if _name_ == '_main_':
    app.run(debug=True)
