from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
#import quandl
import json
import requests
import pandas
from pandas import *
import bokeh
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from datetime import datetime

#quandl.ApiConfig.api_key 
qakey = 'gJCP3YaHM38A6tRTRpSD'

#DEBUG = True     # new
app = Flask(__name__)
app.config.from_object(__name__)    # new
app.config['SECRET_KEY'] = '314159265358979'

url_p = "https://www.quandl.com/api/v3/datasets/WIKI/"
url_j = "/data.json"
par_s = "&api_key=" + qakey + "&start_date=" #quandl.ApiConfig.api_key + "&start_date="
par_m = "&end_date="
par_e = "&order=asc"
date1 = '2012-06-01'
date2 = '2017-06-01'

# new
class ReusableForm(Form):
  name = TextField('Stock Symbol:', validators=[validators.required()])
# end new

def create_figure(ssymb,search_r):
  search_data = search_r.json()
  df = DataFrame(search_data)
  df2 = DataFrame(df['dataset_data']['data'],columns = df['dataset_data']['column_names'])
  dts = pandas.to_datetime(df2['Date'])
  dt1 = dts[0].isoformat()[0:10]
  dt2 = dts[len(dts)-1].isoformat()[0:10]
  dtstr = dt1 + ' to ' + dt2

  datause = 'Close'
  p1 = figure(x_axis_type='datetime', title='Stock Closing Prices ' + dtstr)
  p1.grid.grid_line_alpha = 0.3
  p1.xaxis.axis_label = 'Date'
  p1.yaxis.axis_label = 'Closing Price'
  p1.line(pandas.to_datetime(df2['Date']),df2[datause])

  datause = 'Open'
  p2 = figure(x_axis_type='datetime', title='Stock Opening Prices ' + dtstr)
  p2.grid.grid_line_alpha = 0.3
  p2.xaxis.axis_label = 'Date'
  p2.yaxis.axis_label = 'Opening Price'
  p2.line(pandas.to_datetime(df2['Date']),df2[datause])

  datause = 'Adj. Open'
  p3 = figure(x_axis_type='datetime', title='Stock Adjusted Opening Prices ' + dtstr)
  p3.grid.grid_line_alpha = 0.3
  p3.xaxis.axis_label = 'Date'
  p3.yaxis.axis_label = 'Adj. Opening Price'
  p3.line(pandas.to_datetime(df2['Date']),df2[datause])

  datause = 'Adj. Close'
  p4 = figure(x_axis_type='datetime', title='Stock Adjsuted Closing Prices ' + dtstr)
  p4.grid.grid_line_alpha = 0.3
  p4.xaxis.axis_label = 'Date'
  p4.yaxis.axis_label = 'Adj. Closing Price'
  p4.line(pandas.to_datetime(df2['Date']),df2[datause])

  gridp = gridplot([[p2, p1],[p3, p4]])
  return gridp

@app.route("/", methods=['GET','POST'])    # added methods
def main():
  form = ReusableForm(request.form)

  script = ''
  div = ''
  name = None
  print form.errors
  if request.method == 'POST':
    stckfnd = False
    name = request.form['name']
    print name
    if form.validate():
      search_url = url_p + name + url_j
      search_par = par_s + date1 + par_m + date2 + par_e
      search_r = requests.get(search_url,params=search_par)
      stckfnd = (search_r.status_code == requests.codes.ok)
      if stckfnd:
        plt = create_figure(name,search_r)
        script, div = components(plt)
      else:
        script = 'Invalid stock symbol'
        div = ''
    else:
      flash('Enter stock symbol ')

  if name == None:
    script = ''
    div = ''

  return render_template('stock_plots.html',script=script, div=div, name=name, form=form)

# commented out the following
#  return redirect('/index')
#@app.route('/index')
#def index():

if __name__ == '__main__':
  app.run(port=33507)
#  app.run(host='0.0.0.0')
