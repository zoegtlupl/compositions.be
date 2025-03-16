import os
import sys
from app import app


sys.path.insert(0, os.path.dirname(__file__))


def application(environ, start_response):
    return app(environ,start_response)
    
if __name__ == "__main__":
    app.run(port=5000)

