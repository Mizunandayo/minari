from app.services.delivery.delivery import parse_mr


def test_parse_json():
    iid, url = parse_mr('{"iid": 42, "web_url": "https://gitlab.com/g/p/-/merge_requests/42"}')
    assert iid == 42 and url.endswith("/merge_requests/42")


def test_parse_stringified_iid():
    # @zereight/mcp-gitlab returns ids as strings: "iid": "1" (the real shape
    # that broke the first live MR). Both the JSON and regex paths must coerce it.
    raw = '{"id": "493279325", "iid": "1", "web_url": "https://gitlab.com/g/p/-/merge_requests/1"}'
    iid, url = parse_mr(raw)
    assert iid == 1 and url.endswith("/merge_requests/1")


def test_parse_prose():
    iid, url = parse_mr("Created MR !7. View at https://gitlab.com/g/p/-/merge_requests/7")
    assert iid == 7 and url.endswith("/merge_requests/7")


def test_parse_garbage():
    assert parse_mr("nope") == (None, None)