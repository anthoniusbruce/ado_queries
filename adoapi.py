from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

class AdoApi(object):
    ORGANIZATION_URL = 'https://dev.azure.com/tr-tax'
    PROJECT_NAME = "TaxProf"

    @staticmethod
    def _get_connection(token):
        credentials = BasicAuthentication('', token)
        connection = Connection(base_url=AdoApi.ORGANIZATION_URL, creds=credentials)
        return connection

    @staticmethod
    def GetTest(token, querypath):
        # Create a connection to the org
        connection = AdoApi._get_connection(token)

        # get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        # Get query
        get_query_response = work_item_tracking.get_query(AdoApi.PROJECT_NAME, querypath)
        id = get_query_response.id
        
        # Get data
        query_by_id_response = work_item_tracking.query_by_id(id)
        work_item_id = query_by_id_response.work_item_relations[1].target.id

        #return work_item_tracking._serialize.body(query_by_id_response, 'WorkItemQueryResult')

        # Get History
        get_updates_response = work_item_tracking.get_updates(work_item_id)

        return work_item_tracking._serialize.body(get_updates_response, '[WorkItemUpdate]')

    @staticmethod
    def GetWorkItem(token, workitemid):
        #create connection
        connection = AdoApi._get_connection(token)

        #get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        #get work item data
        work_item_response = work_item_tracking.get_work_item(workitemid)

        return work_item_tracking._serialize.body(work_item_response, 'WorkItem')

    @staticmethod
    def GetWorkItemHistory(token, workitemid):
        #create connection
        connection = AdoApi._get_connection(token)

        #get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        #get history
        get_updates_response = work_item_tracking.get_updates(workitemid)

        return work_item_tracking._serialize.body(get_updates_response, '[WorkItemUpdate]')
