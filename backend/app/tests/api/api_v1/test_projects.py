from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_read_main(client: TestClient, db: Session) -> None:
    response = client.get('api/v1/projects/')
    assert response.status_code == 200
    content = response.json()
    assert content[0]['name'] == 'test'