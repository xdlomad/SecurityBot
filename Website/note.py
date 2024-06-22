from datetime import datetime
import uuid


# Note class
class Note():

    def __init__(self,  body, user_id, user_name, id=""):
        self.body = body
        self.user_id = user_id
        self.user_name = user_name
        self.timestamp = datetime.now()
        self.id = uuid.uuid4().hex if not id else id

    # Return dictionary representation of object
    def dict(self):
        return {
            "body": self.body,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "timestamp": self.timestamp,
            "id": self.id,
        }
