from app.services.postprocess.normalize import normalize

def test_normalize_returns_dict():
    assert normalize({"a": 1})["a"] == 1
