from flask import(
    Blueprint, g, flash, url_for, redirect, render_template, request
)
from werkzeug.exceptions import abort

from inventory.auth import login_required
from inventory.db import get_db

bp = Blueprint('blog', __name__)