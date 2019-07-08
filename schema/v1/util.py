from typing import Union

from exceptions import ONEmSDKException
from model.tag import SectionTag, FormTag
from schema.v1.component import Menu, Form


def create_response(tag: Union[SectionTag, FormTag]) -> dict:
    if isinstance(tag, SectionTag):
        return Menu.from_tag(tag).dict()
    if isinstance(tag, FormTag):
        return Form.from_tag(tag).dict()
    raise ONEmSDKException(f'Cannot create response from {tag} class')
