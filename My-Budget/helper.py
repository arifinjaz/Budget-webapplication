import os
import urllib.parse
import re
from flask import redirect, render_template, request, session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("userid"):
            print(session.get("userid"))
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function