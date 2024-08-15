import argparse
import asyncio
import json
import httpx


class TestAPI:
    def __init__(self):
        self.loop = asyncio.new_event_loop()

        self.ss = httpx.AsyncClient(timeout=None)

        self.url = "http://127.0.0.1:8000"

    async def test_operations(self, params):

        url = "{}/{}".format(self.url, "operations")

        params = params.split(",")

        if len(params) != 2:
            print("Error params: {}".format(params))
            return None

        params = {"from_date": params[0], "to_date":params[1]}

        res = await self.ss.get(url, params = params)

        res = res.json()

        print("Response: ", json.dumps(res, indent=4))

    def run(self, func_loop):
        return self.loop.run_until_complete(func_loop)

    def test(self, case_test, params):
        params = params.split(" ")

        opts = {
            "operations": self.test_operations
        }

        return self.run(opts.get(case_test, "operations")(*params))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='API testing')
    parser.add_argument('--opt', type=str, required=False)
    parser.add_argument('--params', type=str, required=False)

    args = parser.parse_args()

    tester = TestAPI()
    tester.test(args.opt, args.params)