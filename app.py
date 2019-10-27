import flask
import adoapi

app = flask.Flask(__name__)
base_route = "/ado_queries/api"

@app.route("/")
def index():
    return "Status: Up!"

@app.route(base_route + "/v1.0/test", methods = ["POST"])
def get_onbalance_story_and_task_history():
    querypath = flask.request.json["path"]
    token = flask.request.json["token"]
    history = adoapi.AdoApi.GetTest(token, querypath)
    return flask.jsonify(history)
    
@app.route(base_route+"/v1.0/workitem", methods=["POST"])
def get_workitem():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.GetWorkItem(token, workitem)
    return flask.jsonify(response)

@app.route(base_route+"/v1.0/history", methods=["POST"])
def get_history():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.GetWorkItemHistory(token, workitem)
    return flask.jsonify(response)

if (__name__ == "__main__"):
    app.run(debug=True)