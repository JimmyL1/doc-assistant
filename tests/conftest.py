import pytest
from pathlib import Path

TEST_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_txt_path():
    return TEST_DIR / "sample_docs" / "engineering_onboarding.txt"
