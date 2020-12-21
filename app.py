from flask import Flask, render_template, request
import parser as fl
app = Flask(__name__)
@app.route('/')
def student():
   return render_template('input.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      thing = request.form
      # a
      result = {}
      for key, value in thing.items():
         ret_val = fl.Parser(value)
      avg_cost, avg_success, expected_cat = ret_val.get_values()
      # store avg cost and avg success in a dictionary
      result = {}
      result["Expected Category"] = expected_cat
      result["Average Project Goal For Category (USD)"] = avg_cost
      result["Chance of Success based on prior projects(%)"] = avg_success
      return render_template("result.html",result = result)


if __name__ == '__main__':
   app.run(debug = True)
