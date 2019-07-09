from unittest import TestCase

from onemsdk.model import FormTag
from onemsdk.parser import build_node
from onemsdk.schema.v1.component import Form


class TestModel(TestCase):
    def test_model(self):
        filename = 'index.html'
        with open(filename, mode="r") as f:
            html = f.read()
            node = build_node(html)
            tag = FormTag.from_node(node)
            schema = Form.from_tag(tag)
            print(schema.json(indent=2))
