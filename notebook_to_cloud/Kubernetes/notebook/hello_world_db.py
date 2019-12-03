import http.server
import socketserver
from http import HTTPStatus
import numpy as np

class Handler(http.server.SimpleHTTPRequestHandler):
    
    hello_list = ['Hello world!', 'Hola mundo!', 'Da jia hao!', 'Bonjour monde!',
    'Namaste duniya!', "Hallo welt!"];

    def do_GET(self):
        self.send_response(HTTPStatus.OK);
        self.end_headers();

        # get random phrase from list
        hello_phrase = np.random.choice(a=Handler.hello_list, size=1)[0];

        self.wfile.write(hello_phrase.encode('ascii'));

PORT_NUMBER = 8081;
        
try:
    #Create a web server and define the handler to manage the incoming request
    httpd = socketserver.TCPServer(('', PORT_NUMBER), Handler);
    print("Created HTTP server to run our database.");
    print("Press ^C to shut down.");
    
    httpd.serve_forever(); # Wait forever for incoming http requests 

except KeyboardInterrupt:
    print('^C received, shutting down the database.');
    httpd.socket.close();