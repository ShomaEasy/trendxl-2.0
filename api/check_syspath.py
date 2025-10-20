from http.server import BaseHTTPRequestHandler
import json
import sys
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get current file path
            current_file = os.path.abspath(__file__)
            current_dir = os.path.dirname(current_file)

            # Try to import main
            import_error = None
            import_success = False
            try:
                # Try direct import
                import main
                import_success = True
            except Exception as e:
                import_error = str(e)

            # Try sys.path modification
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)

            import_error_after_path_fix = None
            import_success_after_path_fix = False
            try:
                import main
                import_success_after_path_fix = True
            except Exception as e:
                import_error_after_path_fix = str(e)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            message = json.dumps({
                'status': 'ok',
                'current_file': current_file,
                'current_dir': current_dir,
                'sys_path': sys.path,
                'import_success_before': import_success,
                'import_error_before': import_error,
                'import_success_after_path_fix': import_success_after_path_fix,
                'import_error_after_path_fix': import_error_after_path_fix,
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
