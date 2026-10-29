import pytest
from income_tax import taxable_income, tax_due, refund_status


# =====================================================
# taxable_income
# =====================================================
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_negative_income_raises():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_zero_income_is_valid():
    # boundary: gross == 0 is NOT < 0, so no exception; result clamped to 0
    assert taxable_income(0, "new", 0) == 0


def test_old_regime_investments_capped():
    # investments > 150000 -> True branch of the cap
    assert taxable_income(1000000, "old", 200000) == 800000


def test_old_regime_investments_below_cap():
    # investments <= 150000 -> False branch of the cap (previously missed)
    assert taxable_income(1000000, "old", 100000) == 850000


def test_old_regime_investments_exactly_at_cap():
    # boundary: 150000 is NOT > 150000, so it is used as-is
    assert taxable_income(1000000, "old", 150000) == 800000


def test_unknown_regime_raises():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "foo", 0)


def test_taxable_income_clamped_to_zero_new():
    assert taxable_income(50000, "new", 0) == 0


def test_taxable_income_clamped_to_zero_old():
    assert taxable_income(100000, "old", 100000) == 0


def test_taxable_income_exactly_zero_not_clamped():
    # boundary: gross == deduction -> taxable == 0, takes the "return taxable" path
    assert taxable_income(75000, "new", 0) == 0


# =====================================================
# tax_due
# =====================================================
def test_below_exemption():
    assert tax_due(200000, 30) == 0


def test_negative_taxable_raises():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-100, 30)


def test_zero_taxable_is_valid():
    assert tax_due(0, 30) == 0


# --- age group boundaries ---
def test_age_80_is_super_senior():
    assert tax_due(500000, 80) == 0
    assert tax_due(600000, 80) == 5000


def test_age_79_is_senior():
    assert tax_due(400000, 79) == 5000


def test_age_60_is_senior():
    assert tax_due(300000, 60) == 0
    assert tax_due(400000, 60) == 5000


def test_age_59_is_regular():
    assert tax_due(400000, 59) == 7500


# --- exemption / slab boundaries ---
def test_exactly_at_exemption_limit():
    assert tax_due(250000, 30) == 0


def test_just_above_exemption_limit():
    assert tax_due(250001, 30) == 0  # 1 * 5 // 100 == 0 (integer division)


def test_exactly_at_first_slab_limit():
    # slab == 250000 -> still 5%
    assert tax_due(500000, 30) == 12500


def test_just_above_first_slab_limit():
    # slab == 250001 -> 12500 + 1*20//100 == 12500
    assert tax_due(500001, 30) == 12500


def test_second_slab():
    assert tax_due(600000, 30) == 32500


def test_second_slab_senior():
    # exempt 300000, slab 400000 -> 12500 + 150000*20% = 42500
    assert tax_due(700000, 65) == 42500


# =====================================================
# refund_status
# =====================================================
def test_refund_on_time():
    assert refund_status(10000, 5000, True) == "refund"


def test_refund_delayed():
    assert refund_status(10000, 5000, False) == "refund delayed"


def test_pay_balance_on_time():
    assert refund_status(5000, 10000, True) == "pay balance"


def test_pay_balance_with_penalty():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"


def test_settled_on_time():
    assert refund_status(5000, 5000, True) == "settled"


def test_settled_late():
    # difference == 0 settles regardless of filing time
    assert refund_status(5000, 5000, False) == "settled"
