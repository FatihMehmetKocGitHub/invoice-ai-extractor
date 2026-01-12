from app.services.validation.vat import validate_vat

def test_vat_placeholder():
    assert isinstance(validate_vat(100.0), list)
