from datetime import date

from ingest.paths import BARS_DIR, FULL_BARS, VIRGIN_BARS
from research.arrow47 import shares_for
from research.arrow65 import fill_session_of
from research.arrow66 import hold_exit_of
from research.arrow81 import (
    CONTROL_ID,
    EXPERIMENTS,
    FILL_KIND,
    HOLD_BACKSTOP,
    NOTIONAL,
    fires_stop,
    first_stop,
    remaining_names,
)
from research.clock import entry_split, is_is_session, tape_root
from research.costs import signed_pnl


def test_id0_hold10_no_stop() -> None:
    assert EXPERIMENTS[0][0] == CONTROL_ID == "h10_4k"
    assert EXPERIMENTS[0][1] is None
    assert FILL_KIND == "nextrth"
    assert HOLD_BACKSTOP == 10
    assert NOTIONAL == 4000.0
    assert len(EXPERIMENTS) == 5
    fill = date(2026, 1, 8)
    sess = [
        date(2026, 1, 8),
        date(2026, 1, 9),
        date(2026, 1, 12),
        date(2026, 1, 13),
        date(2026, 1, 14),
        date(2026, 1, 15),
        date(2026, 1, 16),
        date(2026, 1, 20),
        date(2026, 1, 21),
        date(2026, 1, 22),
        date(2026, 1, 23),
    ]
    assert hold_exit_of(fill, 10, sess) == date(2026, 1, 23)
    assert fires_stop(10.2, 10.0, None) is False
    assert first_stop(10.0, [(1, 10.2), (10, 9.0)], None) == (10, 9.0)
    assert shares_for(20.0, 4000.0) == 200
    assert signed_pnl(-1, 10, 20.0, 19.0) > 0


def test_id1_cashes_lastrth_at_or_above_fill_times_103() -> None:
    assert EXPERIMENTS[1][0] == "stop_3"
    assert EXPERIMENTS[1][1] == 0.03
    assert fires_stop(10.3, 10.0, 0.03) is True
    assert fires_stop(10.29, 10.0, 0.03) is False
    hit = first_stop(10.0, [(1, 10.1), (2, 10.31), (10, 9.0)], 0.03)
    assert hit == (2, 10.31)
    assert hit[0] < HOLD_BACKSTOP
    assert fires_stop(10.0, 10.0, 0.03) is False


def test_id4_does_not_open_new_leftover_after_stop() -> None:
    assert EXPERIMENTS[4][0] == "stop_12"
    kept = remaining_names(["OLD1", "OLD2", "OLD3"], {"OLD1"}, ["NEW", "OLD2", "OLD3"])
    assert kept == ["OLD2", "OLD3"]
    assert "NEW" not in kept
    assert "OLD1" not in kept
    assert fires_stop(11.2, 10.0, 0.12) is True
    assert fires_stop(11.19, 10.0, 0.12) is False


def test_even_month_signal_is_not_is() -> None:
    wed = date(2026, 2, 4)
    assert wed.weekday() == 2
    assert entry_split(wed) == "OOS"
    assert not is_is_session(wed)
    assert is_is_session(date(2026, 1, 7))
    sess = [date(2026, 1, 7), date(2026, 1, 8)]
    assert fill_session_of(date(2026, 1, 7), "nextrth", sess) == date(2026, 1, 8)


def test_do_not_read_lab_a_bars() -> None:
    for d in (date(2026, 1, 7), date(2026, 6, 3), date(2026, 8, 26)):
        assert tape_root(d) != BARS_DIR
        assert tape_root(d) in {VIRGIN_BARS, FULL_BARS}
    assert tape_root(date(2026, 1, 7)) == VIRGIN_BARS
    assert tape_root(date(2026, 7, 1)) == FULL_BARS
