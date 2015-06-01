# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for, Response

# Import needed classes
from app.helpers.functions import *
from config import CHIVO_URL

import urllib
import re
#Creating objects
chivoReg = ChivoRegistry()

# Define the blueprint: 'services'
alias = Blueprint('services', __name__)

@alias.route('cycle0fits/q/siap-cycle0-fits/<param>'):
def alias(param):
	return redirect(CHIVO_URL+"/alma/tap/"+param)
	
