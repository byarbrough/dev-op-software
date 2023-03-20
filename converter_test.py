import converter

def test_convert():
    assert converter.convert("1") == "One"
    assert converter.convert("-45") == "(negative) Forty five"
    assert converter.convert("2016") == "Two thousand and sixteen"