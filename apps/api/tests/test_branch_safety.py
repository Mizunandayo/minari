import pytest

from app.services.validation.branch import (
    fix_branch_name,
    is_safe_node_name,
    is_safe_repo_path,
    safe_slug,
)


@pytest.mark.parametrize("path,ok", [
    ("tests/test_async_timing.py", True),
    ("src/a/b_test.go", True),
    ("../../etc/passwd", False),
    ("tests/x.py; rm -rf /", False),
    ("tests/x.txt", False),
    ("/abs/path.py", False),
])
def test_repo_path_validation(path, ok):
    assert is_safe_repo_path(path) is ok



@pytest.mark.parametrize("name,ok", [
    ("test_checkout", True),
    ("test_param[case-1]", True),
    ("test; curl evil", False),
    ("$(whoami)", False),
])



def test_node_name_validation(name, ok):
    assert is_safe_node_name(name) is ok


def test_branch_name_is_ref_safe():
    b = fix_branch_name("test Checkout Flow / concurrent!!", "1a2b3c4d-ffff")
    assert b.startswith("minari/fix-") and ".." not in b and " " not in b
    assert b.endswith("1a2b3c4d")


def test_slug_never_empty():
    assert safe_slug("!!!") == "test"
