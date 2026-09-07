from ingest.paths import safe_symbol_filename
from ingest.symbols import filter_common, is_common_stock_ticker


def test_keeps_common_and_class_shares() -> None:
    assert is_common_stock_ticker("AAPL")
    assert is_common_stock_ticker("BRK.B")
    assert is_common_stock_ticker("BF.A")
    assert is_common_stock_ticker("AA")


def test_drops_preferred_warrant_unit_wi() -> None:
    assert not is_common_stock_ticker(".PR.I.PR.A")
    assert not is_common_stock_ticker("BAC.PR")
    assert not is_common_stock_ticker("F.WS")
    assert not is_common_stock_ticker("XYZ.U")
    assert not is_common_stock_ticker("ABC/WI")
    assert not is_common_stock_ticker("ABC.WI")
    assert not is_common_stock_ticker(".PR.S/WI")


def test_filter_common_dedupes() -> None:
    out = filter_common(["aapl", "AAPL", "BAC.PR", "BRK.B", ".PR.I.PR.A"])
    assert out == ["AAPL", "BRK.B"]


def test_windows_reserved_filenames() -> None:
    assert safe_symbol_filename("AAPL") == "AAPL"
    assert safe_symbol_filename("CON") == "_CON"
    assert safe_symbol_filename("PRN") == "_PRN"
