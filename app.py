import flask
import adoapi
import cycle_time
import story_point_data
import cycle_time_jsonencoder
import story_point_data_jsonencoder
from flask_swagger_ui import get_swaggerui_blueprint

app = flask.Flask(__name__)
ADO_BASE_ROUTE = "/ado_queries/api"
ADO_DEFAULT_ROUTE = "/ado_default_queries/api"
tfs_base_route = "/tfs_queries/api"

@app.route("/")
def index():
    return "Status: Up!"

@app.route(ADO_BASE_ROUTE + "/v1.0/test", methods = ["POST"])
def get_test():
    querypath = flask.request.json["path"]
    token = flask.request.json["token"]
    project = flask.request.json["project"]
    org = flask.request.json["org"]
    history = adoapi.AdoApi.AdoGetTest(token, querypath, project, org)
    return flask.jsonify(history)
    
@app.route(tfs_base_route + "/v1.0/test", methods = ["POST"])
def get_tfs_test():
    querypath = flask.request.json["path"]
    token = flask.request.json["token"]
    project = flask.request.json["project"]
    history = adoapi.AdoApi.TfsGetTest(token, querypath, project)
    return flask.jsonify(history)
    
@app.route(ADO_BASE_ROUTE+"/v1.0/workitem", methods=["POST"])
def get_workitem():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    org = flask.request.json["org"]
    response = adoapi.AdoApi.AdoGetWorkItem(token, workitem, org)
    return flask.jsonify(response)

@app.route(ADO_BASE_ROUTE+"/v1.0/history", methods=["POST"])
def get_history():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    org = flask.request.json["org"]
    response = adoapi.AdoApi.AdoGetWorkItemHistory(token, workitem, org)
    return flask.jsonify(response)

@app.route(ADO_BASE_ROUTE+"/v1.0/cycletime", methods=["POST"])
def get_cycle_time():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    org = flask.request.json["org"]
    result = adoapi.AdoApi.AdoGetCycleTimeFromUserStoryQuery(token, querypath, project, org)
    encoder = cycle_time_jsonencoder.CycleTimeJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_BASE_ROUTE+"/v1.0/atfstorypoints", methods=["POST"])
def get_aft_story_points():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    org = flask.request.json["org"]
    result = adoapi.AdoApi.AdoGetAtfStorySizeFromUserStoryQuery(token, querypath, project, org)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(tfs_base_route+"/v1.0/atfstorypoints", methods=["POST"])
def get_tfs_aft_story_points():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    result = adoapi.AdoApi.TfsGetAtfStorySizeFromUserStoryQuery(token, querypath, project)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_BASE_ROUTE+"/v1.0/atfvelocity", methods=["POST"])
def get_aft_velocity():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    org = flask.request.json["org"]
    result = adoapi.AdoApi.AdoGetAtfVelocityMonthlyData(token, querypath, project, org)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(tfs_base_route+"/v1.0/atfvelocity", methods=["POST"])
def get_tfs_aft_velocity():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    result = adoapi.AdoApi.TfsGetAtfVelocityMonthlyData(token, querypath, project)
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