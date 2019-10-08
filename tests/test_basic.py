import unmock
import requests


def replyFn(request):
  if request.host == "www.example.com":
    name = request.qs.get("name", ["World"])
    s = "Hello {}!".format(name[0])
    return {"content": s, "status": 200, "headers": {"Content-Length": len(s)}}
  return {"status": 204, "content": {"foo": "bar"}}


def test_reply_fn():
  unmock.on(replyFn=replyFn)
  res = requests.get("https://www.example.com/?name=foo")
  assert res.text == "Hello foo!"
  assert res.headers.get("Content-Length") == str(len("Hello foo!"))
  unmock.off()


def test_context_manager():
  with unmock.patch(replyFn=replyFn):
    res = requests.get("https://www.example.com/")
    assert res.text == "Hello World!"
    assert res.headers.get("Content-Length") == str(len("Hello World!"))


def test_pytest_fixture(unmock_t):
  unmock_t(replyFn=replyFn)
  res = requests.get("https://www.example.com/?name=baz")
  assert res.text == "Hello baz!"
  assert res.headers.get("Content-Length") == str(len("Hello baz!"))


def test_json_content():
  unmock.on(replyFn=replyFn)
  res = requests.get("http://www.foo.com/")
  assert res.json() == {"foo": "bar"}
  unmock.off()
