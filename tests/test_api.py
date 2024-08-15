import argparse, json
import httpx
import pytest
import pytest_asyncio

import asyncio

class TestApi:
    url = "http://127.0.0.1:8000"
    #loop = asyncio.new_event_loop()
    ss = httpx.AsyncClient()

    @pytest.mark.asyncio(scope="session")
    async def test_operations(self):
        url = "{}/{}".format(self.url, "operations")

        params = {"from_date": "2023-05-01", "to_date": "2023-05-02"}

        res = await self.ss.get(url, params = params)

        assert res.status_code == 200

    @pytest.mark.asyncio(scope="session")
    async def test_operations_with_wrong_date_format(self):
        url = "{}/{}".format(self.url, "operations")

        params = {"from_date": "2023-05-01", "to_date": "2023-05/02"}

        res = await self.ss.get(url, params = params)

        assert res.status_code == 400

    @pytest.mark.asyncio(scope="session")
    async def test_operations_with_date_out_of_range(self):
        url = "{}/{}".format(self.url, "operations")

        params = {"from_date": "2023-05-01", "to_date": "2023-05-30"}

        res = await self.ss.get(url, params = params)

        assert res.status_code == 400

    @pytest.mark.asyncio(scope="session")
    async def test_docs_in_response(self):
        url = "{}/{}".format(self.url, "operations")

        params = {"from_date": "2023-05-01", "to_date": "2023-05-02"}

        res = await self.ss.get(url, params = params)

        resp = res.json()

        id_available = all(["doc" in x for x in resp["operations"]])

        assert res.status_code == 200 and id_available

    @pytest.mark.asyncio(scope="session")
    async def test_id_in_response(self):
        url = "{}/{}".format(self.url, "operations")

        params = {"from_date": "2023-05-01", "to_date": "2023-05-02"}

        res = await self.ss.get(url, params = params)

        resp = res.json()

        id_available = all(["id" in x["doc"] for x in resp["operations"]])

        assert res.status_code == 200 and id_available

    @pytest.mark.asyncio(scope="session")
    async def test_operation_type_in_response(self):
        url = "{}/{}".format(self.url, "operations")

        params = {"from_date": "2023-05-01", "to_date": "2023-05-02"}

        res = await self.ss.get(url, params = params)

        resp = res.json()

        op_types = ["createFile", "deleteFile", "updateFileName", "updateFileMeta"]

        id_available = all([x["operation_type"] in op_types for x in resp["operations"]])

        assert res.status_code == 200 and id_available

    @pytest.mark.asyncio(scope="session")
    async def test_many_dates(self):
        url = "{}/{}".format(self.url, "operations")

        is_ok = True
        for x in range(1, 8):
            params = {"from_date": "2023-05-0{}".format(x), "to_date": "2023-05-0{}".format(x+1)}

            res = await self.ss.get(url, params = params)

            resp = res.json()

            op_types = ["createFile", "deleteFile", "updateFileName", "updateFileMeta"]

            id_available = all([x["operation_type"] in op_types for x in resp["operations"]])

            if res.status_code != 200 or not id_available:
                is_ok = False

        assert is_ok