from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

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
        get_query_response = work_item_tracking.get_query(AdoApi.PROJECT_NAME, querypath)
        id = get_query_response.id
        
        # Get data
        query_by_id_response = work_item_tracking.query_by_id(id)
        work_item_id = query_by_id_response.work_item_relations[1].target.id

        # Get History
        get_updates_response = work_item_tracking.get_updates(work_item_id)

        return work_item_tracking._serialize.body(get_updates_response, '[WorkItemUpdate]')
        
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
        #get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        #get work item data
        work_item_response = work_item_tracking.get_work_item(workitemid)

        return work_item_tracking._serialize.body(work_item_response, 'WorkItem')

    @staticmethod
    def AdoGetWorkItem(token, workitemid):
        #create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetWorkItem(connection, workitemid)

    @staticmethod
    def TfsGetWorkItem(token, workitemid):
        #create connection
        connection = AdoApi._get_connection(token, AdoApi.TFS_ORGANIZATION_URL)

        return AdoApi.GetWorkItem(connection, workitemid)

    @staticmethod
    def GetWorkItemHistory(connection, workitemid):
        #get work item tracking client
        work_item_tracking = connection.clients.get_work_item_tracking_client()

        #get history
        get_updates_response = work_item_tracking.get_updates(workitemid)

        return work_item_tracking._serialize.body(get_updates_response, '[WorkItemUpdate]')

    @staticmethod
    def AdoGetWorkItemHistory(token, workitemid):
        #create connection
        connection = AdoApi._get_connection(token, AdoApi.ADO_ORGANIZATION_URL)

        return AdoApi.GetWorkItemHistory(connection, workitemid)

    @staticmethod
    def TfsGetWorkItemHistory(token, workitemid):
        #create connection
        connection = AdoApi._get_connection(token, AdoApi.TFS_ORGANIZATION_URL)

        return AdoApi.GetWorkItemHistory(connection, workitemid)
