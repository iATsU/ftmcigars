import os
import pandas as pd
import flask
from flask import request, jsonify
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)
#app.config["DEBUG"] = True


data = pd.read_excel('final.xlsx', usecols=['Background', 'Wrapper', 'Band', 'Ash', 'Ashtray'])

cigars = []

for row in data.itertuples(index=True, name='Pandas'):
    meta = {
        'name': f'FTM Cigar #{row.Index}',
        'external_url': 'https://ftmcigars.xyz/',
        'ID': row.Index,
        'image': f'https://ftmcyberpunks.com/cigar/art/{row.Index}.png',
        'attributes': [
            {'trait_type':'Background', 'value':row.Background},
            {'trait_type':'Wrapper', 'value':row.Wrapper},
            {'trait_type':'Band', 'value':row.Band},
            {'trait_type':'Ash', 'value':row.Ash},
            {'trait_type':'Ashtray', 'value':row.Ashtray}
        ]
    }
    
    cigars.append(meta)

@app.route('/api/cigarsMeta', methods=['GET'])
def api_index():
    # Check if an index was provided as part of the URL.
    # If index is provided, assign it to a variable.
    # If no index is provided, display an error in the browser.
    if 'index' in request.args:
        index = int(request.args['index'])
    else:
        return "Error: Please provide a valid token ID"

    # Create an empty list for our results
    #results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    if 0<=index<200:
        for cigar in cigars:
            if cigar['ID'] == index:
                result = cigar
    else:
        result = 'null'

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)