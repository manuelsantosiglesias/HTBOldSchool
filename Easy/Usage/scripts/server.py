import os
import http.server
import socketserver
import io

PORT = 4433

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        content_type = self.headers['Content-Type']
        boundary = content_type.split("boundary=")[1].encode()
        parts = post_data.split(boundary)
        
        for part in parts:
            if b'Content-Disposition: form-data;' in part and b'filename="' in part:
                header, file_data = part.split(b'\r\n\r\n', 1)
                file_data = file_data.rsplit(b'\r\n', 1)[0]
                filename = header.split(b'filename="')[1].split(b'"')[0].decode()
                with open(os.path.join('.', filename), 'wb') as output_file:
                    output_file.write(file_data)
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Finalizado correctamente.")
                return
        
        self.send_response(400)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Subida fallida.")

Handler = CustomHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Funcionando en puerto {PORT}")
    httpd.serve_forever()
