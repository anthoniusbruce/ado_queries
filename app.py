import flask
import adoapi
import cycle_time
import story_point_data
import cycle_time_jsonencoder
import story_point_data_jsonencoder
from flask_swagger_ui import get_swaggerui_blueprint

app = flask.Flask(__name__)
ADO_BASE_ROUTE = "/ado_queries/api"
ADO_HISTORICAL_ROUTE = "/historical_queries/api"

@app.route("/")
def index():
    return "Status: Up!"

@app.route(ADO_BASE_ROUTE + "/v1.0/test", methods = ["POST"])
def get_test():
    querypath = flask.request.json["path"]
    token = flask.request.json["token"]
    history = adoapi.AdoApi.AdoGetTest(token, querypath)
    return flask.jsonify(history)
    
@app.route(ADO_HISTORICAL_ROUTE + "/v1.0/test", methods = ["POST"])
def get_historical_test():
    querypath = flask.request.json["path"]
    token = flask.request.json["token"]
    project = flask.request.json["project"]
    history = adoapi.AdoApi.HistoricalGetTest(token, querypath, project)
    return flask.jsonify(history)
    
@app.route(ADO_BASE_ROUTE+"/v1.0/workitem", methods=["POST"])
def get_workitem():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.AdoGetWorkItem(token, workitem)
    return flask.jsonify(response)

@app.route(ADO_BASE_ROUTE+"/v1.0/history", methods=["POST"])
def get_history():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.AdoGetWorkItemHistory(token, workitem)
    return flask.jsonify(response)

@app.route(ADO_BASE_ROUTE+"/v1.0/cycletime", methods=["POST"])
def get_cycle_time():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    result = adoapi.AdoApi.AdoGetCycleTimeFromUserStoryQuery(token, querypath)
    encoder = cycle_time_jsonencoder.CycleTimeJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_HISTORICAL_ROUTE+"/v1.0/cycletime", methods=["POST"])
def get_historical_cycle_time():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    result = adoapi.AdoApi.HistoricalGetCycleTimeFromUserStoryQuery(token, querypath, project)
    encoder = cycle_time_jsonencoder.CycleTimeJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_BASE_ROUTE+"/v1.0/atfstorypoints", methods=["POST"])
def get_aft_story_points():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    result = adoapi.AdoApi.AdoGetAtfStorySizeFromUserStoryQuery(token, querypath)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_HISTORICAL_ROUTE+"/v1.0/atfstorypoints", methods=["POST"])
def get_historical_aft_story_points():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    result = adoapi.AdoApi.HistoricalGetAtfStorySizeFromUserStoryQuery(token, querypath, project)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_BASE_ROUTE+"/v1.0/atfvelocity", methods=["POST"])
def get_aft_velocity():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    result = adoapi.AdoApi.AdoGetAtfVelocityMonthlyData(token, querypath)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_HISTORICAL_ROUTE+"/v1.0/atfvelocity", methods=["POST"])
def get_ado_default_aft_velocity():
    token = flask.request.json["token"]
    querypath = flask.request.json["path"]
    project = flask.request.json["project"]
    result = adoapi.AdoApi.HistoricalGetAtfVelocityMonthlyData(token, querypath, project)
    encoder = story_point_data_jsonencoder.StoryPointDataJSONEncoder()
    response = flask.Response(encoder.encode(result), mimetype="application/json")
    return response

@app.route(ADO_HISTORICAL_ROUTE+"/v1.0/workitem", methods=["POST"])
def get_historical_workitem():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.HistoricalGetWorkItem(token, workitem)
    return flask.jsonify(response)

@app.route(ADO_HISTORICAL_ROUTE+"/v1.0/history", methods=["POST"])
def get_historical_history():
    token = flask.request.json["token"]
    workitem = flask.request.json["workitemid"]
    response = adoapi.AdoApi.HistoricalGetWorkItemHistory(token, workitem)
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