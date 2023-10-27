# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie as cookie  
from networking import mac_from_ip
from urllib.parse import parse_qs

import routes
from game import Game


game = Game()

hostName = "killyourfriends.party"
serverPort = 80

static = {
    "/static/styles.css": "text/css",
    "/static/bg.jpg": "image/jpeg",
    "/static/rules.html": "text/html",
}

get_handlers = {
    "/": routes.get_homepage,
    "/shell": routes.get_admin_shell,
}

post_handlers = {
    "/add": routes.post_add_player,
    "/kill": routes.post_record_kill,
    "/start": routes.post_start_game,
    "/end": routes.post_end_game,
    "/remove": routes.post_admin_remove,
    "/reroll": routes.post_admin_reroll,
    "/shell": routes.post_admin_shell,
}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path in get_handlers:
                self.ok()
                get_handlers[self.path](self, game, mac_from_ip(self.client_address[0]))
            elif self.path in static:
                self.send_response(200)
                self.send_header('Content-type', static[self.path])
                self.end_headers()
                with open(self.path[1:], "rb") as f:
                    self.wfile.write((f.read()))
            else:
                self.send_response(302)
                self.send_header('Location', "/")
                self.end_headers()
        except ConnectionAbortedError as e:
            print("Oh no")
        

    def do_POST(self):
        try:
            length = int(self.headers['content-length'])
            postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
            postvars = { key.decode(): vals[0].decode() for key, vals in postvars.items() }
            print("POST", self.path, postvars)
            if self.path in post_handlers:
                self.ok()
                post_handlers[self.path](self, game, mac_from_ip(self.client_address[0]), postvars)
            else:
                self.send_response(302)
                self.send_header('Location', "/")
                self.end_headers()
        except ConnectionAbortedError as e:
            print("Oh no")

    def ok(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<head><link rel=stylesheet href=/static/styles.css></head>", "utf-8"))



if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")