from flask import Blueprint, render_template, request, url_for, flash, session, redirect
from flask_login import login_required, current_user, login_user
from models.measurement import Measurement

measurements_blueprint = Blueprint('measurements',
                            __name__,
                            template_folder='templates')