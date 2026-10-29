import pytest
from income_tax import taxable_income, tax_due, refund_status


# ---------- taxable_income ----------
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_negative_income_raises():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_old_regime_investments_capped():
    # investments 200000 is capped to 150000 -> deduction = 50000 + 150000
    assert taxable_income(1000000, "old", 200000) == 800000


def test_unknown_regime_raises():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "foo", 0)


def test_taxable_income_never_negative():
    # deduction (75000) > gross -> clamped to 0
    assert taxable_income(50000, "new", 0) == 0


# ---------- tax_due ----------
def test_below_exemption():
    assert tax_due(200000, 30) == 0


def test_negative_taxable_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-100, 30)


def test_super_senior_citizen():
    # exempt = 500000, slab = 100000 -> 5%
    assert tax_due(600000, 85) == 5000


def test_senior_citizen():
    # exempt = 300000, slab = 100000 -> 5%
    assert tax_due(400000, 65) == 5000


def test_regular_citizen_first_slab():
    # exempt = 250000, slab = 150000 -> 5%
    assert tax_due(400000, 30) == 7500


def test_regular_citizen_second_slab():
    # exempt = 250000, slab = 350000 -> 12500 + 100000*20%
    assert tax_due(600000, 30) == 32500


# ---------- refund_status ----------
def test_refund_on_time():
    assert refund_status(10000, 5000, True) == "refund"


def test_refund_delayed():
    assert refund_status(10000, 5000, False) == "refund delayed"


def test_pay_balance_on_time():
    assert refund_status(5000, 10000, True) == "pay balance"


def test_pay_balance_with_penalty():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"


def test_settled():
    assert refund_status(5000, 5000, True) == "settled"
