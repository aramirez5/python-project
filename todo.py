from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Lista para almacenar las tareas
tasks = []
# Lista para almacenar los mensajes de error
error_messages = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks, error_messages=error_messages)

@app.route('/add', methods=['POST'])
def add():
    task = request.form['task']
    
    if task in tasks:
        error_messages.append(f'La tarea "{task}" ya existe.')
    else:
        tasks.append(task)
        success_message = f'Se agregó la tarea "{task}" correctamente.'
        error_messages.clear()
    return render_template('index.html', tasks=tasks, error_messages=error_messages, success_message=success_message)

@app.route('/delete', methods=['POST'])
def delete():
    task = request.form['task']
    
    success_message = None  # Inicializamos la variable success_message
    
    if task in tasks:
        tasks.remove(task)
        success_message = f'Se eliminó la tarea "{task}" correctamente.'
        error_messages.clear()
    else:
        error_messages.append(f'La tarea "{task}" no existe.')
    return render_template('index.html', tasks=tasks, error_messages=error_messages, success_message=success_message)

if __name__ == '__main__':
    app.run(debug=True)
