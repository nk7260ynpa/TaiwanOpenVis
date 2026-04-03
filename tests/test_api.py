"""API 端點單元測試。"""


def test_health(client):
    """健康檢查端點應回傳 200 與 status ok。"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "data_cached_at" in data


def test_get_counties(client, sample_counties):
    """縣市端點應回傳縣市人口密度列表。"""
    response = client.get("/api/population/counties")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_counties)
    assert data[0]["county"] == "台北市"
    assert "population" in data[0]
    assert "area" in data[0]
    assert "density" in data[0]


def test_get_towns(client, sample_towns):
    """鄉鎮端點應回傳指定縣市的鄉鎮資料。"""
    response = client.get("/api/population/towns/台北市")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["county"] == "台北市" for t in data)


def test_get_towns_not_found(client):
    """不存在的縣市應回傳 404。"""
    response = client.get("/api/population/towns/不存在市")
    assert response.status_code == 404


def test_get_all_towns(client, sample_towns):
    """全部鄉鎮端點應回傳所有鄉鎮資料。"""
    response = client.get("/api/population/towns/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_towns)


def test_index_page(client):
    """首頁應回傳 200。"""
    response = client.get("/")
    assert response.status_code == 200


def test_map_page(client):
    """地圖頁應回傳 200。"""
    response = client.get("/map")
    assert response.status_code == 200


def test_detail_page(client):
    """詳情頁應回傳 200。"""
    response = client.get("/detail/台北市")
    assert response.status_code == 200
