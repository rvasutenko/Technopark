from urllib.parse import parse_qs
from wsgiref.util import setup_testing_defaults


def application(environ, start_response):
    # Настраиваем окружение
    setup_testing_defaults(environ)

    # Получаем метод запроса
    method = environ['REQUEST_METHOD']

    # Получаем GET параметры
    query_string = environ.get('QUERY_STRING', '')
    get_params = parse_qs(query_string)

    # Получаем POST параметры (если есть)
    post_body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0))) if method == 'POST' else b''
    post_params = parse_qs(post_body.decode('utf-8'))

    # Формируем ответ
    response_body = f"""
        <html>
        <body>
            <h1>WSGI Parameters</h1>
            <h2>GET Parameters:</h2>
            <pre>{get_params}</pre>
            <h2>POST Parameters:</h2>
            <pre>{post_params}</pre>
        </body>
        </html>
    """
    response_body = response_body.encode('utf-8')

    # Устанавливаем HTTP-заголовки
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8'),
               ('Content-Length', str(len(response_body)))]
    start_response(status, headers)

    return [response_body]
