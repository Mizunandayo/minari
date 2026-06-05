import pytest

from app.services.fixes.syntax import is_syntax_valid


@pytest.mark.parametrize("grammar,src,ok", [
    ("python", "def f():\n    return 1\n", True),
    ("python", "def f(:\n    return\n", False),
    ("javascript", "test('x', () => { expect(1).toBe(1); });", True),
    ("go", "package p\nfunc f() {}\n", True),
])
def test_syntax(grammar, src, ok):
    assert is_syntax_valid(grammar, src) is ok