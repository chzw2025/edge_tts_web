from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import subprocess
import os
import time

PORT = 8000
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

class Handler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/tts":
            length = int(self.headers.get("Content-Length"))
            data = self.rfile.read(length)
            req = json.loads(data.decode())
            text = req.get("text", "")
            voice = req.get("voice", "zh-HK-HiuMaanNeural")

            filename = f"output_{int(time.time())}.mp3"
            filepath = os.path.join(OUTPUT_DIR, filename)

            cmd = [
                "python3", "-m", "edge_tts",
                "--voice", voice,
                "--text", text,
                "--write-media", filepath
            ]
            print(f"Running command: {' '.join(cmd)}")
            subprocess.run(cmd)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"path": f"/{OUTPUT_DIR}/{filename}"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404)

httpd = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"访问：http://localhost:{PORT}")
httpd.serve_forever()
