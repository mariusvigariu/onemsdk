import json
from unittest import TestCase

from onemsdk.parser import SectionTag
from onemsdk.parser.util import load_html
from onemsdk.schema.v1 import Response


class TestModel(TestCase):
    def test_index_html(self):
        filename = 'index.html'
        root_tag = load_html(html_file=filename)
        response = Response.from_tag(root_tag)
        expected = {
            'content_type': 'form',
            'content': {
                'type': 'form',
                'body': [
                    {
                        'type': 'string',
                        'name': 'first-step',
                        'description': 'Paragraph 1 section 1',
                        'header': 'Header section 1',
                        'footer': 'Footer section 1'
                    },
                    {
                        'type': 'form-menu',
                        'body': [
                            {
                                'type': 'content',
                                'description': 'Separator 1 section 2',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Option 1 section 2',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Option 2 section 2',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Separator 2 section 2',
                                'value': None
                            }
                        ],
                        'name': 'second-step',
                        'header': 'Header section 2',
                        'footer': 'Footer section 2'
                    },
                    {
                        'type': 'form-menu',
                        'body': [
                            {
                                'type': 'content',
                                'description': 'Paragraph 1 section 3',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Option 1 section 3',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Option 2 section 3',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Option 3 section 3',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Separator 1 section 3',
                                'value': None
                            },
                            {
                                'type': 'content',
                                'description': 'Paragraph 2 section 3',
                                'value': None
                            }
                        ],
                        'name': 'third-step',
                        'header': 'Header section 3',
                        'footer': None
                    }
                ],
                'method': 'POST',
                'path': '/path-1',
                'header': 'Parent header',
                'footer': None,
                'meta': {
                    'completion_status_show': None,
                    'completion_status_in_header': None,
                    'confirmation_needed': None
                },
            }}
        self.assertEqual(json.dumps(expected), response.json())

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
        response = Response.from_tag(tag)
        expected = {
            "content_type": "menu",
            "content": {
                "type": "menu",
                "body": [
                    {
                        "type": "option",
                        "description": "First item",
                        "method": "GET",
                        "path": "/callback-url/item1"
                    },
                    {
                        "type": "option",
                        "description": "Second item",
                        "method": "GET",
                        "path": "/callback-url/item2"
                    },
                    {
                        "type": "option",
                        "description": "Third item",
                        "method": "POST",
                        "path": "/callback-url/item3"
                    }
                ],
                "header": "my menu",
                "footer": "my footer"
            }
        }
        self.assertEqual(json.dumps(expected), response.json())

    def test_response_with_navigable_menu_from_html_text(self):
        html = '''
        <section header="Some header" footer="Some footer" name="some-name" expected-response="option">
           <ul>
               <li><a href="/route1" method="POST">Route 1</a></li>
               <li><a href="/route2">Route 2</a></li>
               <li>Separator</li>
               <li><a href="/route3">Route 3</a></li>
           </ul>
        </section>
        '''
        rootTag: SectionTag = load_html(html_str=html)
        response = Response.from_tag(rootTag)
        expected = {
            "content_type": "menu",
            "content": {
                "type": "menu",
                "body": [{
                    "type": "option",
                    "description": "Route 1",
                    "method": "POST",
                    "path": "/route1"
                }, {
                    "type": "option",
                    "description": "Route 2",
                    "method": 'GET',
                    "path": "/route2"
                }, {
                    "type": "content",
                    "description": "Separator",
                    "method": None,
                    "path": None
                }, {
                    "type": "option",
                    "description": "Route 3",
                    "method": 'GET',
                    "path": "/route3"
                }],
                "header": "Some header",
                "footer": "Some footer"
            }
        }

        self.assertEqual(json.dumps(expected), response.json())

    def test_response_header_and_footer_recognized_as_children_and_attrs(self):
        html = """
            <section header="header attr" footer="footer attr">
                <p></p>
            </section>
        """
        rootTag: SectionTag = load_html(html_str=html)
        response = Response.from_tag(rootTag)
        expected = {
            "content_type": "menu",
            "content": {
                "type": "menu",
                "body": [],
                "header": "header attr",
                "footer": "footer attr"
            }
        }
        self.assertEqual(json.dumps(expected), response.json())

        html = """
            <section>
                <header>header child</header>
                <footer>footer child</footer>
            </section>
        """
        rootTag: SectionTag = load_html(html_str=html)
        response = Response.from_tag(rootTag)
        expected = {
            "content_type": "menu",
            "content": {
                "type": "menu",
                "body": [],
                "header": "header child",
                "footer": "footer child"
            }
        }
        self.assertEqual(json.dumps(expected), response.json())

    def test_response_ignore_attrs_header_and_footer_if_present_in_children(self):
        html = """
            <section header="header attr" footer="footer attr">
                <header>header child</header>
            </section>
        """
        root_tag = load_html(html_str=html)
        response = Response.from_tag(root_tag)
        expected = {
            "content_type": "menu",
            "content": {
                "type": "menu",
                "body": [],
                "header": "header child",
                "footer": "footer attr"
            }
        }
        self.assertEqual(json.dumps(expected), response.json())

    def test_response_from_html_file_form(self):
        filename = 'form-big.html'
        root_tag = load_html(html_file=filename)
        response = Response.from_tag(root_tag)
        expected = {
            "content_type": "form",
            "content": {
                "type": "form",
                "body": [
                    {
                        "type": "string",
                        "name": "step1",
                        "description": "What is your name?",
                        "header": "SETUP NAME",
                        "footer": "Reply with text"
                    }, {
                        "type": "form-menu",
                        "body": [{
                            "type": "content",
                            "description": "Choose your city:",
                            "value": None
                        }, {
                            "type": "content",
                            "description": "UK",
                            "value": None
                        }, {
                            "type": "option",
                            "description": "London",
                            "value": "london"
                        }, {
                            "type": "option",
                            "description": "Manchester",
                            "value": "manchester"
                        }, {
                            "type": "content",
                            "description": "FR",
                            "value": None
                        }, {
                            "type": "option",
                            "description": "Paris",
                            "value": "paris"
                        }, {
                            "type": "option",
                            "description": "Nice",
                            "value": "nice"
                        }],
                        "name": "step2",
                        "header": "SETUP CITY",
                        "footer": "Reply A-D",
                    }],
                "method": "POST",
                "path": "/route",
                "header": "Form header",
                "footer": "Form footer",
                "meta": {
                    "completion_status_show": None,
                    "completion_status_in_header": None,
                    "confirmation_needed": None
                }
            }
        }
        self.assertEqual(json.dumps(expected), response.json())

    def test_response_from_html_form(self):
        html = """
            <form header="Form header" confirmation-needed="true" method="PATCH" action="/route">
                <section name="step1">
                   <ul>
                       <li value="first">First item</li>
                       <li value="second">Second item</li>
                   </ul>
                </section>
                <section name="step2">
                   <label>A question</label>
                   <input type="date"/>
                </section>
            </form>
        """
        root_tag = load_html(html_str=html)
        response = Response.from_tag(root_tag)
        expected = {
            "content_type": "form",
            "content": {
                "type": "form",
                "body": [
                    {
                        "type": "form-menu",
                        "body": [
                            {
                                "type": "option",
                                "description": "First item",
                                "value": "first"
                            },
                            {
                                "type": "option",
                                "description": "Second item",
                                "value": "second"
                            }
                        ],
                        "name": "step1",
                        "header": None,
                        "footer": None,
                    },
                    {
                        "type": "date",
                        "name": "step2",
                        "description": "A question",
                        "header": None,
                        "footer": None
                    }
                ],
                "method": "PATCH",
                "path": "/route",
                "header": "Form header",
                "footer": None,
                "meta": {
                    "completion_status_show": None,
                    "completion_status_in_header": None,
                    "confirmation_needed": True
                }
            }
        }

        self.assertEqual(json.dumps(expected), response.json())
