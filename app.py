from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def start():
    return render_template('start.html')

# Ruta para la página principal donde se muestran los síntomas
@app.route('/sintomas')
def index():
    # Cargar el archivo CSV
    df = pd.read_csv('enfermedades.csv', encoding='utf-8')

    # Crear un conjunto para almacenar todos los síntomas únicos
    sintomas = set()

    # Iterar sobre cada fila del CSV y agregar los síntomas al conjunto
    for index, row in df.iterrows():
        sintomas.add(row['sintoma1'])
        sintomas.add(row['sintoma2'])
        sintomas.add(row['sintoma3'])

    # Convertir el conjunto a lista y ordenar los síntomas alfabéticamente
    sintomas = sorted(list(sintomas))

    # Renderizar la plantilla con los síntomas
    return render_template('index.html', sintomas=sintomas)

# Ruta para procesar los síntomas seleccionados y mostrar el diagnóstico
@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    sintomas_seleccionados = request.form.getlist('sintomas')
    
    # Verificar si no se ha seleccionado ningún síntoma
    if not sintomas_seleccionados:
        enfermedad_diagnostico = "No seleccionaste ningún síntoma"
        consejo = "Por favor, selecciona al menos un síntoma para continuar con el diagnóstico."
        return render_template('resultado.html', enfermedad=enfermedad_diagnostico, consejo=consejo)

    # Cargar la base de datos de enfermedades
    df = pd.read_csv('enfermedades.csv', encoding='utf-8', on_bad_lines='skip')
    
    # Lista para almacenar posibles diagnósticos
    posibles_diagnosticos = []

    # Buscar coincidencias de síntomas
    for index, row in df.iterrows():
        # Recolectar los síntomas de la enfermedad actual
        sintomas_enfermedad = [row['sintoma1'], row['sintoma2'], row['sintoma3']]
        
        # Calcular cuántos síntomas seleccionados coinciden con esta enfermedad
        coincidencias = len(set(sintomas_seleccionados) & set(sintomas_enfermedad))
        
        if coincidencias > 0:  # Si hay al menos una coincidencia
            posibles_diagnosticos.append({
                'enfermedad': row['enfermedad'],
                'coincidencias': coincidencias,
                'consejo': row['consejo']
            })
    
    # Ordenar las enfermedades por mayor número de coincidencias
    posibles_diagnosticos = sorted(posibles_diagnosticos, key=lambda d: d['coincidencias'], reverse=True)
    
    # Si no hay coincidencias
    if not posibles_diagnosticos:
        enfermedad_diagnostico = "No se pudo determinar un diagnóstico"
        consejo = "Por favor, consulte a un médico para una evaluación más precisa."
        return render_template('resultado.html', enfermedad=enfermedad_diagnostico, consejo=consejo)
    
    # Solo mostrar el diagnóstico con más coincidencias (el primero en la lista)
    mejor_diagnostico = posibles_diagnosticos[0]

    return render_template('resultado.html', diagnosticos=[mejor_diagnostico])
                           
if __name__ == '__main__':
    app.run(debug=True)
