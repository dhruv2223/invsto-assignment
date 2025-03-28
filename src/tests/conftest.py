import pytest
import coverage
import os

@pytest.fixture(autouse=True)
def setup_coverage():
    cov = coverage.Coverage()
    cov.start()
    yield
    cov.stop()
    cov.save()
    # Ensure minimum 80% coverage
    coverage_percentage = cov.report()
    assert coverage_percentage >= 80, f"Coverage {coverage_percentage}% is below required 80%" 
