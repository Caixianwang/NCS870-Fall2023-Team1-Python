from flask import Flask  # 导入Flask类

app = Flask(__name__)
import threading

# Import customized libraries
# sys.path.append('./src')
from src.ver870.new_down_data import grap_main


@app.before_first_request
def activate_job():
    def run_job():
        grap_main()

    thread = threading.Thread(target=run_job)
    thread.start()


@app.route("/")
def hello():
    print("Hello World!")
    return "Hello World!"


if __name__ == "__main__":
    app.run(use_reloader=False)
