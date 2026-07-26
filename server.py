# Bloque de importaciones con manejo de dependencia principal.
try:
    # try to import flask, or return error if has not been installed
    from flask import Flask
    from flask import send_from_directory
except ImportError:
    print("You don't have Flask installed, run `$ pip3 install flask` and try again")
    exit(1)

import os, subprocess

# Configuracion de rutas estaticas y creacion de la aplicacion Flask.
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), './')
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #disable cache

# Ruta principal: sirve app.py (si existe) o index.html como pagina inicial.
@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    if os.path.exists("app.py"):
        # Si existe app.py, se ejecuta y se devuelve su salida renderizada.
        out = subprocess.Popen(['python3','app.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        return stdout if out.returncode == 0 else f"<pre style='color: red;'>{stdout.decode('utf-8')}</pre>"
    if os.path.exists("index.html"):
        # Si no hay app.py, se devuelve el index estatico.
        return send_from_directory(static_file_dir, 'index.html')
    else:
        # Mensaje de error amigable cuando falta el archivo principal.
        return "<h1 align='center'>404</h1><h2 align='center'>Missing index.html file</h2><p align='center'><img src='https://github.com/4GeeksAcademy/html-hello/blob/main/.vscode/rigo-baby.jpeg?raw=true' /></p>"

# Ruta comodin: sirve cualquier archivo estatico solicitado por URL.
@app.route('/<path:path>', methods=['GET'])
def serve_any_other_file(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        # Si el path es un directorio, intenta resolver su index.html.
        path = os.path.join(path, 'index.html')
    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0 # avoid cache memory
    return response

# Arranque del servidor de desarrollo con escucha global en el puerto 3000.
app.run(host='0.0.0.0',port=3000, debug=True, extra_files=['./',])
