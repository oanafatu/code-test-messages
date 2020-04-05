from src import app


def start_local_server():
    app.run(debug=True)


if __name__ == '__main__':
    start_local_server()
