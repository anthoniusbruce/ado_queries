from azure.devops.connection import Connection
from azure.devops.v5_1.work_item_tracking import models
from msrest.authentication import BasicAuthentication
import cycle_time
import story_point_data
import task_extents
import datetime
import atf_velocity_response
import velocity_values
import calendar
import velocity_and_bug_response

class AdoApi(object):
    ADO_ORGANIZATION_URL = "https://dev.azure.com/!!!!Add your organization!!!!!"
    ADO_HISTORICAL_URL = "https://dev.azure.com/!!!!Add your second organization!!!!!"
    PROJECT_NAME = "!!!!!!!Project name!!!!!!!"

    @staticmethod
    def _get_connection(token, org):
        credentials = BasicAuthentication('', token)
        connection = Connection(base_url=org, creds=credentials)
        return connection

    @staticmethod
    def AddMonthFilter(year, month, query):
        if (isinstance(month, str)):
            month = list(calendar.month_name).index(month)
        if (isinstance(year, str)):
            year = int(year)
        first_day = datetime.date(year, month, 1)
        last_day = first_day.replace(day = calendar.monthrange(year, month)[1])
        queryparts = query.partition(" order by ")
        result = queryparts[0] + " and [System.CreatedDate] >= '{}' and [System.CreatedDate] <= '{}' ".format(first_day, last_day) + queryparts[1] + queryparts[2]
        return result

    @staticmethod
    def GetTest(connection, querypath, projectname):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # Get query
        get_query_response = work_item_tracking.get_query(projectname, querypath, expand="wiql")

        wiql = AdoApi.AddMonthFilter("2019", "April", get_query_response.wiql)

        tc = models.TeamContext(project=projectname)
        result = work_item_tracking.query_by_wiql(models.Wiql(wiql), tc)
        #result = work_item_tracking.query_by_wiql(models.Wiql(get_query_response.wiql), tc)

        #return wiql
        #return get_query_response.wiql
        #return len(result.work_items)
        return work_item_tracking._serialize.body(result, "WorkItemQueryResult")
        #id = get_query_response.id

        # Get data
        # query_by_id_response = work_item_tracking.query_by_id(id)

        # return work_item_tracking._serialize.body(query_by_id_response, "WorkItemQueryResult")

        # get_work_items_response = work_item_tracking.get_work_item(query_by_id_response.work_items[0].id, expand="Relations")

        # return work_item_tracking._serialize.body(get_work_items_response.relations[0], 'WorkItemRelation')

    @staticmethod
    def AdoGetTest(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetTest(connection, querypath, AdoApi.PROJECT_NAME)

    @staticmethod
    def HistoricalGetTest(token, querypath, projectname):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_HISTORICAL_URL)

        return AdoApi.GetTest(connection, querypath, projectname)

    @staticmethod
    def GetWorkItem(connection, workitemid):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # get work item data
        work_item_response = work_item_tracking.get_work_item(workitemid, expand="All")

        return work_item_tracking._serialize.body(work_item_response, 'WorkItem')

    @staticmethod
    def AdoGetWorkItem(token, workitemid):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetWorkItem(connection, workitemid)

    @staticmethod
    def HistoricalGetWorkItem(token, workitemid):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_HISTORICAL_URL)

        return AdoApi.GetWorkItem(connection, workitemid)

    @staticmethod
    def GetWorkItemHistory(connection, workitemid):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # get history
        get_updates_response = work_item_tracking.get_updates(workitemid)

        return work_item_tracking._serialize.body(get_updates_response, '[WorkItemUpdate]')

    @staticmethod
    def AdoGetWorkItemHistory(token, workitemid):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetWorkItemHistory(connection, workitemid)

    @staticmethod
    def HistoricalGetWorkItemHistory(token, workitemid):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_HISTORICAL_URL)

        return AdoApi.GetWorkItemHistory(connection, workitemid)

    @staticmethod
    def GetFirstActivatedDate(work_item_history):
        activated_date = ""
        activatedDateKey = "Microsoft.VSTS.Common.ActivatedDate"
        for history_item in work_item_history:
            if (not history_item.fields is None and activatedDateKey in history_item.fields):
                act_date = history_item.fields[activatedDateKey].new_value
                if (not act_date is None):
                    if (activated_date == "" or act_date < activated_date):
                        activated_date = act_date
        return activated_date


    @staticmethod
    def PrepWorkItem(work_item, work_item_history):
        cycle = cycle_time.CycleTime(work_item.id, "", "")
        ResolvedDateKey = "Microsoft.VSTS.Common.ResolvedDate"
        ClosedDateKey = "Microsoft.VSTS.Common.ClosedDate"
        ChangedDateKey = "System.ChangedDate"
        if (not work_item.fields is None and ResolvedDateKey in work_item.fields):
            cycle.resolved = AdoApi._convert_str_to_date(work_item.fields[ResolvedDateKey])
        elif (not work_item.fields is None and ClosedDateKey in work_item.fields):
            cycle.resolved = AdoApi._convert_str_to_date(work_item.fields[ClosedDateKey])
        elif (not work_item.fields is None and ChangedDateKey in work_item.fields):
            cycle.resolved = AdoApi._convert_str_to_date(work_item.fields[ChangedDateKey])
        else:
            cycle.resolved = datetime.datetime.min
            print("workitemid:{}".format(work_item.id))

        cycle.firstactive = AdoApi._convert_str_to_date(AdoApi.GetFirstActivatedDate(work_item_history))

        return cycle

    @staticmethod
    def GetCycleTimes(cycle_times, ids, work_item_tracking):
        if (len(ids) == 0):
            return cycle_times

        get_work_items_response = work_item_tracking.get_work_items(ids)
        for wrk_tm in get_work_items_response:
            wrk_tm_hstry = work_item_tracking.get_updates(wrk_tm.id)
            cycle = AdoApi.PrepWorkItem(wrk_tm, wrk_tm_hstry)
            cycle_times.append(cycle)

        return cycle_times

    @staticmethod
    def GetCycleTimeFromUserStoryQuery(connection, querypath, projectname):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # Get query
        get_query_response = work_item_tracking.get_query(projectname, querypath)
        id = get_query_response.id

        # Get data
        query_by_id_response = work_item_tracking.query_by_id(id)

        cycle_times = []
        ids = []
        count = 0
        for work_item_ref in query_by_id_response.work_items:
            count = count + 1
            ids.append(work_item_ref.id)

            if (count == 200):
                count = 0
                cycle_times = AdoApi.GetCycleTimes(cycle_times, ids, work_item_tracking)
                ids = []

        cycle_times = AdoApi.GetCycleTimes(cycle_times, ids, work_item_tracking)

        return cycle_times

    @staticmethod
    def AdoGetCycleTimeFromUserStoryQuery(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetCycleTimeFromUserStoryQuery(connection, querypath, AdoApi.PROJECT_NAME)

    @staticmethod
    def HistoricalGetCycleTimeFromUserStoryQuery(token, querypath, projectname):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_HISTORICAL_URL)

        return AdoApi.GetCycleTimeFromUserStoryQuery(connection, querypath, projectname)

    @staticmethod
    def ConvertToPoints(total_seconds):
        MAX_0 = 60
        MAX_1 = 43200
        MAX_2 = 172800
        MAX_3 = 518400
        MAX_5 = 864000
        MAX_8 = 1728000

        story_points = 13
        if (total_seconds <= MAX_0):
            story_points = 0
        elif (total_seconds <= MAX_1):
            story_points =  1
        elif (total_seconds <= MAX_2):
            story_points = 2
        elif (total_seconds <= MAX_3):
            story_points = 3
        elif (total_seconds <= MAX_5):
            story_points = 5
        elif (total_seconds <= MAX_8):
            story_points = 8

        return story_points

    @staticmethod
    def GetAdoStoryPoints(story_points, ids, work_item_tracking):
        WorkItemTypeKey = "System.WorkItemType"
        CreatedDateKey = "System.CreatedDate"
        ClosedDateKey = "Microsoft.VSTS.Common.ClosedDate"
        ClosedByKey = "Microsoft.VSTS.Common.ClosedBy"
        StateKey = "System.State"

        if (len(ids) == 0):
            return story_points

        get_work_items_response = work_item_tracking.get_work_items(ids, expand="Relations")
        for wrk_tm in get_work_items_response:
            wrk_tm_hstry = work_item_tracking.get_updates(wrk_tm.id)
            cycle = AdoApi.PrepWorkItem(wrk_tm, wrk_tm_hstry)
            points = story_point_data.StoryPointData(cycle.workitemid, cycle.firstactive, cycle.resolved)

            task_ids = []
            if (wrk_tm.relations != None):
                for related in wrk_tm.relations:
                    if (related.attributes["name"] == "Child"):
                        segments = related.url.split("/")
                        task_ids.append(segments.pop())

            if (len(task_ids) > 0):
                tasks = work_item_tracking.get_work_items(task_ids)
                task_dates = {}
                for task in tasks:
                    if (task.fields[WorkItemTypeKey] == "Task" and task.fields[StateKey] == "Closed"):
                            created_date = AdoApi._convert_str_to_date(task.fields[CreatedDateKey])
                            closed_date = AdoApi._convert_str_to_date(task.fields[ClosedDateKey])
                            closed_by = task.fields[ClosedByKey]["displayName"]
                            task_dates.setdefault(closed_by,[]).append(task_extents.TaskExtents(created_date, closed_date))
                
                points_total = datetime.timedelta(0)
                for key in task_dates:
                    points.closers.add(key)
                    for extents in task_dates[key]:
                        start_date = extents.created_date
                        if (points.firstactive > start_date):
                            start_date = points.firstactive
                        date_resolved = extents.closed_date
                        date_activated = start_date
                        if (date_resolved > date_activated):
                            points_total =  points_total + (date_resolved - date_activated)

                points.storypoints = AdoApi.ConvertToPoints(points_total.total_seconds())

            story_points.append(points)

        return story_points

    @staticmethod 
    def _convert_str_to_date(strdate):
        if (strdate.find(".") ==  -1):
            strdate = strdate.replace("Z", ".0Z")
        return datetime.datetime.strptime(strdate, '%Y-%m-%dT%H:%M:%S.%fZ')


    @staticmethod
    def GetHistoricalStoryPoints(story_points, ids, work_item_tracking):
        WorkItemTypeKey = "System.WorkItemType"
        CreatedDateKey = "System.CreatedDate"
        ClosedDateKey = "Microsoft.VSTS.Common.ClosedDate"
        ClosedByKey = "Microsoft.VSTS.Common.ClosedBy"
        StateKey = "System.State"

        if (len(ids) == 0):
            return story_points

        get_work_items_response = work_item_tracking.get_work_items(ids, expand="Relations")
        for wrk_tm in get_work_items_response:
            wrk_tm_hstry = work_item_tracking.get_updates(wrk_tm.id)
            cycle = AdoApi.PrepWorkItem(wrk_tm, wrk_tm_hstry)
            points = story_point_data.StoryPointData(cycle.workitemid, cycle.firstactive, cycle.resolved)

            task_ids = []
            if (wrk_tm.relations != None):
                for related in wrk_tm.relations:
                    if (related.rel == "System.LinkTypes.Hierarchy-Forward"):
                        segments = related.url.split("/")
                        task_ids.append(segments.pop())

            if (len(task_ids) > 0):
                tasks = work_item_tracking.get_work_items(task_ids)
                task_dates = {}
                for task in tasks:
                    if (task.fields[WorkItemTypeKey] == "Task" and task.fields[StateKey] == "Closed"):
                            created_date = AdoApi._convert_str_to_date(task.fields[CreatedDateKey])
                            closed_date = AdoApi._convert_str_to_date(task.fields[ClosedDateKey])
                            closed_by = task.fields[ClosedByKey]["displayName"]
                            task_dates.setdefault(closed_by,[]).append(task_extents.TaskExtents(created_date, closed_date))
                
                points_total = datetime.timedelta(0)
                for key in task_dates:
                    points.closers.add(key)
                    for extents in task_dates[key]:
                        start_date = extents.created_date
                        if (points.firstactive > start_date):
                            start_date = points.firstactive
                        date_resolved = extents.closed_date
                        date_activated = start_date
                        if (date_resolved > date_activated):
                            points_total =  points_total + (date_resolved - date_activated)

                points.storypoints = AdoApi.ConvertToPoints(points_total.total_seconds())

            story_points.append(points)

        return story_points

    @staticmethod
    def GetAtfStorySizeFromUserStoryQuery(connection, querypath, projectname, GetStoryPoints):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # Get query
        get_query_response = work_item_tracking.get_query(projectname, querypath)
        id = get_query_response.id

        # Get data
        query_by_id_response = work_item_tracking.query_by_id(id)

        story_points = []
        ids = []
        count = 0
        for work_item_ref in query_by_id_response.work_items:
            count = count + 1
            ids.append(work_item_ref.id)

            if (count == 200):
                count = 0
                story_points = GetStoryPoints(story_points, ids, work_item_tracking)
                ids = []

        story_points = GetStoryPoints(story_points, ids, work_item_tracking)

        return story_points

    @staticmethod
    def AdoGetAtfStorySizeFromUserStoryQuery(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetAtfStorySizeFromUserStoryQuery(connection, querypath, AdoApi.PROJECT_NAME, AdoApi.GetAdoStoryPoints)

    @staticmethod
    def HistoricalGetAtfStorySizeFromUserStoryQuery(token, querypath, projectname):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_HISTORICAL_URL)

        return AdoApi.GetAtfStorySizeFromUserStoryQuery(connection, querypath, projectname, AdoApi.GetHistoricalStoryPoints)

    @staticmethod 
    def GetAtfVelocityMonthlyData(connection, querypath, projectname, GetStoryPoints):
        story_points = AdoApi.GetAtfStorySizeFromUserStoryQuery(connection, querypath, projectname, GetStoryPoints)
        yearmonths = {}

        for story in story_points:
            year = story.resolved.year
            if (year == 1):
                print("item:{} year:{} resolved:{}".format(story.workitemid, year, story.resolved))
            month = calendar.month_name[story.resolved.month]
            yearmonth = "{}%{}".format(year, month)
            item = yearmonths.get(yearmonth)
            if (item is None):
                velocity = velocity_values.VelocityValues(story.storypoints, story.closers)
                yearmonths.update({yearmonth:velocity})
            else:
                item.add(story.storypoints, story.closers)
                yearmonths.update({yearmonth:item})

        response = []
        for key in yearmonths.keys():
            keyvalues = key.split("%")
            year = keyvalues[0]
            month = keyvalues[1]
            yearmonth = yearmonths.get(key)
            total_story_points = yearmonth.story_points
            number_of_closers = len(yearmonth.closers)
            response.append(atf_velocity_response.AtfVelocityResponse(year, month, total_story_points, number_of_closers))

        return response

    @staticmethod
    def AdoGetAtfVelocityMonthlyData(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetAtfVelocityMonthlyData(connection, querypath, AdoApi.PROJECT_NAME, AdoApi.GetAdoStoryPoints)

    @staticmethod
    def HistoricalGetAtfVelocityMonthlyData(token, querypath, projectname):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_HISTORICAL_URL)

        return AdoApi.GetAtfVelocityMonthlyData(connection, querypath, projectname, AdoApi.GetHistoricalStoryPoints)

    @staticmethod
    def GetAtfVelocityAndBugsMonthlyData(connection, velocityquery, bugquery, projectname, GetStoryPoints):
        velocities = AdoApi.GetAtfVelocityMonthlyData(connection, velocityquery, projectname, GetStoryPoints)

        work_item_tracking = connection.clients.get_work_item_tracking_client()
        # Get bug query for modification
        get_query_response = work_item_tracking.get_query(projectname, bugquery, expand="wiql")
        velocities_and_bugs = []
        for velo in velocities:
            velo_bug = velocity_and_bug_response.VelocityAndBugResponse(velo.year, velo.month, velo.total_story_points, velo.number_of_closers, velo.average_story_points, 0)
            
            wiql = AdoApi.AddMonthFilter(velo.year, velo.month, get_query_response.wiql)

            tc = models.TeamContext(project=projectname)
            result = work_item_tracking.query_by_wiql(models.Wiql(wiql), tc)
            velo_bug.bug_count = len(result.work_items)

            velocities_and_bugs.append(velo_bug)

        return velocities_and_bugs

    @staticmethod
    def AdoGetAtfVelocityAndBugsMonthlyData(token, velocityquery, bugquery):
        # Create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetAtfVelocityAndBugsMonthlyData(connection, velocityquery, bugquery, AdoApi.PROJECT_NAME, AdoApi.GetAdoStoryPoints)

    @staticmethod
    def HistoricalGetAtfVelocityAndBugsMonthlyData(token, velocityquery, bugquery, projectname):
        # Create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_HISTORICAL_URL)

        return AdoApi.GetAtfVelocityAndBugsMonthlyData(connection, velocityquery, bugquery, projectname, AdoApi.GetHistoricalStoryPoints)
