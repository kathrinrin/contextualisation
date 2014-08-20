#!/usr/local/bin/python2.7

from flask.ext.wtf import Form
from wtforms import SelectField, BooleanField, TextAreaField
from ConfigParser import ConfigParser

config = ConfigParser()

class MainForm(Form):
    datafromendpoint = BooleanField('datafromendpoint', default=True)
    query = TextAreaField('query')
    endpoints = SelectField('category', choices=[('Drugbank', 'Drugbank'),
                  ('Pubmed Publications', 'Pubmed Publications'),
#                   ('LinkedCT', 'LinkedCT'),
#                   ('Clinical Trials', 'Clinical Trials'),
                  ('DBPedia', 'DBPedia')], default='Drugbank')
