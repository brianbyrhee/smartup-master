from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/')
def student():
   return render_template('input.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      thing = request.form
      result = {}
      for key, value in thing.items():
          result[key] = value + "hi"
      return render_template("result.html",result = result)


if __name__ == '__main__':
   app.run(debug = True)
