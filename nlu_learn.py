
from __future__ import unicode_literals, print_function

import io
import json
import sys


from snips_nlu import SnipsNLUEngine, load_resources
from flask import Flask
from flask import request

app = Flask(__name__)

with io.open("dataset/data.json") as f:
    sample_dataset = json.load(f)

with io.open("configs/config_en.json") as f:
    config = json.load(f)

# text = sys.argv[1]

def parseResponse(responseText):
    response = json.loads(responseText)
    for slot in response['slots']:
        if slot['slotName'] == 'absDuration':
            slot['duration'] = slot['value']
            del slot['value']
    return response

def nluparse(text):
    load_resources(sample_dataset["language"])
    nlu_engine = SnipsNLUEngine(config=config)
    nlu_engine.fit(sample_dataset)

    # text = "Show me jobs in LA for today"
    parsing = nlu_engine.parse(text)
    return json.dumps(parsing, indent=2)

@app.route("/")
def start():
    nl_search = request.args.get('searchText')
    response_text = nluparse(nl_search)
    parsedData = parseResponse(response_text)
    # print(parsedData)
    return json.dumps(parsedData, indent=2)


if __name__ == '__main__':
    app.run(debug=True)
