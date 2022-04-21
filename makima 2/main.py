#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import flask
import numpy as np
from flask import Flask, request

import search

app = Flask(__name__, static_folder="static", static_url_path="", template_folder="templates")


@app.route('/', methods=['GET'])
def root():
    r = request.args.get('arg')
    a = str(r)
    summary, eq, plot, eval = "", "", False, ""
    if r != None and a != "":
        # list = wikipedia.search(a)
        # web = str(wikipedia.page(a).links)
        # summary = str(list) + "\t" + wikipedia.summary(list[0], sentences=3)# += wikipedia.page().title# wikipedia.page(list[0]).title + "\n" + wikipedia.summary(list[0])
        eval, eq, plot, summary = search.main(a)  # str(N(sympify(a, locals=z._locals)))#str(sympify(parse_expr(a)))
        if eval == eq:
            eval = ""

    return flask.render_template(
        'index.html', phrase=a, summary=summary, eval=eval, latex=eq, plot = plot
    )

if __name__ == '__main__':
    app.run(debug=True)
