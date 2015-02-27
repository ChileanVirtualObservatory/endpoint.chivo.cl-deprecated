#import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

# Import needed classes
from app.helpers.functions import *

#Creating objects
chivoReg = ChivoRegistry()

# Define the blueprint: 'services'
registry = Blueprint('registry', __name__)


@registry.route('/registry/oai.xml')
def reg():
	return "it works"
