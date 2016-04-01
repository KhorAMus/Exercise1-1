reference_map = {
    """/about/aboutme.html""": """C:\\Users\\khoramus\\Desktop\\web\\Exercise1-1\\myproject\\about\\aboutme.html""",
    '''/index.html''': '''C:\\Users\\khoramus\\Desktop\\web\\Exercise1-1\\myproject\\index.html''',
    '''/''': '''C:\\Users\\khoramus\\Desktop\\web\\Exercise1-1\\myproject\\index.html'''
}


def app(environ, start_response):

    path_info = environ["PATH_INFO"]
    if path_info in reference_map.keys():
        status = '200 OK'
        response_headers = [('Content-type', 'text/html')]
        start_response(status, response_headers)
        full_path = reference_map[path_info]
        html_file = open(full_path, 'rb')
        file_lines = html_file.readlines()
        html_file.close()
        return file_lines
    else:
        status = '404 Page not found'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return ["Запрашиваемая страница не найдена :(".encode("utf-8")]


class TestMiddleware(object):
    def __init__(self, my_application):
        self.app = my_application

    def __call__(self, environ, start_response):
        top_str = "    <div class='top'>Middleware TOP</div>\n".encode()
        bottom_str = "    <div class='bottom'>Middleware BOTTOM</div>\n".encode()
        body_open_bstr = "<body>".encode('utf-8')
        body_close_bstr = "</body>".encode('utf-8')

        for line in self.app(environ, start_response):

            if line.find(body_open_bstr) != -1:
                yield line
                yield top_str
            elif line.find(body_close_bstr) != -1:
                yield bottom_str
                yield line
            else:
                yield line


app = TestMiddleware(app)

if __name__ == '__main__':
    from paste import reloader
    from paste.httpserver import serve

    reloader.install()
    serve(app, host='localhost', port=8000)
