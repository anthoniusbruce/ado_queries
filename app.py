import flask
import adoapi
import cycle_time
import story_point_data
import cycle_time_jsonencoder
import story_point_data_jsonencoder
from flask_swagger_ui import get_swaggerui_blueprint

app = flask.Flask(__name__)
ado_base_route = "/ado_queries/api"
tfs_base_route = "/tfs_queries/api"

@app.route("/")
def index():
    return "Status: Up!"

@app.route(ado_base_route + "/v1.0/test", methods = ["POST"])
def get_test():
    querypath = flask.request.json["path"]
    token = flask.request.json["token"]
    history = adoapi.AdoApi.AdoGetTest(token, querypath)
    return flask.jsonify(history)
    
@app.route(tfs_base_route + "/v1.0/test", methods = ["POST"])
def get_tfs_test():
    querypath = flask.request.json["path"]
    token = flask.request.json["token"]
    history = adoapi.AdoApi.TfsGetTest(token, querypath)
    return flask.jsonify(history)
    
@app.route(ado_base_route+"/v1.0/workitem", methods=["POST"])
def get_workitem():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.AdoGetWorkItem(token, workitem)
    return flask.jsonify(response)

@app.route(ado_base_route+"/v1.0/history", methods=["POST"])
def get_history():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.AdoGetWorkItemHistory(token, workitem)
    return flask.jsonify(response)

@app.route(ado_base_route+"/v1.0/cycletime", methods=["POST"])
def get_cycle_time():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    result = adoapi.AdoApi.AdoGetCycleTimeFromUserStoryQuery(token, querypath)
    encoder = cycle_time_jsonencoder.CycleTimeJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ado_base_route+"/v1.0/atfstorypoints", methods=["POST"])
def get_aft_story_points():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    result = adoapi.AdoApi.AdoGetAtfStorySizeFromUserStoryQuery(token, querypath)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(tfs_base_route+"/v1.0/atfstorypoints", methods=["POST"])
def get_tfs_aft_story_points():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    result = adoapi.AdoApi.TfsGetAtfStorySizeFromUserStoryQuery(token, querypath)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(tfs_base_route+"/v1.0/workitem", methods=["POST"])
def get_tfs_workitem():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.TfsGetWorkItem(token, workitem)
    return flask.jsonify(response)

@app.route(tfs_base_route+"/v1.0/history", methods=["POST"])
def get_tfs_history():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.TfsGetWorkItemHistory(token, workitem)
    return flask.jsonify(response)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ado_queries"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

if (__name__ == "__main__"):
    app.run(debug=True)