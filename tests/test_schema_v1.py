import json
import os
from unittest import TestCase

from pydantic import ValidationError

from onemsdk import set_static_dir
from onemsdk.exceptions import ONEmSDKException
from onemsdk.parser import SectionTag
from onemsdk.parser.util import load_html
from onemsdk.schema.v1 import Response, FormItem, FormItemType

set_static_dir(os.path.join(os.path.dirname(__file__), 'static'))


class TestModel(TestCase):
    def test_index_html(self):
        filename = 'index.html'
        root_tag = load_html(html_file=filename)
        response = Response.from_tag(root_tag)
        expected = {
            "content_type": "form",
            "content": {
                "type": "form",
                "body": [
                    {
                        "type": "string",
                        "name": "first-step",
                        "description": "Paragraph 1 section 1",
                        "header": "Header section 1",
                        "footer": "Footer section 1",
                        "body": None,
                        "value": None,
                        "chunking_footer": None,
                        "confirmation_label": None,
                        "min_length": None,
                        "min_length_error": None,
                        "max_length": None,
                        "max_length_error": None,
                        "min_value": None,
                        "min_value_error": None,
                        "max_value": None,
                        "max_value_error": None,
                        "meta": {
                            "auto_select": False,
                            "multi_select": False,
                            "numbered": False
                        },
                        "method": None,
                        "required": False,
                        "status_exclude": False,
                        "status_prepend": False,
                        "url": None,
                        "validate_type_error": None,
                        "validate_type_error_footer": None,
                        "validate_url": None
                    },
                    {
                        "type": "form-menu",
                        "name": "second-step",
                        "description": None,
                        "header": "Header section 2",
                        "footer": "Footer section 2",
                        "body": [
                            {
                                "type": "content",
                                "description": "Separator 1 section 2",
                                "value": None,
                                "text_search": None,
                            },
                            {
                                "type": "option",
                                "description": "Option 1 section 2",
                                "value": "opt-21",
                                "text_search": None,
                            },
                            {
                                "type": "option",
                                "description": "Option 2 section 2",
                                "value": "opt-22",
                                "text_search": None,
                            },
                            {
                                "type": "content",
                                "description": "Separator 2 section 2",
                                "value": None,
                                "text_search": None,
                            }
                        ],
                        "value": None,
                        "chunking_footer": None,
                        "confirmation_label": None,
                        "min_length": None,
                        "min_length_error": None,
                        "max_length": None,
                        "max_length_error": None,
                        "min_value": None,
                        "min_value_error": None,
                        "max_value": None,
                        "max_value_error": None,
                        "meta": {
                            "auto_select": False,
                            "multi_select": False,
                            "numbered": False
                        },
                        "method": None,
                        "required": False,
                        "status_exclude": False,
                        "status_prepend": False,
                        "url": None,
                        "validate_type_error": None,
                        "validate_type_error_footer": None,
                        "validate_url": None
                    },
                    {
                        "type": "form-menu",
                        "name": "third-step",
                        "description": None,
                        "header": "Header section 3",
                        "footer": None,
                        "body": [
                            {
                                "type": "content",
                                "description": "Paragraph 1 section 3",
                                "value": None,
                                "text_search": None,
                            },
                            {
                                "type": "option",
                                "description": "Option 1 section 3",
                                "value": "opt-31",
                                "text_search": "Context for option 1 section 3",
                            },
                            {
                                "type": "option",
                                "description": "Option 2 section 3",
                                "value": "opt-32",
                                "text_search": "Context for option 2 section 3",
                            },
                            {
                                "type": "option",
                                "description": "Option 3 section 3",
                                "value": "opt-33",
                                "text_search": "Context for option 3 section 3",
                            },
                            {
                                "type": "content",
                                "description": "Separator 1 section 3",
                                "value": None,
                                "text_search": None,
                            },
                            {
                                "type": "content",
                                "description": "Paragraph 2 section 3",
                                "value": None,
                                "text_search": None
                            }
                        ],
                        "value": None,
                        "chunking_footer": None,
                        "confirmation_label": None,
                        "min_length": None,
                        "min_length_error": None,
                        "max_length": None,
                        "max_length_error": None,
                        "min_value": None,
                        "min_value_error": None,
                        "max_value": None,
                        "max_value_error": None,
                        "meta": {
                            "auto_select": False,
                            "multi_select": False,
                            "numbered": False
                        },
                        "method": None,
                        "required": False,
                        "status_exclude": False,
                        "status_prepend": False,
                        "url": None,
                        "validate_type_error": None,
                        "validate_type_error_footer": None,
                        "validate_url": None
                    }
                ],
                "method": "POST",
                "path": "/path-1",
                "header": "Parent header",
                "footer": None,
                "meta": {
                    "completion_status_show": False,
                    "completion_status_in_header": False,
                    "confirmation_needed": False
                }
            }
        }
        self.assertEqual(json.dumps(expected, indent=2), response.json(indent=2))

    def test_response(self):
        html = """
        <section auto-select="True cause it's present">
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
                        "text_search": None,
                        "method": "GET",
                        "path": "/callback-url/item1"
                    },
                    {
                        "type": "option",
                        "description": "Second item",
                        "text_search": None,
                        "method": "GET",
                        "path": "/callback-url/item2"
                    },
                    {
                        "type": "option",
                        "description": "Third item",
                        "text_search": None,
                        "method": "POST",
                        "path": "/callback-url/item3"
                    }
                ],
                "header": "my menu",
                "footer": "my footer",
                "meta": {
                    "auto_select": True
                }
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
                "body": [
                    {
                        "type": "option",
                        "description": "Route 1",
                        "text_search": None,
                        "method": "POST",
                        "path": "/route1"
                    },
                    {
                        "type": "option",
                        "description": "Route 2",
                        "text_search": None,
                        "method": 'GET',
                        "path": "/route2"
                    },
                    {
                        "type": "content",
                        "description": "Separator",
                        "text_search": None,
                        "method": None,
                        "path": None
                    },
                    {
                        "type": "option",
                        "description": "Route 3",
                        "text_search": None,
                        "method": 'GET',
                        "path": "/route3"
                    }
                ],
                "header": "Some header",
                "footer": "Some footer",
                "meta": {
                    "auto_select": False
                }
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
                "footer": "footer attr",
                "meta": {
                    "auto_select": False
                }
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
                "footer": "footer child",
                "meta": {
                    "auto_select": False
                }
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
                "footer": "footer attr",
                "meta": {
                    "auto_select": False,
                }
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
                        "type": "float",
                        "name": "step1",
                        "description": "What is your height?",
                        "header": "SETUP HEIGHT",
                        "footer": "Reply with text",
                        "body": None,
                        "value": None,
                        "chunking_footer": None,
                        "confirmation_label": None,
                        "min_length": None,
                        "min_length_error": None,
                        "max_length": None,
                        "max_length_error": None,
                        "min_value": 0.5,
                        "min_value_error": "Are you a baby?",
                        "max_value": 2.5,
                        "max_value_error": "Too high",
                        "meta": {
                            "auto_select": False,
                            "multi_select": False,
                            "numbered": False
                        },
                        "method": None,
                        "required": True,
                        "status_exclude": False,
                        "status_prepend": False,
                        "url": None,
                        "validate_type_error": None,
                        "validate_type_error_footer": None,
                        "validate_url": None
                    },
                    {
                        "type": "form-menu",
                        "name": "step2",
                        "description": None,
                        "header": "SETUP CITY",
                        "footer": "Reply A-D",
                        "body": [
                            {
                                "type": "content",
                                "description": "Choose your city:",
                                "value": None,
                                "text_search": None,
                            },
                            {
                                "type": "content",
                                "description": "UK",
                                "value": None,
                                "text_search": None,
                            },
                            {
                                "type": "option",
                                "description": "London",
                                "value": "london",
                                "text_search": None,
                            },
                            {
                                "type": "option",
                                "description": "Manchester",
                                "value": "manchester",
                                "text_search": None,
                            },
                            {
                                "type": "content",
                                "description": "FR",
                                "value": None,
                                "text_search": None,
                            },
                            {
                                "type": "option",
                                "description": "Paris",
                                "value": "paris",
                                "text_search": None,
                            },
                            {
                                "type": "option",
                                "description": "Nice",
                                "value": "nice",
                                "text_search": None,
                            }
                        ],
                        "value": None,
                        "chunking_footer": None,
                        "confirmation_label": None,
                        "min_length": None,
                        "min_length_error": None,
                        "max_length": None,
                        "max_length_error": None,
                        "min_value": None,
                        "min_value_error": None,
                        "max_value": None,
                        "max_value_error": None,
                        "meta": {
                            "auto_select": True,
                            "multi_select": False,
                            "numbered": True
                        },
                        "method": None,
                        "required": True,
                        "status_exclude": False,
                        "status_prepend": False,
                        "url": None,
                        "validate_type_error": None,
                        "validate_type_error_footer": None,
                        "validate_url": None
                    }
                ],
                "method": "POST",
                "path": "/route",
                "header": "Form header",
                "footer": "Form footer",
                "meta": {
                    "completion_status_show": False,
                    "completion_status_in_header": True,
                    "confirmation_needed": False
                }
            }
        }
        self.assertEqual(json.dumps(expected), response.json())

    def test_response_from_html_form(self):
        html = """
            <form header="Form header" confirmation-needed method="PATCH" action="/route">
                <section name="step1" numbered required auto-select>
                    <p></p>
                    <ul>
                        <li value="first" text-search="Context for first item">First item</li>
                        <li value="second">Second item</li>
                    </ul>
                    <p></p>
                </section>
                <section name="step2" method="POST" confirmation-label="confirmation label" required>
                   <label>A question</label>
                   <input type="number" step="1" />
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
                        "name": "step1",
                        "description": None,
                        "header": None,
                        "footer": None,
                        "body": [
                            {
                                "type": "option",
                                "description": "First item",
                                "value": "first",
                                "text_search": "Context for first item",
                            },
                            {
                                "type": "option",
                                "description": "Second item",
                                "value": "second",
                                "text_search": None,
                            }
                        ],
                        "value": None,
                        "chunking_footer": None,
                        "confirmation_label": None,
                        "min_length": None,
                        "min_length_error": None,
                        "max_length": None,
                        "max_length_error": None,
                        "min_value": None,
                        "min_value_error": None,
                        "max_value": None,
                        "max_value_error": None,
                        "meta": {
                            "auto_select": True,
                            "multi_select": False,
                            "numbered": True
                        },
                        "method": None,
                        "required": True,
                        "status_exclude": False,
                        "status_prepend": False,
                        "url": None,
                        "validate_type_error": None,
                        "validate_type_error_footer": None,
                        "validate_url": None
                    },
                    {
                        "type": "int",
                        "name": "step2",
                        "description": "A question",
                        "header": None,
                        "footer": None,
                        "body": None,
                        "value": None,
                        "chunking_footer": None,
                        "confirmation_label": "confirmation label",
                        "min_length": None,
                        "min_length_error": None,
                        "max_length": None,
                        "max_length_error": None,
                        "min_value": None,
                        "min_value_error": None,
                        "max_value": None,
                        "max_value_error": None,
                        "meta": {
                            "auto_select": False,
                            "multi_select": False,
                            "numbered": False
                        },
                        "method": "POST",
                        "required": True,
                        "status_exclude": False,
                        "status_prepend": False,
                        "url": None,
                        "validate_type_error": None,
                        "validate_type_error_footer": None,
                        "validate_url": None
                    }
                ],
                "method": "PATCH",
                "path": "/route",
                "header": "Form header",
                "footer": None,
                "meta": {
                    "completion_status_show": False,
                    "completion_status_in_header": False,
                    "confirmation_needed": True
                }
            }
        }
        self.assertEqual(json.dumps(expected), response.json())


