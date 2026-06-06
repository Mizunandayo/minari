"""Lock the @zereight MCP response-format parsing the Validator depends on."""

from app.services.validation.pipeline import (
    _as_obj,
    _extract_pipeline_id,
    _extract_status,
    _parse_runs,
)

# create_pipeline returns prose, not JSON.
CREATE_PROSE = ("Created pipeline #2581527293 for minari/fix-x-c1. Status: created\n"
                "Web URL: https://gitlab.com/g/p/-/pipelines/2581527293")
# get_pipeline returns a JSON string with a STRINGIFIED id and a real status.
GET_JSON = '{"id": "2581527293", "status": "running", "duration": null}'
# list_pipeline_jobs returns a JSON array string; duration is seconds (or null).
JOBS_JSON = ('[{"name": "verify_1", "status": "success", "duration": 18.4},'
             ' {"name": "verify_2", "status": "failed", "duration": 19.1}]')


def test_extract_pipeline_id_from_prose():
    assert _extract_pipeline_id(CREATE_PROSE) == 2581527293


def test_extract_pipeline_id_from_json_string_id():
    assert _extract_pipeline_id(GET_JSON) == 2581527293


def test_extract_pipeline_id_none_when_absent():
    assert _extract_pipeline_id("nothing useful here") is None


def test_extract_status_from_json():
    assert _extract_status(GET_JSON) == "running"


def test_parse_runs_reads_status_and_duration():
    runs = _parse_runs(JOBS_JSON, runs=2)
    assert [r.passed for r in runs] == [True, False]
    assert runs[0].duration_ms == 18400.0       # seconds -> ms
    assert _as_obj(JOBS_JSON)[0]["name"] == "verify_1"
