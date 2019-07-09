from unittest import TestCase

from onemsdk.schema import load_template


class TestUtil(TestCase):
    def test_load_template(self):
        data = {
            'li': {
                '2': {'data': 'opt-21'},
            },
            'section': {
                '3': {'name': 'third-step'}
            },
            'items': [
                {'data': 'opt-31', 'href': 'route-1', 'desc': 'Option 1 section 3'},
                {'data': 'opt-32', 'href': 'route-2', 'desc': 'Option 2 section 3'},
                {'data': 'opt-33', 'href': 'route-3', 'desc': 'Option 3 section 3'},
            ]
        }
        rendered_html = load_template('index.j2', **data)
        with open('index.html', mode='r') as f:
            html = f.read()

        self.assertEqual(html, rendered_html)