class TestFormItem(TestCase):
    def test_from_tag__should_raise_error_for_invalid_type(self):
        html = """
        <section name="name">
            <input type="blabla"/>
        </section>
        """

        with self.assertRaises(ValidationError) as context:
            section_tag = load_html(html_str=html)
            form_item = FormItem.from_tag(section_tag)

        self.assertIn(
            "value is not a valid enumeration member; permitted: 'text', 'date', 'number', 'hidden', 'email', 'url', 'datetime', 'location'",
            str(context.exception)
        )

    def test_from_tag__should_raise_error_if_type_hidden_and_no_value(self):
        html = """
        <section name="name">
            <input type="hidden"/>
        </section>
        """
        section_tag = load_html(html_str=html)

        with self.assertRaises(ONEmSDKException) as context:
            form_item = FormItem.from_tag(section_tag)

        self.assertIn('value attribute is required for input type="hidden"',
                      str(context.exception))

    def test_from_tag__should_correctly_parse_int_float_from_number(self):
        html = """
        <section name="name">
            <input type="number" step="1"/>
        </section>
        """
        section_tag = load_html(html_str=html)
        form_item = FormItem.from_tag(section_tag)
        self.assertEqual(form_item.type, FormItemType.int)

        html = """
        <section name="name">
            <input type="number"/>
        </section>
        """
        section_tag = load_html(html_str=html)
        form_item = FormItem.from_tag(section_tag)
        self.assertEqual(form_item.type, FormItemType.float)

    def test_from_tag__should_correctly_parse_complex_section_tag(self):
        html = """
        <section name="first-step"
                 header="The header"
                 footer="The footer"
                 chunking-footer="Chunking footer"
                 confirmation-label="Conf label"
                 method="PATCH"
                 status-exclude
                 url="https://url.url"
                 validate-type-error="The validate type err"
                 validate-type-error-footer="The val type err footer"
                 validate-url="The val url"
                 auto-select
                 numbered
                 required>
            <input type="email"
                   minlength="3"
                   minlength-error="The minlen error"
                   maxlength="100"
                   maxlength-error="The maxlen error" />
        </section>
        """
        section_tag = load_html(html_str=html)
        form_item = FormItem.from_tag(section_tag)
        expected = {
            "type": "email",
            "name": "first-step",
            "description": "",
            "header": "The header",
            "footer": "The footer",
            "body": None,
            "value": None,
            "chunking_footer": "Chunking footer",
            "confirmation_label": "Conf label",
            "min_length": 3,
            "min_length_error": "The minlen error",
            "max_length": 100,
            "max_length_error": "The maxlen error",
            "min_value": None,
            "min_value_error": None,
            "max_value": None,
            "max_value_error": None,
            "meta": {
                "auto_select": True,
                "multi_select": False,
                "numbered": True
            },
            "method": "PATCH",
            "required": True,
            "status_exclude": True,
            "status_prepend": False,
            "url": "https://url.url",
            "validate_type_error": "The validate type err",
            "validate_type_error_footer": "The val type err footer",
            "validate_url": "The val url"
        }
        self.assertEqual(json.dumps(expected), form_item.json())
