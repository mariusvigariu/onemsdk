from typing import Union

from onemsdk.exceptions import ONEmSDKException
from onemsdk.model import SectionTag, FormTag
from onemsdk.parser import build_node, get_root_tag
from .component import Menu, Form


def load_html(*, html_file: str = None, html_str: str = None
              ) -> Union[SectionTag, FormTag]:
    if html_file:
        with open(html_file, 'r') as f:
            html_str = f.read()

    node = build_node(html_str)
    root_tag = get_root_tag(node)
    return root_tag


def create_response(tag: Union[SectionTag, FormTag]) -> dict:
    if isinstance(tag, SectionTag):
        return Menu.from_tag(tag).dict()
    if isinstance(tag, FormTag):
        return Form.from_tag(tag).dict()
    raise ONEmSDKException(f'Cannot create response from {tag} class')
