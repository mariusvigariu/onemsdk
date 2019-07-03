from __future__ import annotations

import inspect
import sys
from abc import ABC, abstractmethod
from typing import List, Union, Type, Optional, get_type_hints, Any

from pydantic import BaseModel, Schema, validator

from exceptions import NodeTagMismatchException, ONEmSDKException
from .node import Node

__all__ = ['Tag', 'HeaderTag', 'FooterTag', 'BrTag', 'UlTag', 'LiTag', 'FormTag',
           'SectionTag', 'InputTagAttrs', 'InputTag', 'FormTagAttrs', 'PTag', 'ATag',
           'ATagAttrs', 'get_tag_cls']


class Tag(BaseModel, ABC):
    _tag = None
    _root = False

    children: Optional[Any]

    @abstractmethod
    def render(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_node(cls: Type[Tag], node: Node) -> Tag:
        pass

    @validator('children', whole=True, pre=True)
    def validate_children_type(cls, children):
        children_annotations = get_type_hints(cls).get('children')
        types = []
        if len(children_annotations.__args__) == 1:
            arg = children_annotations.__args__[0]
            if hasattr(arg, '__origin__'):
                if arg.__origin__ == Union:
                    types.extend(arg.__args__)
                else:
                    raise Exception('Case not treated', arg)
            else:
                if issubclass(arg, (Tag, str)):
                    types.append(arg)
                else:
                    raise Exception('Another case not treated', arg)

        if types:
            for child in children:
                if isinstance(child, str):
                    if str not in types:
                        raise ValueError(f'text cannot be a child for <{cls._tag}>')
                elif isinstance(child, Tag):
                    child_cls = get_tag_cls(child.get_name())
                    if child_cls not in types:
                        raise ValueError(
                            f'<{child._tag}> cannot be a child for <{cls._tag}>')
                else:
                    raise Exception(f'Bad child type: {type(child)}')

        return children

    @classmethod
    def is_root(cls):
        return cls._root

    @classmethod
    def get_name(cls):
        return cls._tag


class HeaderTag(Tag):
    _tag = 'header'

    children: List[str]

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if len(v) == 1:
            return v
        raise ValueError(f'<{cls._tag}> tag must have 1 text child')

    @validator('children', whole=True, pre=True)
    def validate_children_type(cls, children):
        return super(HeaderTag, cls).validate_children_type(children)

    def render(self):
        return self.children[0] + '\n'

    @classmethod
    def from_node(cls, node: Node) -> HeaderTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)


HeaderTag.update_forward_refs()


class FooterTag(Tag):
    _tag = 'footer'

    children: List[str] = Schema(...)

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if len(v) == 1:
            return v
        raise ValueError(f'<{cls._tag}> must have 1 text child')

    def render(self):
        return self.children[0]

    @classmethod
    def from_node(cls, node: Node) -> FooterTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)


FooterTag.update_forward_refs()


class InputTagAttrs(BaseModel):
    name: str
    type: str


class InputTag(Tag):
    _tag = 'input'

    attrs: InputTagAttrs

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if not v:
            return None
        raise ValueError(f'<{cls._tag}> cannot have children')

    def render(self):
        return ''

    @classmethod
    def from_node(cls, node: Node) -> InputTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')
        attrs = InputTagAttrs(**node.attrs)
        return cls(attrs=attrs, children=node.children)


InputTag.update_forward_refs()


class ATagAttrs(BaseModel):
    href: str


class ATag(Tag):
    _tag = 'a'

    attrs = ATagAttrs
    children: List[str]

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if len(v) == 1:
            return v
        raise ValueError(f'<{cls._tag}> must have 1 text child')

    def render(self):
        return self.children[0]

    @classmethod
    def from_node(cls, node: Node) -> ATag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')
        attrs = ATagAttrs(**node.attrs)
        children = node.children.copy()
        return cls(attrs=attrs, children=children)


ATag.update_forward_refs()


class LiTag(Tag):
    _tag = 'li'

    children: List[Union[ATag, str]]
    spinach: Optional[str]

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if len(v) == 1:
            return v
        raise ValueError(f'<{cls._tag}> must have 1 child: text or <a>')

    def render(self):
        if isinstance(self.children[0], ATag):
            return self.children[0].render() + '\n'
        return self.children[0] + '\n'

    @classmethod
    def from_node(cls, node: Node) -> LiTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')

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


LiTag.update_forward_refs()


class UlTag(Tag):
    _tag = 'ul'

    children: List[LiTag]

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if len(v) >= 1:
            return v
        raise ValueError(f'<{cls._tag}> must have at least 1 <li> child')

    def render(self):
        return ''.join([child.render() for child in self.children])

    @classmethod
    def from_node(cls, node: Node) -> UlTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')

        children = [get_tag_cls(child.tag).from_node(child) for child in node.children]
        return cls(children=children)


UlTag.update_forward_refs()


class PTag(Tag):
    _tag = 'p'

    children: List[str]

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if len(v) == 1:
            return v
        raise ValueError(f'<{cls._tag}> must have 1 text child')

    def render(self):
        return f'{self.children[0]}\n'

    @classmethod
    def from_node(cls, node: Node) -> PTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)


PTag.update_forward_refs()


class BrTag(Tag):
    _tag = 'br'

    @validator('children', whole=True)
    def validate_children_len(cls, v):
        if not v:
            return None
        raise ValueError(f'<{cls._tag}> cannot have children')

    def render(self):
        return '\n'

    @classmethod
    def from_node(cls, node: Node) -> BrTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')
        return cls(children=node.children)


BrTag.update_forward_refs()


class SectionTag(Tag):
    _tag = 'section'
    _root = True

    children: List[Union[FooterTag, HeaderTag, UlTag, PTag, InputTag, BrTag, str]]

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
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')

        tag_children: List[Union[Tag, str]] = []

        for node_child in node.children:
            if isinstance(node_child, str):
                tag_children.append(node_child)
            else:
                tag_cls = get_tag_cls(node_child.tag)
                tag_child = tag_cls.from_node(node_child)
                tag_children.append(tag_child)
        return cls(children=tag_children)


SectionTag.update_forward_refs()


class FormTagAttrs(BaseModel):
    data_route: Optional[str]
    data_method: Optional[str]
    data_type: Optional[str]


class FormTag(Tag):
    _tag = 'form'
    _root = True

    attrs: FormTagAttrs
    children: List[SectionTag] = Schema(..., min_length=1)

    def render(self):
        return '\n'.join([child.render() for child in self.children])

    @classmethod
    def from_node(cls, node: Node) -> FormTag:
        if node.tag != cls._tag:
            raise NodeTagMismatchException(
                f'Expected tag <{cls._tag}>, received <{node.tag}>')
        children = [get_tag_cls(child.tag).from_node(child) for child in node.children]
        attrs = FormTagAttrs(**node.attrs)
        return cls(children=children, attrs=attrs)


FormTag.update_forward_refs()

_map_tag_cls = {}

for name, obj in inspect.getmembers(sys.modules[__name__]):
    if inspect.isclass(obj) and issubclass(obj, Tag):
        _map_tag_cls[obj._tag] = obj


def get_tag_cls(tag_name: str) -> Type[Tag]:
    global _map_tag_cls

    try:
        return _map_tag_cls[tag_name]
    except KeyError:
        raise ONEmSDKException(f'Tag <{tag_name}> is not supported')
