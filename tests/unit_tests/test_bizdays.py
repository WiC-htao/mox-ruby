import numpy as np
import pytest

from mox.ruby.bizdays import Bizdays


def test_Bizdays(request: pytest.FixtureRequest):
    assert Bizdays.from_dts(
        request.config.rootpath / "tests/data/unit_tests/sample_calendar.dts"
    )
    with pytest.raises(AssertionError):
        Bizdays(np.array([20240922, 20240924, 20240924]))


class TestBizdays:

    BIZDAYS = Bizdays(np.array([20240922, 20240924, 20240926]))

    def test_next(self):
        assert self.BIZDAYS.next(20240924) == 20240926
        assert self.BIZDAYS.next(20240925) == 20240926

    def test_prev(self):
        assert self.BIZDAYS.prev(20240924) == 20240922
        assert self.BIZDAYS.prev(20240923) == 20240922
        with pytest.raises(ValueError):
            self.BIZDAYS.prev(20240922)
        with pytest.raises(ValueError):
            self.BIZDAYS.prev(20240921)
