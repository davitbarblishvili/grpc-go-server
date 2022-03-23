import grpc
from concurrent import futures
import part_identifier_pb2 as pb2
import part_identifier_pb2_grpc as pb2_grpc

import sqlite3
import logging



class PartIdentifierService(pb2_grpc.PartIdentifierService):

    def __init__(self, *args, **kwargs):
        pass
        
    def connectToDatabase(self):

        logging.info("Creating sqlite_part_database.db...")
        with sqlite3.connect("sqlite_part_database.db") as con:
            createPartTableSQL = '''
                            CREATE TABLE IF NOT EXISTS factory_parts
                            (id TEXT PRIMARY KEY, 
                            title TEXT, 
                            image TEXT, 
                            part_number TEXT, 
                            location TEXT)'''

        
            logging.info("Create factory_parts table...")
            con.execute(createPartTableSQL)
            logging.info("part table created")
        
        return con

    def insertPart(self, part_id, part_title, image_url, part_number, location):
        logging.info("Inserting part record ...")
        insert_query = "INSERT into factory_parts(id, title, image, part_number, location) VALUES (?, ?, ?, ?, ?)"
        cur = self.conn.cursor()
        cur.execute(insert_query, (part_id, part_title, image_url, part_number, location))
        self.conn.commit()

        logging.info(cur.lastrowid)    

    def getPartFromDB(self, part_id):
        with sqlite3.connect("sqlite_part_database.db") as conn:
            logging.info("Invoked getPartFromDB Function ...")
            cur = conn.cursor()
            cur.execute("select * from factory_parts where id =?", (part_id,))
            result = cur.fetchall()
            return result
        

    def IdentifyPart(self, request, context):

        # get the string from the incoming request
       
        part_id = request.part_id
        resp = self.getPartFromDB(part_id=part_id)
        result = {
            'id': resp[0][0],
            'title': resp[0][1],
            'image_url': resp[0][2],
            'part_number': resp[0][3],
            'location': resp[0][4]
            }

        return pb2.IdentifyPartResponse(**result)


def serve():
    print("Running the server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_PartIdentifierServiceServicer_to_server(
        PartIdentifierService(), server)
    server.add_insecure_port('[::]:4050')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
   