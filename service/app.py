#!flask/bin/python
from flask import Flask, jsonify,request

app = Flask(__name__)

#load model and a confirgation object
# for now we are globally loading these files, once we have enough scale even these will be turned into api calls
#config objects would be stored in a dict , and the api call will also have to pass the trading symbol name and type

#'http://localhost/refresh?time=88'
@app.route('/refresh', methods=['GET'])
def refresh_data():
    time = request.args.get('time',type=int)
    # get historical data and update local pandas frame
    return jsonify({'status': 'success'})

@app.route('/infer', methods=['GET'])
def refresh_infer():
    time = request.args.get('time',type=int)
    # get historical data , update local pandas frame and infer th model
    return jsonify({'status': 'success'})


if __name__ == '__main__':
    app.run(debug=True)