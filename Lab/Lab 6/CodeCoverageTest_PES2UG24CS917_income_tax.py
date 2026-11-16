"""
Lab 6: Code Coverage Test Cases
Student Name: R P Pranav
SRN: PES2UG24CS917
Application: Income Tax Calculator (income_tax.py)

This test suite targets line (statement) coverage for all functions in income_tax.py:
- taxable_income
- tax_due
- refund_status
Achieves 100% statement (line) coverage.
"""

import pytest
from income_tax import taxable_income, tax_due, refund_status


# Starter example tests
def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_below_exemption():
    assert tax_due(200000, 30) == 0


# Test cases for line / statement coverage
def test_taxable_income_negative_gross():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_taxable_income_old_regime():
    # Covers old regime with capped investments (> 150000)
    # gross = 500000, investments = 200000 (capped at 150000)
    # deduction = 50000 + 150000 = 200000 -> taxable = 300000
    assert taxable_income(500000, "old", 200000) == 300000


def test_taxable_income_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(500000, "invalid_regime", 0)


def test_taxable_income_negative_result():
    # Gross is less than standard deduction (50000 - 75000 < 0 -> returns 0)
    assert taxable_income(50000, "new", 0) == 0


def test_tax_due_negative_taxable():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-100, 30)


def test_tax_due_super_senior():
    # age >= 80, slab > 250000
    # taxable = 800000, exempt = 500000 -> slab = 300000
    # tax = 12500 + (300000 - 250000) * 0.2 = 22500
    assert tax_due(800000, 85) == 22500


def test_tax_due_senior():
    # age >= 60, slab <= 250000
    # taxable = 400000, exempt = 300000 -> slab = 100000
    # tax = 100000 * 5 // 100 = 5000
    assert tax_due(400000, 65) == 5000


def test_refund_status_refund():
    # difference > 0, filed_on_time True
    assert refund_status(50000, 40000, True) == "refund"


def test_refund_status_refund_delayed():
    # difference > 0, filed_on_time False
    assert refund_status(50000, 40000, False) == "refund delayed"


def test_refund_status_pay_balance():
    # difference < 0, filed_on_time True
    assert refund_status(30000, 40000, True) == "pay balance"


def test_refund_status_pay_balance_with_penalty():
    # difference < 0, filed_on_time False
    assert refund_status(30000, 40000, False) == "pay balance with penalty"


def test_refund_status_settled():
    # difference == 0
    assert refund_status(40000, 40000, True) == "settled"
