from flask import Flask, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    return render_template('dashboard.html', cpu_usage=cpu_usage, memory_info=memory_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
