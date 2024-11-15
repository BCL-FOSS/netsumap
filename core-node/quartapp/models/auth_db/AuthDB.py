from mongoengine import Document, connect

class AuthDB:
    def __init__(self) -> None:
        pass

    def db_connection(self, db_name='', host='', port=27017):
        # Create database connection object
        mdb_host = host
        db = connect(alias=db_name, db=db_name, host=f"mongodb://{mdb_host}", port=port)
        return db