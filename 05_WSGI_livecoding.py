import os
import csv
import json
from wsgiref.simple_server import make_server
import logging

# Настройка логгера
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()

# Создаем CSV-файл и записываем заголовки, если файл не существует
csv_file_path = 'data.csv'
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['name', 'city', 'age'])

def simple_app(environ, start_response):
    """Простое WSGI-приложение для обработки HTTP-запросов.

        Обрабатывает следующие пути:
        - '/' (GET): Возвращает приветственное сообщение.
        - '/goodbye' (GET): Возвращает прощальное сообщение.
        - '/info' (GET): Возвращает метод запроса.
        - '/get_people' (GET): Возвращает содержимое файла data.csv в формате JSON.
        - '/add_person' (POST): Добавляет новую запись в CSV-файл с данными из тела запроса в формате JSON.
        - Все другие пути: Возвращает ошибку 404 (Not Found).

        @param environ: Словарь с информацией о запросе (заголовки, параметры запроса и т.д.).
        @param start_response: Функция, которая должна быть вызвана для отправки ответа (статус и заголовки).
        @return: Итератор байтов, содержащий тело ответа.
    """
    request_method = environ.get('REQUEST_METHOD', 'GET')
    path = environ.get('PATH_INFO', '/')

    if path == '/':
        response_body = b"Hello, WSGI World!"
        status = '200 OK'

    elif path == '/get_people' and request_method == 'GET':
        with open(csv_file_path, 'r') as csvfile:
            people = list(csv.DictReader(csvfile))
        response_body = json.dumps(people).encode('utf-8')
        status = '200 OK'

    elif path == '/add_person' and request_method == 'POST':
        request_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
        data = json.loads(request_body.decode('utf-8'))
        with open(csv_file_path, 'a', newline='') as csvfile:
            csvwriter = csv.DictWriter(csvfile, fieldnames=['name', 'city', 'age'])
            csvwriter.writerow(data)
        response_body = b"Person added successfully!"
        status = '200 OK'

    else:
        response_body = b"Not Found"
        status = '404 Not Found'

    headers = [('Custom-Header', 'foo-bar')]
    start_response(status, headers)
    return [response_body]

# Запуск сервера
httpd = make_server('localhost', 9999, simple_app)
logger.info(f"Serving on  http://localhost:9999...")
httpd.serve_forever()
