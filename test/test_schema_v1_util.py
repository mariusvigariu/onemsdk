import json
from unittest import TestCase

from onemsdk.schema.v1 import load_html
from onemsdk.schema.v1.util import create_response


class TestUtil(TestCase):
    def test_load_html(self):
        tag = load_html(html_file='index.html')
        assert tag.Config.tag_name == 'form'

    def test_create_response(self):
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
        js = create_response(tag)
        print(json.dumps(js, indent=2))
