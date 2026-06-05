from app.services.fixes.assertions import assertions_preserved

ORIGINAL = (
    "def test_x():\n"
    "    result = compute()\n"
    "    assert result == 3\n"
)



def test_preserved_when_assertion_unchanged():
    fixed = (
        "import threading\n"
        "def test_x():\n"
        "    with lock:\n"
        "        result = compute()\n"
        "    assert result == 3\n"
    )
    assert assertions_preserved("python", ORIGINAL, fixed) is True




def test_rejected_when_assertion_weakened():
    fixed = (
        "def test_x():\n"
        "    result = compute()\n"
        "    assert result in (2, 3)\n"   
    )
    assert assertions_preserved("python", ORIGINAL, fixed) is False

def test_rejected_when_assertion_removed():
    fixed = "def test_x():\n    result = compute()\n"
    assert assertions_preserved("python", ORIGINAL, fixed) is False

def test_adding_assertions_is_allowed():
    fixed = ORIGINAL + "    assert result > 0\n"
    assert assertions_preserved("python", ORIGINAL, fixed) is True