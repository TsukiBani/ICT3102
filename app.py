from distutils.log import debug
from website import create_app

from typing import List, Dict
from flask import Flask
import mysql.connector
import json

app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
