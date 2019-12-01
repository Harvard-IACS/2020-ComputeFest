import http.server
import socketserver
from http import HTTPStatus
import requests
import sys

class Handler(http.server.SimpleHTTPRequestHandler):


    def do_GET(self):
        self.send_response(HTTPStatus.OK);
        self.end_headers();

        # determine what the URL for the database should be
        if(len(sys.argv) == 2):
            db_url = sys.argv[1];
        else:
            db_url = 'http://localhost:8081/'; # set default url for database

        try:
	        # response = requests.get('http://localhost:8081/', timeout=2.50);
            response = requests.get(db_url, timeout=2.50);
            if(response.ok): # check if status_code is 200 or less, which indicates succeessful response
                self.wfile.write(response.text.encode('ascii'));
            else:
                print(db_url)
                print(response.text);
                raise Exception();
        except Exception as e:
            print(e);
            self.wfile.write(b'Could not connect to database.');


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