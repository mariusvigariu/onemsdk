from __future__ import annotations

import inspect
import sys
from abc import ABC, abstractmethod
from typing import List, Union, Type, Optional, Tuple

from pydantic import BaseModel

from exceptions import NodeTagMismatchException, ONEmSDKException
from .node import Node

__all__ = ['Tag', 'HeaderTag', 'FooterTag', 'BrTag', 'UlTag', 'LiTag', 'FormTag',
           'SectionTag', 'InputTagAttrs', 'InputTag', 'FormTagAttrs', 'PTag', 'ATag',
           'ATagAttrs', 'get_tag_cls']


class Tag(BaseModel, ABC):
    children: List[Union[Tag, str]]

    def __init__(self, **data):
        children: List[Union[Tag, str]] = data.pop('children', None) or []

        min_children, max_children = self.Config.children_count

        if min_children is None:
            min_children = 0
        if max_children is None:
            max_children = 1000

        if not min_children <= len(children) <= max_children:
            if min_children == max_children:
                error = (f'<{self.Config.tag_name}> must have {min_children} children. '
                         f'Children: {len(children)}')
            else:
                error = (f'<{self.Config.tag_name}> must have between {min_children} '
                         f'and {max_children} children. Children: {len(children)}')
            raise ONEmSDKException(error)

        supported_children_types = tuple(self.Config.children_types)

        if children:
            for child in children:
                if not isinstance(child, supported_children_types):
                    raise ONEmSDKException(
                        f'<{child.Config.tag_name}> cannot be child for <{self.Config.tag_name}>')
        else:
            if supported_children_types:
                raise ONEmSDKException(f'<{self.Config.tag_name}> cannot be empty')

        super(Tag, self).__init__(**data, children=children)

    @abstractmethod
    def render(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_node(cls: Type[Tag], node: Node) -> Tag:
        pass

    class Config:
        can_be_root: bool = False
        tag_name: str = None
        children_types: List[Union[Type[Tag], Type[str]]] = None
        children_count: Tuple[int, int] = None


class HeaderTag(Tag):
    def render(self):
        return self.children[0] + '\n'

    @classmethod
    def from_node(cls, node: Node) -> HeaderTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)

    class Config:
        can_be_root: bool = False
        tag_name = 'header'
        children_types = [str]
        children_count = (1, 1)


HeaderTag.update_forward_refs()


class FooterTag(Tag):

    def render(self):
        return self.children[0]

    @classmethod
    def from_node(cls, node: Node) -> FooterTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)

    class Config:
        can_be_root: bool = False
        tag_name = 'footer'
        children_types = [str]
        children_count = (1, 1)


FooterTag.update_forward_refs()


class InputTagAttrs(BaseModel):
    name: str
    type: str


class InputTag(Tag):
    attrs: InputTagAttrs

    def render(self):
        return ''

    @classmethod
    def from_node(cls, node: Node) -> InputTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')
        attrs = InputTagAttrs(**node.attrs)
        return cls(attrs=attrs, children=node.children)

    class Config:
        can_be_root: bool = False
        tag_name = 'input'
        children_types = []
        children_count = (0, 0)


InputTag.update_forward_refs()


class ATagAttrs(BaseModel):
    href: str


class ATag(Tag):
    attrs = ATagAttrs

    def render(self):
        return self.children[0]

    @classmethod
    def from_node(cls, node: Node) -> ATag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')
        attrs = ATagAttrs(**node.attrs)
        children = node.children.copy()
        return cls(attrs=attrs, children=children)

    class Config:
        can_be_root: bool = False
        tag_name = 'a'
        children_types = [str]
        children_count = (1, 1)


ATag.update_forward_refs()


class LiTag(Tag):
    def render(self):
        if isinstance(self.children[0], ATag):
            return self.children[0].render() + '\n'
        return self.children[0] + '\n'

    @classmethod
    def from_node(cls, node: Node) -> LiTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')

        children: List[Union[ATag, str]] = []

        for node_child in node.children:
            if isinstance(node_child, str):
                children.append(node_child)
            elif isinstance(node_child, Node):
                tag_cls = get_tag_cls(node_child.tag)
                tag_obj = tag_cls.from_node(node_child)
                children.append(tag_obj)
            else:
                raise Exception(f'Unknown node type: {type(node)}')
        return cls(children=children)

    class Config:
        can_be_root: bool = False
        tag_name = 'li'
        children_types = [ATag, str]
        children_count = (1, 1)


