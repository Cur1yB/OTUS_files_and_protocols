# Запуск сервера с помощью wsgiref
from wsgiref.simple_server import make_server


def simple_app(environ, start_response):
    '''Простое WSGI-приложение.
    
        @param environ: Словарь с информацией о запросе (заголовки, параметры запроса и т.д.).
        @param start_response: Функция, которая должна быть вызвана для отправки ответа (статус и заголовки).
        @return: Итератор байтов, содержащий тело ответа.'''
    # Статус ответа
    status = '200 OK'
    # Заголовки ответа
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    # Начало ответа
    start_response(status, headers)

    body = "Hello, WSGI World!"

    bytes_body = body.encode()
    # Тело ответа
    return [bytes_body] 
""" Почему возвращается байтовая строка?

WSGI-приложения возвращают тело ответа в виде итератора байтов (не строк), потому что:

1. HTTP передает данные в виде байтов, а не Unicode-строк.
2. Это обеспечивает совместимость с разными серверами.
3. Текст нужно преобразовать в байты (например, с помощью UTF-8), чтобы сервер мог корректно передать его клиенту.

Пример: строка b"Hello, WSGI World!" — это закодированное байтовое представление текста, необходимое для передачи по HTTP.

Альтернативный способ: используйте метод encode(), чтобы преобразовать обычную строку в байты:
response_body = "Hello, WSGI World!".encode('utf-8')
"""


# Создание WSGI-сервера
httpd = make_server('localhost', 8051, simple_app)
print("Serving on port 8051...")

# Запуск сервера
httpd.serve_forever()

'''Далее преходите через браузер на адрес http://localhost:8051/'''
