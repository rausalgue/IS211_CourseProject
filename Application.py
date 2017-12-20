#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignemnt Week 13 - Flask App"""

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import re
import sqlite3 as lite
from contextlib import closing

DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)



if __name__ == '__main__':
    app.run()