LiTag.update_forward_refs()


class UlTag(Tag):
    def render(self):
        return ''.join([child.render() for child in self.children])

    @classmethod
    def from_node(cls, node: Node) -> UlTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')

        children = [get_tag_cls(child.tag).from_node(child) for child in node.children]
        return cls(children=children)

    class Config:
        can_be_root: bool = False
        tag_name = 'ul'
        children_types = [LiTag]
        children_count = (1, None)


UlTag.update_forward_refs()


class PTag(Tag):
    def render(self):
        return f'{self.children[0]}\n'

    @classmethod
    def from_node(cls, node: Node) -> PTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)

    class Config:
        can_be_root: bool = False
        tag_name = 'p'
        children_types = [str]
        children_count = (1, 1)


PTag.update_forward_refs()


class BrTag(Tag):

    def render(self):
        return '\n'

    @classmethod
    def from_node(cls, node: Node) -> BrTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')
        return cls(children=node.children)

    class Config:
        can_be_root: bool = False
        tag_name = 'br'
        children_types = []
        children_count = (0, 0)


BrTag.update_forward_refs()


class SectionTag(Tag):
    def __init__(self, **data):
        super(SectionTag, self).__init__(**data)
        children = data['children']

        header_pos = [t[0] for t in enumerate(children) if isinstance(t[1], HeaderTag)]
        if len(header_pos) > 1:
            raise ONEmSDKException('1 <header> per <section> permitted')
        if header_pos and header_pos[0] != 0:
            raise ONEmSDKException('<header> must be first in a <section>')

        footer_pos = [t[0] for t in enumerate(children) if isinstance(t[1], FooterTag)]
        if len(footer_pos) > 1:
            raise ONEmSDKException('1 <footer> per <section> permitted')
        if footer_pos and footer_pos[0] != len(children) - 1:
            raise ONEmSDKException('<footer> must be last in a <section>')

        if len(children) - len(header_pos) - len(footer_pos) < 1:
            raise ONEmSDKException('<section> must contain a body')

    def render(self):
        rendered_children = []
        for child in self.children:
            if isinstance(child, str):
                rendered_children.append(child)
            else:
                rendered_children.append(child.render())
        return ''.join(rendered_children)

    @classmethod
    def from_node(cls, node: Node) -> SectionTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')

        tag_children: List[Union[Tag, str]] = []

        for node_child in node.children:
            if isinstance(node_child, str):
                tag_children.append(node_child)
            else:
                tag_cls = get_tag_cls(node_child.tag)
                tag_child = tag_cls.from_node(node_child)
                tag_children.append(tag_child)
        return cls(children=tag_children)

    class Config:
        can_be_root = True
        tag_name = 'section'
        children_types = [FooterTag, HeaderTag, UlTag, PTag, InputTag, BrTag, str]
        children_count = (1, None)


SectionTag.update_forward_refs()


class FormTagAttrs(BaseModel):
    data_route: Optional[str]
    data_method: Optional[str]
    data_type: Optional[str]


class FormTag(Tag):
    attrs: FormTagAttrs

    def render(self):
        return '\n'.join([child.render() for child in self.children])

    @classmethod
    def from_node(cls, node: Node) -> FormTag:
        if node.tag != cls.Config.tag_name:
            raise NodeTagMismatchException(
                f'Expected tag <{cls.Config.tag_name}>, received <{node.tag}>')
        children = [get_tag_cls(child.tag).from_node(child) for child in node.children]
        attrs = FormTagAttrs(**node.attrs)
        return cls(children=children, attrs=attrs)

    class Config:
        can_be_root = True
        tag_name = 'form'
        children_types = [SectionTag]
        children_count = (1, None)


FormTag.update_forward_refs()

_map_tag_cls = {}

for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, Tag):
        _map_tag_cls[obj.Config.tag_name] = obj


def get_tag_cls(tag_name: str) -> Type[Tag]:
    global _map_tag_cls

    try:
        return _map_tag_cls[tag_name]
    except KeyError:
        raise ONEmSDKException(f'Tag <{tag_name}> is not supported')
