from flask import render_template, url_for
from . import bp

@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.jinja', title='Avenger Assembler')