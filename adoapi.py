from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import cycle_time

class AdoApi(object):
    ADO_ORGANIZATION_URL = 'https://dev.azure.com/tr-tax'
    TFS_ORGANIZATION_URL = 'http://tfstta.int.thomsonreuters.com:8080/tfs/DefaultCollection'
    PROJECT_NAME = "TaxProf"

    @staticmethod
    def _get_connection(token, org):
        credentials = BasicAuthentication('', token)
        connection = Connection(base_url=org, creds=credentials)
        return connection

    @staticmethod
    def GetTest(connection, querypath):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # Get query
        get_query_response = work_item_tracking.get_query(
            AdoApi.PROJECT_NAME, querypath)
        id = get_query_response.id

        # Get data
        query_by_id_response = work_item_tracking.query_by_id(id)

        work_item_id = query_by_id_response.work_items[0].id

        story_updates = work_item_tracking.get_updates(work_item_id)

        activated_date = ""
        activatedDateKey = "Microsoft.VSTS.Common.ActivatedDate"
        for story_upd in story_updates:
            if (not story_upd.fields is None and activatedDateKey in story_upd.fields):
                act_date = story_upd.fields[activatedDateKey].new_value
                if (not act_date is None):
                    if (activated_date == "" or act_date < activated_date):
                        activated_date = act_date

        return activated_date

    @staticmethod
    def AdoGetTest(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetTest(connection, querypath)

    @staticmethod
    def TfsGetTest(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.TFS_ORGANIZATION_URL)

        return AdoApi.GetTest(connection, querypath)

    @staticmethod
    def GetWorkItem(connection, workitemid):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # get work item data
        work_item_response = work_item_tracking.get_work_item(workitemid)

        return work_item_tracking._serialize.body(work_item_response, 'WorkItem')

    @staticmethod
    def AdoGetWorkItem(token, workitemid):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetWorkItem(connection, workitemid)

    @staticmethod
    def TfsGetWorkItem(token, workitemid):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.TFS_ORGANIZATION_URL)

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
    def TfsGetWorkItemHistory(token, workitemid):
        # create connection
        connection = AdoApi._get_connection(token, AdoApi.TFS_ORGANIZATION_URL)

        return AdoApi.GetWorkItemHistory(connection, workitemid)

    @staticmethod
    def PrepWorkItem(work_item, work_item_history):
        cycle = cycle_time.CycleTime(work_item.id, "", "")
        ResolvedDateKey ="Microsoft.VSTS.Common.ResolvedDate"
        if (not work_item.fields is None and ResolvedDateKey in work_item.fields):
            cycle.resolved = work_item.fields[ResolvedDateKey]

        activated_date = ""
        activatedDateKey = "Microsoft.VSTS.Common.ActivatedDate"
        for history_item in work_item_history:
            if (not history_item.fields is None and activatedDateKey in history_item.fields):
                act_date = history_item.fields[activatedDateKey].new_value
                if (not act_date is None):
                    if (activated_date == "" or act_date < activated_date):
                        activated_date = act_date
        cycle.firstactive = activated_date

        return cycle

    @staticmethod
    def GetCycleTimes(cycle_times, alt_ids, work_item_tracking):
        if (len(alt_ids) == 0):
            return cycle_times

        get_work_items_response = work_item_tracking.get_work_items(alt_ids)
        for wrk_tm in get_work_items_response:
            wrk_tm_hstry = work_item_tracking.get_updates(wrk_tm.id)
            cycle = AdoApi.PrepWorkItem(wrk_tm, wrk_tm_hstry)
            cycle_times.append(cycle)

        return cycle_times

    @staticmethod
    def GetCycleTimeFromUserStoryQuery(connection, querypath):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # Get query
        get_query_response = work_item_tracking.get_query(
            AdoApi.PROJECT_NAME, querypath)
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

        cycle_times = AdoApi.GetCycleTimes(cycle_times, ids, work_item_tracking)

        return cycle_times

    @staticmethod
    def GetCycleTimeFromUserStoryQuery2(connection, querypath):
        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # Get query
        get_query_response = work_item_tracking.get_query(
            AdoApi.PROJECT_NAME, querypath)
        id = get_query_response.id

        # Get data
        query_by_id_response = work_item_tracking.query_by_id(id)

        cycle_times = []
        ids = ""
        count = 0
        for work_item_ref in query_by_id_response.work_items:
            count = count + 1
            if (ids == ""):
                ids = str(work_item_ref.id)
            else:
                ids = ids + "," + str(work_item_ref.id)

            if (count == 200):
                count = 0
                cycle_times = AdoApi.GetCycleTimes(cycle_times, ids, work_item_tracking)

        cycle_times = AdoApi.GetCycleTimes(cycle_times, ids, work_item_tracking)

        return cycle_times

    @staticmethod
    def AdoGetCycleTimeFromUserStoryQuery(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetCycleTimeFromUserStoryQuery(connection, querypath)
