# This is the file that implements a flask server to do inferences. It's the file that you will modify to
# implement the scoring for your own algorithm.

from __future__ import print_function

import os
import json
import pickle
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from io import StringIO    
import sys
import signal
import traceback

import flask

import pandas as pd

prefix = '/opt/ml/'
model_path = os.path.join(prefix, 'model')

# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.

class ScoringService(object):
    model = None                # Where we keep the model when it's loaded
    @classmethod
    def deterministic_pred(cls,some_list):
        a = some_list[0]
        b = some_list[1]
        c = some_list[2]
        if (len(some_list)==0):
            output = 'EMPTY LIST. Check Data Parser'
        elif(a == 0 and b == 0):
            if(c==0):
                output = 'ALL_NONE'
            else:
                output = 'AB_NONE'

        elif(a == 1 and b == 1):
            if(c==0):
                output = 'C_NONE'
            else:
                output = 'ALL_YES'
        else:
            output = 'PARTIAL_YES'

        return(output) 
    
# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    """Determine if the container is working and healthy. In this sample container, we declare
    it healthy if we can load the model successfully."""
    health = ScoringService.deterministic_pred([0,0,0]) is not None  # You can insert a health check here

    status = 200 if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/invocations', methods=['POST'])
def transformation():
    """Do an inference on a single batch of data. In this sample server, we take data as CSV, convert
    it to a pandas data frame for internal use and then convert the predictions back to CSV (which really
    just means one prediction per line, since there's a single column.
    """
    data = None
    data_list = []
    # Convert from CSV to pandas
    if flask.request.content_type == 'text/csv':        
        pl = (flask.request.get_data().decode("utf-8"))        
        data_list = json.loads(pl)
               
    else:
        pl = flask.request.get_data().decode("utf-8")
        Message_to_return = 'Payload: {}. This predictor only supports list data'.format(pl)
        return flask.Response(response=Message_to_return, status=415, mimetype='text/plain')
        #return flask.Response(response='This predictor only supports JSON data with key as "somekey"', status=415, mimetype='text/plain')

    print('Parsed JSON payload to get list:',data_list)

    # Do the prediction
    predictions = ScoringService.deterministic_pred(data_list)

    # Convert from numpy back to CSV
    #out = StringIO.StringIO()
    #pd.DataFrame({'results':predictions}).to_csv(out, header=False, index=False)
    #result = out.getvalue()

    return flask.Response(response=predictions, status=200, mimetype='text/csv')