"""Demo app para el flujo GitOps: edita COLOR, VERSION o MESSAGE y haz push."""
import http.server
import socket

VERSION = "1.1.0"
COLOR = "#7c3aed"
MESSAGE = "Hola equipo! Desplegado por ArgoCD"

PAGE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<title>argocd-demo {version}</title>
<style>
  body {{
    margin: 0; height: 100vh; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: .5rem;
    background: {color}; color: #fff;
    font-family: system-ui, sans-serif; text-align: center;
  }}
  h1 {{ font-size: 3rem; margin: 0; }}
  .badge {{
    background: rgba(0,0,0,.3); padding: .4rem 1rem;
    border-radius: 999px; font-size: 1.1rem;
  }}
</style>
</head>
<body>
  <h1>{message}</h1>
  <div class="badge">version {version}</div>
  <div class="badge">pod: {hostname}</div>
</body>
</html>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = PAGE.format(
            version=VERSION,
            color=COLOR,
            message=MESSAGE,
            hostname=socket.gethostname(),
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # cierra la conexion para que cada refresco pueda caer en otro pod
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("", 8080), Handler).serve_forever()
