from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get current file path
            current_file = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_file)

            # List files in current directory
            files_in_api = []
            if os.path.exists(current_dir):
                files_in_api = os.listdir(current_dir)

            # Check if main.py exists
            main_py_path = os.path.join(current_dir, 'main.py')
            main_py_exists = os.path.exists(main_py_path)
            main_py_size = os.path.getsize(main_py_path) if main_py_exists else 0

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            message = json.dumps({
                'status': 'ok',
                'current_file': current_file,
                'current_dir': current_dir,
                'files_in_api_dir': sorted(files_in_api),
                'main_py_path': main_py_path,
                'main_py_exists': main_py_exists,
                'main_py_size': main_py_size,
                'path': self.path
            }, indent=2)

            self.wfile.write(message.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            message = json.dumps({
                'status': 'error',
                'message': str(e),
                'path': self.path
            })
            self.wfile.write(message.encode())
        return
