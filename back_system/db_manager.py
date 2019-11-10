import mongoengine


class DBManager:
    def __init__(self, db_name, db_user, db_pass, db_host, db_port):
        self.db: mongoengine.connection = mongoengine.connect(db_name,
                                                              username=db_user,
                                                              password=db_pass,
                                                              host=db_host,
                                                              port=db_port)
