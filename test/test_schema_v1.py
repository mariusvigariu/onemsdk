import json
from unittest import TestCase

from onemsdk.model import FormTag
from onemsdk.parser import build_node, load_html
from onemsdk.schema.v1 import Form, Response


class TestModel(TestCase):
    def test_model(self):
        filename = 'index.html'
        with open(filename, mode="r") as f:
            html = f.read()
            node = build_node(html)
            tag = FormTag.from_node(node)
            schema = Form.from_tag(tag)
            print(schema.json(indent=2))

    def test_response(self):
        html = """
        <section>
          <header>my menu</header>
          <ul>
            <li>
              <a href="/callback-url/item1" method="GET">First item</a>
            </li>
            <li>
              <a href="/callback-url/item2" method="GET">Second item</a>
            </li>
            <li>
              <a href="/callback-url/item3" method="POST">Third item</a>
            </li>
          </ul>
          <footer>my footer</footer>
        </section>
        """
        tag = load_html(html_str=html)
        js = Response.from_tag(tag, message_id='asdf').dict()
        print(json.dumps(js, indent=2))
