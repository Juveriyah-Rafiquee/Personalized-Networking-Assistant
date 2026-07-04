from app.services import fact_checker

def test_fact_checker_returns_summary():
    summary = fact_checker.fact_check("Artificial Intelligence")
    assert isinstance(summary, str)
    assert len(summary) > 10