"""
Lab 6: Branch Coverage Test Cases
Student Name: R P Pranav
SRN: PES2UG24CS917
Application: Income Tax Calculator (income_tax.py)

This test suite comprehensively tests all decision outcomes, edge cases,
and boundary conditions for every branch in income_tax.py:
- taxable_income: gross validation, regime branches ("new", "old", invalid),
  investment cap branch (> 150000 vs <= 150000), taxable floor (< 0 vs >= 0)
- tax_due: taxable validation, age tiers (super senior >= 80, senior >= 60, regular < 60),
  exemption threshold (<= exempt vs > exempt), tax slabs (<= 250000 vs > 250000)
- refund_status: positive difference (on-time vs delayed), negative difference
  (on-time vs penalty), zero difference (settled)

Achieves 100% Statement Coverage and 100% Branch Coverage (28/28 branches).
"""

import pytest
from income_tax import taxable_income, tax_due, refund_status


# ============================================================================
# Starter example tests from repository
# ============================================================================
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_below_exemption():
    assert tax_due(200000, 30) == 0


# ============================================================================
# Branch Coverage Tests for taxable_income(gross, regime, investments)
# ============================================================================
def test_taxable_income_negative_gross():
    """Branch: gross < 0 evaluates to True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_taxable_income_new_regime_positive():
    """Branch: regime == 'new' and taxable >= 0."""
    # gross = 800000, deduction = 75000 -> taxable = 725000
    assert taxable_income(800000, "new", 0) == 725000


def test_taxable_income_old_regime_investments_above_limit():
    """Branch: regime == 'old' and investments > 150000 (Branch True: 7 -> 8)."""
    # investments capped at 150000; deduction = 50000 + 150000 = 200000
    # taxable = 600000 - 200000 = 400000
    assert taxable_income(600000, "old", 200000) == 400000


def test_taxable_income_old_regime_investments_within_limit():
    """Branch: regime == 'old' and investments <= 150000 (Branch False: 7 -> 9)."""
    # investments = 100000; deduction = 50000 + 100000 = 150000
    # taxable = 500000 - 150000 = 350000
    assert taxable_income(500000, "old", 100000) == 350000


def test_taxable_income_old_regime_exact_investment_limit():
    """Boundary test: investments == 150000 (Branch False: 7 -> 9)."""
    # investments = 150000; deduction = 50000 + 150000 = 200000
    assert taxable_income(400000, "old", 150000) == 200000


def test_taxable_income_unknown_regime():
    """Branch: regime not 'new' and not 'old' (else branch raises ValueError)."""
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "corporate", 0)


def test_taxable_income_negative_taxable_floor():
    """Branch: taxable < 0 evaluates to True (returns 0)."""
    # gross = 50000, deduction = 75000 -> 50000 - 75000 = -25000 < 0 -> returns 0
    assert taxable_income(50000, "new", 0) == 0


def test_taxable_income_exact_zero_taxable():
    """Boundary test: gross == deduction -> taxable == 0 (Branch False: 13 -> 15)."""
    # gross = 75000, deduction = 75000 -> taxable = 0
    assert taxable_income(75000, "new", 0) == 0


# ============================================================================
# Branch Coverage Tests for tax_due(taxable, age)
# ============================================================================
def test_tax_due_negative_taxable():
    """Branch: taxable < 0 evaluates to True (raises ValueError)."""
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-50, 25)


def test_tax_due_super_senior_above_slab():
    """Branch: age >= 80 (exempt = 500000) and slab > 250000."""
    # taxable = 850000, exempt = 500000 -> slab = 350000
    # tax = 12500 + (350000 - 250000) * 20 // 100 = 12500 + 20000 = 32500
    assert tax_due(850000, 85) == 32500


def test_tax_due_super_senior_below_slab():
    """Branch: age >= 80 (exempt = 500000) and slab <= 250000."""
    # taxable = 600000, exempt = 500000 -> slab = 100000 <= 250000
    # tax = 100000 * 5 // 100 = 5000
    assert tax_due(600000, 80) == 5000


def test_tax_due_senior_citizen_below_slab():
    """Branch: 60 <= age < 80 (exempt = 300000) and slab <= 250000."""
    # taxable = 450000, exempt = 300000 -> slab = 150000 <= 250000
    # tax = 150000 * 5 // 100 = 7500
    assert tax_due(450000, 65) == 7500


def test_tax_due_senior_citizen_above_slab():
    """Branch: 60 <= age < 80 (exempt = 300000) and slab > 250000."""
    # taxable = 650000, exempt = 300000 -> slab = 350000 > 250000
    # tax = 12500 + (350000 - 250000) * 20 // 100 = 32500
    assert tax_due(650000, 60) == 32500


def test_tax_due_regular_age_above_slab():
    """Branch: age < 60 (exempt = 250000) and slab > 250000."""
    # taxable = 600000, exempt = 250000 -> slab = 350000 > 250000
    # tax = 12500 + (350000 - 250000) * 20 // 100 = 32500
    assert tax_due(600000, 45) == 32500


def test_tax_due_regular_age_below_slab():
    """Branch: age < 60 (exempt = 250000) and slab <= 250000."""
    # taxable = 350000, exempt = 250000 -> slab = 100000 <= 250000
    # tax = 100000 * 5 // 100 = 5000
    assert tax_due(350000, 35) == 5000


def test_tax_due_exact_exemption_boundary():
    """Boundary test: taxable == exempt (Branch: taxable <= exempt is True)."""
    # exempt = 250000 for age 30; tax = 0
    assert tax_due(250000, 30) == 0


def test_tax_due_exact_slab_boundary():
    """Boundary test: slab == 250000 (Branch: slab <= 250000 is True)."""
    # exempt = 250000, taxable = 500000 -> slab = 250000
    # tax = 250000 * 5 // 100 = 12500
    assert tax_due(500000, 30) == 12500


# ============================================================================
# Branch Coverage Tests for refund_status(tax_paid, tax_due_amount, filed_on_time)
# ============================================================================
def test_refund_status_positive_diff_on_time():
    """Branch: difference > 0 and filed_on_time == True -> 'refund'."""
    assert refund_status(50000, 40000, True) == "refund"


def test_refund_status_positive_diff_delayed():
    """Branch: difference > 0 and filed_on_time == False -> 'refund delayed'."""
    assert refund_status(50000, 40000, False) == "refund delayed"


def test_refund_status_negative_diff_on_time():
    """Branch: difference < 0 and filed_on_time == True -> 'pay balance'."""
    assert refund_status(30000, 40000, True) == "pay balance"


def test_refund_status_negative_diff_penalty():
    """Branch: difference < 0 and filed_on_time == False -> 'pay balance with penalty'."""
    assert refund_status(30000, 40000, False) == "pay balance with penalty"


def test_refund_status_settled():
    """Branch: difference == 0 (neither > 0 nor < 0) -> 'settled'."""
    assert refund_status(40000, 40000, True) == "settled"
    assert refund_status(40000, 40000, False) == "settled"
