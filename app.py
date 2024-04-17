from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def metodo_euler(f, x0, y0, h, iteraciones, solucion_exacta=None):
    puntos_x = [x0]
    puntos_y = [y0]
    errores = []
    for i in range(iteraciones):
        y_nueva = y0 + h * f(x0, y0)
        x0, y0 = x0 + h, y_nueva
        puntos_x.append(x0)
        puntos_y.append(y_nueva)
        if solucion_exacta:
            error_actual = abs(solucion_exacta(x0) - y_nueva) / abs(solucion_exacta(x0)) * 100 if solucion_exacta(x0) != 0 else 0
            errores.append(error_actual)
        else:
            errores.append(None)  # Asegurarse de mantener la longitud de la lista de errores igual a la de puntos_x y puntos_y
    return puntos_x, puntos_y, errores

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            f = eval('lambda x, y: ' + request.form['funcion'])
            x0 = float(request.form['x0'])
            y0 = float(request.form['y0'])
            h = float(request.form['h'])
            iteraciones = int(request.form['iteraciones'])
            solucion_exacta = eval('lambda x: ' + request.form['solucion_exacta']) if request.form.get('solucion_exacta') else None

            xs, ys, errores = metodo_euler(f, x0, y0, h, iteraciones, solucion_exacta)
            puntos = list(zip(xs, ys, errores))

            plot_url = create_plot(xs, ys)
            solucion_exacta_provided = bool(request.form.get('solucion_exacta'))
            return render_template('resultado.html', plot_url=plot_url, puntos=puntos, solucion_exacta_provided=solucion_exacta_provided)
        except Exception as e:
            return f"Ocurrió un error: {e}"
    return render_template('index.html')

def create_plot(xs, ys):
    plt.figure()
    plt.plot(xs, ys, '-o', label='Aproximación Euler')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url

if __name__ == '__main__':
    app.run(debug=True)
