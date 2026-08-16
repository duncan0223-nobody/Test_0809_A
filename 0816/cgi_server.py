#!/home/pi/Documents/github/Test_0809_A/.venv/bin/python3
# -*- coding: utf-8 -*-
"""單執行緒 CGI 伺服器(避免多執行緒 fork 死鎖)"""
import os
import sys
from http.server import HTTPServer, CGIHTTPRequestHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8000


class QuietHandler(CGIHTTPRequestHandler):
    pass


def main():
    os.chdir(BASE_DIR)
    server = HTTPServer(("0.0.0.0", PORT), QuietHandler)
    print(f"CGI 伺服器啟動於 http://0.0.0.0:{PORT}  (Ctrl+C 停止)")
    print(f"網址:http://<本機IP>:{PORT}/cgi-bin/id_check.py")
    server.serve_forever()


if __name__ == "__main__":
    main()
