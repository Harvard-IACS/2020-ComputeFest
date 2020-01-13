import http.server
import socketserver
from http import HTTPStatus
import requests
import sys
import numpy as np
import array

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(HTTPStatus.OK);
        self.end_headers();

        hello_list = ['Hello world!', 'Hola mundo!', 'Da jia hao!', 'Bonjour monde!',
    'Namaste duniya!', "Hallo welt!"];
        # get random phrase from list
        hello_phrase = np.random.choice(a=hello_list, size=1)[0];
        self.wfile.write(hello_phrase.encode('ascii'));


PORT_NUMBER = 8080;
        
try:
    #Create a web server and define the handler to manage the incoming request
    httpd = socketserver.TCPServer(('', PORT_NUMBER), Handler);
    print("Created HTTP server");
    print("Please go to http://localhost:{0}/".format(PORT_NUMBER) );
    print("Press ^C to shut down.");
    
    httpd.serve_forever(); # Wait forever for incoming http requests 

except KeyboardInterrupt:
    print('^C received, shutting down the web server');
    httpd.socket.close();