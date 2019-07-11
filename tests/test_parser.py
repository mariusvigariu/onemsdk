from unittest import TestCase

from onemsdk.parser.util import build_node, _load_template


class TestParser(TestCase):
    def test_build_node_small(self):
        html = """
        <form>
          <section>
            <header>Header</header>
            <ul>
              <li>as</li>
            </ul>
          </section>
          
          <section>
            <p>text line</p>
            <input name="input-name" type="text" />
          </section>
        </form>
        
        """
        node = build_node(html)

        self.assertEqual('form', node.tag)

        self.assertEqual(2, len(node.children))

        self.assertEqual('text line', node.children[1].children[0].children[0])

        self.assertEqual(2, len(node.children[1].children[1].attrs.keys()))

        self.assertEqual('input-name', node.children[1].children[1].attrs['name'])

    def test_build_node_big(self):
        filename = 'index.html'
        with open(filename, mode="r") as f:
            html = f.read()
            node = build_node(html)

        self.assertEqual(3, len(node.children))

        first_section = node.children[0]
        self.assertEqual('section', first_section.tag)
        self.assertEqual(3, len(first_section.children))

        first_header = first_section.children[0]
        self.assertEqual('header', first_header.tag)
        self.assertEqual(1, len(first_header.children))
        self.assertEqual('Header section 1', first_header.children[0])

        second_section = node.children[1]
        self.assertEqual('section', second_section.tag)
        self.assertEqual(3, len(second_section.children))

        first_list = second_section.children[1]
        self.assertEqual('ul', first_list.tag)
        self.assertEqual(4, len(first_list.children))

        second_separator = first_list.children[3]
        self.assertEqual('li', second_separator.tag)
        self.assertEqual(1, len(second_separator.children))
        self.assertEqual('Separator 2 section 2', second_separator.children[0])

        second_item = first_list.children[2]
        self.assertEqual('li', second_item.tag)
        self.assertEqual(1, len(second_item.children))
        self.assertEqual('a', second_item.children[0].tag)
        self.assertEqual(1, len(second_item.children[0].children))
        self.assertEqual('Option 2 section 2', second_item.children[0].children[0])
        self.assertEqual('/route-2', second_item.children[0].attrs['href'])

        third_section = node.children[2]
        self.assertEqual('section', third_section.tag)
        self.assertEqual(4, len(third_section.children))

        second_paragraph = third_section.children[3]
        self.assertEqual('p', second_paragraph.tag)
        self.assertEqual(1, len(second_paragraph.children))
        self.assertEqual('Paragraph 2 section 3', second_paragraph.children[0])

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
        rendered_html = _load_template('index.j2', **data)
        with open('index.html', mode='r') as f:
            html = f.read()

        self.assertEqual(html, rendered_html)
