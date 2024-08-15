from falcon import testing
import app

import pytest
import pytest_asyncio

class TestFalcon:
    app = app.create_app()
    client = testing.ASGIConductor(app)

    @pytest.mark.asyncio(scope="session")
    async def test_operations(self):
        params = {"from_date": "2023-05-01", "to_date": "2023-05-02"}

        res = await self.client.simulate_get('/operations', params=params)

        assert res.status_code == 200