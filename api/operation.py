import falcon
import aiofiles
import asyncio

import json

class Operation:
    def __init__(self):
        pass

    async def compare_docs(self, last_doc, current_doc):
        if not last_doc:
            return {
                "operation_type": "createFile",
                "doc": current_doc
            }

        if not current_doc:
            return {
                "operation_type": "deleteFile",
                "doc": { "id": last_doc["id"]}
            }

        if last_doc["name"] != current_doc["name"]:
            return {
                "operation_type": "updateFileName",
                "doc": {x: current_doc[x] for x in ["id", "name"]}
            }

        docs_keys = {*last_doc["meta"].keys(), *current_doc["meta"].keys()}

        if not all(last_doc["meta"].get(x, "") == current_doc["meta"].get(x, "") for x in docs_keys):
            return {
                "operation_type": "updateFileMeta",
                "changes": {x: current_doc[x] for x in ["id", "meta"]}
            }

        return {}
        
    async def get_file(self, filename):
        filename = "files/{}.jsonl".format(filename)

        content = None

        try:
            async with aiofiles.open(filename, mode = 'r') as f:
                content = [json.loads(line) async for line in f if line]

        except Exception as ex:
            print("Error file", filename)

        if not content:
            return {}

        docs = {doc["id"]: doc for doc in content}

        return docs

    

    async def on_get_operations(self, req, resp): #list_operations

        #Read query params
        from_date = req.get_param_as_date("from_date", default = "", required = True)
        to_date = req.get_param_as_date("to_date", default = "", required=True)

        #Get async the json docs from files
        aws = [self.get_file(from_date), self.get_file(to_date)]

        last_docs, current_docs = await asyncio.gather(*aws)

        if not last_docs:
            resp.media = {"error": "File for date {} not found".format(from_date)}
            resp.status = falcon.HTTP_400
            return None

        if not current_docs:
            resp.media = {"error": "File for date {} not found".format(to_date)}
            resp.status = falcon.HTTP_400
            return None

        #Concatenate ids from both docs
        all_ids = {*last_docs.keys(), *current_docs.keys()}

        #Compare the docs using the ID and return the operations
        aws = [self.compare_docs(last_docs.get(id, {}), current_docs.get(id, {})) for id in all_ids]

        opts = [opt for opt in await asyncio.gather(*aws) if opt]


        resp.media = {"operations": opts}
        resp.status = falcon.HTTP_200


    