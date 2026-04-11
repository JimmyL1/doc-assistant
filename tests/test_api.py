def test_health(client):
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "vector_store_count" in data


def test_upload_txt(client, sample_txt_path):
    with open(sample_txt_path, "rb") as f:
        resp = client.post(
            "/api/v1/upload",
            files={"file": ("sample.txt", f, "text/plain")},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["chunks_added"] > 0
    assert data["filename"] == "sample.txt"


def test_query_after_upload(client):
    resp = client.post(
        "/api/v1/query",
        json={"question": "這份文件的主題是什麼？"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["answer"] != ""
    assert isinstance(data["sources"], list)


def test_upload_unsupported_type(client):
    resp = client.post(
        "/api/v1/upload",
        files={"file": ("report.xyz", b"some content", "application/octet-stream")},
    )
    assert resp.status_code == 422
