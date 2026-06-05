import pytest
from pydantic import ValidationError

from app.schemas.fix import FixCandidate, FixCategory


def _valid() -> dict:
    return {"rank": 1, "fix_category": "isolate", "confidence": 0.88,
            "explanation": "Scope the table name per test invocation with a uuid suffix.",
            "fixed_source": "def test_x():\n    assert True\n"}


def test_parses_and_defaults():
    c = FixCandidate.model_validate(_valid())
    assert c.fix_category is FixCategory.ISOLATE
    assert c.syntax_valid is False and c.assertions_safe is False
    assert c.is_safe is False


def test_confidence_bounds():
    with pytest.raises(ValidationError):
        FixCandidate.model_validate({**_valid(), "confidence": 1.5})




