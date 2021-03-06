from datetime import datetime
import githubAPI
from sqlite3 import Cursor, Connection


class Logic:
    '''
This is logic to analyze the data from the githubAPI Pull Request API and store the data in a database.
    '''

    def __init__(self, gha: githubAPI = None, data: dict = None, responseHeaders: tuple = None, cursor: Cursor = None, connection: Connection = None):
        '''
Initializes the class and sets class variables that are to be used only in this class instance.\n
:param gha: An instance of the githubAPI class.\n
:param data: The dictionary of data that is returned from the API call.\n
:param responseHeaders: The dictionary of data that is returned with the API call.\n
:param cursor: The database cursor.\n
:param connection: The database connection.
        '''
        self.gha = gha
        self.data = data
        self.responseHeaders = responseHeaders
        self.dbCursor = cursor
        self.dbConnection = connection

    def parser(self) -> None:
        '''
Actually scrapes, sanitizes, and stores the data returned from the API call.
        '''
        while True:
            if len(self.data) == 0:  # If there is no data returned, quit parsing immediatly
                break

            for x in self.data:  # Scrapes the data
                # All of these are manually set to none in order prevent overwritting variable data
                user = None
                user_id = None
                pull_req_id = None
                comments_url = None
                node_id = None
                number = None
                title = None
                labels = None
                state = None
                locked = None
                assignee = None
                assignees = None
                created_at = None
                updated_at = None
                closed_at = None
                body = None
                comment_user = None
                comment_user_id = None
                comment_id = None
                comment_node_id = None
                comment_created_at = None
                comment_updated_at = None
                comment_body = None

                user = x["user"]["login"]
                user_id = x["user"]["id"]
                pull_req_id = x["id"]
                comments_url = x["comments_url"]
                node_id = x["node_id"]
                number = x["number"]
                title = x["title"]
                labels = x["labels"]
                state = x["state"]
                locked = x["locked"]
                assignee = x["assignee"]
                assignees = x["assignees"]
                body = x["body"]
                # Scrapes and sanitizes the time related data
                created_at = x["created_at"].replace(
                    "T", " ").replace("Z", " ")
                updated_at = x["updated_at"].replace(
                    "T", " ").replace("Z", " ")
                try:
                    closed_at = x["closed_at"].replace("T", " ").replace("Z", " ")
                    closed_at = datetime.strptime(closed_at, "%Y-%m-%d %H:%M:%S ")
                except:
                    closed_at = None

                created_at = datetime.strptime(
                    created_at, "%Y-%m-%d %H:%M:%S ")
                updated_at = datetime.strptime(
                    updated_at, "%Y-%m-%d %H:%M:%S ")
                
                # Stores the data into a SQL database
                sql = "INSERT INTO PULLREQUESTS (user, user_id, pull_req_id, comments_url, node_id, number, title, labels, state, locked, assignee, assignees, created_at, updated_at, closed_at, body, comment_user, comment_user_id, comment_id, comment_node_id, comment_created_at, comment_updated_at, comment_body) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
                self.dbCursor.execute(sql, (str(user), str(user_id), str(pull_req_id), str(comments_url), str(node_id), str(number), str(title), str(labels), str(state), str(locked), str(assignee), str(assignees), str(created_at), str(updated_at), str(
                    closed_at), str(body), str(comment_user), str(comment_user_id), str(comment_id), str(comment_node_id), str(comment_created_at), str(comment_updated_at), str(comment_body)))    # Str data type wrapper called in order to assure type
                self.dbConnection.commit()  # Actually stores the data in the database

            # Below checks to see if there are any links related to the data returned
            try:
                foo = self.responseHeaders["Link"]
                if 'rel="next"' not in foo:  # Breaks if there is no rel="next" text in key Link
                    break

                bar = foo.split(",")

                for x in bar:
                    if 'rel="next"' in x:   # Recursive logic to open a supported link, download the data, and reparse the data
                        url = x[x.find("<")+1:x.find(">")]
                        self.data = self.gha.access_githubAPISpecificURL(
                            url=url)
                        self.responseHeaders = self.gha.get_ResponseHeaders()
                        self.parser()   # Recursive
            except KeyError:    # Raises if there is no key Link
                break
            break
