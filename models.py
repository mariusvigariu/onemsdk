from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Union, Type, Optional

from pydantic import BaseModel, Schema

from exceptions import NodeTagMismatchException, ONEmSDKException


class Node(BaseModel):
    tag: str
    attrs: Dict[str, str] = {}
    children: List[Union['Node', str]] = []

    def add_child(self, child: Union['Node', str]):
        self.children.append(child)


Node.update_forward_refs()


def get_tag_cls(tag_name: str) -> Type[Tag]:
    supported_tags = {
        'section': SectionTag,
        'header': HeaderTag,
        'footer': FooterTag,
        'form': FormTag,
        'input': InputTag,
        'ul': UlTag,
        'li': LiTag,
        'a': ATag,
        'p': PTag,
        'br': BrTag
    }
    try:
        return supported_tags[tag_name]
    except KeyError:
        raise ONEmSDKException(f'Tag <{tag_name}> is not supported')


class Tag(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_node(cls: Type[Tag], node: Node) -> Tag:
        pass


class HeaderTag(BaseModel, Tag):
    children: List[str] = Schema(..., min_length=1, max_length=1)

    def render(self):
        return self.children[0] + '\n'

    @classmethod
    def from_node(cls, node: Node) -> HeaderTag:
        this_tag = 'header'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)


class FooterTag(BaseModel, Tag):
    children: List[str] = Schema(..., min_length=1, max_length=1)

    def render(self):
        return self.children[0]

    @classmethod
    def from_node(cls, node: Node) -> FooterTag:
        this_tag = 'footer'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        children = node.children.copy()

        return cls(children=children)


class FormTagAttrs(BaseModel):
    data_route: Optional[str]
    data_method: Optional[str]
    data_type: Optional[str]


class InputTagAttrs(BaseModel):
    name: str
    type: str


class InputTag(BaseModel, Tag):
    attrs: InputTagAttrs

    def render(self):
        return ''

    @classmethod
    def from_node(cls, node: Node) -> InputTag:
        this_tag = 'input'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        attrs = InputTagAttrs(**node.attrs)
        return cls(attrs=attrs)


class ATagAttrs(BaseModel):
    href: str


class ATag(BaseModel, Tag):
    attrs = ATagAttrs
    children: List[str] = Schema(..., min_length=1)

    def render(self):
        return self.children[0]

    @classmethod
    def from_node(cls, node: Node) -> ATag:
        this_tag = 'a'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        attrs = ATagAttrs(**node.attrs)
        children = node.children.copy()
        return cls(attrs=attrs, children=children)


class LiTag(BaseModel, Tag):
    children: List[Union[ATag, str]] = Schema(..., min_length=1)

    def render(self):
        if isinstance(self.children[0], ATag):
            return self.children[0].render() + '\n'
        return self.children[0] + '\n'

    @classmethod
    def from_node(cls, node: Node) -> LiTag:
        this_tag = 'li'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        children = []
        for child in node.children:
            if isinstance(child, str):
                children.append(child)
            else:
                children.append(get_tag_cls(child.tag).from_node(child))

        return cls(children=children)


class UlTag(BaseModel, Tag):
    children: List[LiTag] = Schema(..., min_length=1)

    def render(self):
        return ''.join([child.render() for child in self.children])

    @classmethod
    def from_node(cls, node: Node) -> UlTag:
        this_tag = 'ul'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        children = [get_tag_cls(child.tag).from_node(child) for child in node.children]
        return cls(children=children)


class PTag(BaseModel, Tag):
    children: List[str] = Schema(..., min_length=1)

    def render(self):
        return f'{self.children[0]}\n'

    @classmethod
    def from_node(cls, node: Node) -> PTag:
        this_tag = 'p'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        children = node.children.copy()
        return cls(children=children)


class BrTag(BaseModel, Tag):

    def render(self):
        return '\n'

    @classmethod
    def from_node(cls, node: Node) -> BrTag:
        this_tag = 'br'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        return cls()


class SectionTag(BaseModel, Tag):
    children: List[Union[HeaderTag, FooterTag, UlTag, PTag, InputTag, BrTag, str]]

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
        this_tag = 'section'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        children = []
        for child in node.children:
            if isinstance(child, str):
                children.append(child)
            else:
                children.append(get_tag_cls(child.tag).from_node(child))
        return cls(children=children)


SectionTag.update_forward_refs()


class FormTag(BaseModel, Tag):
    attrs: FormTagAttrs
    children: List[SectionTag] = Schema(..., min_length=1)

    def render(self):
        return '\n'.join([child.render() for child in self.children])

    @classmethod
    def from_node(cls, node: Node) -> FormTag:
        this_tag = 'form'
        if node.tag != this_tag:
            raise NodeTagMismatchException(
                f'Expected tag <{this_tag}>, received <{node.tag}>')
        children = [get_tag_cls(child.tag).from_node(child) for child in node.children]
        attrs = FormTagAttrs(**node.attrs)
        return cls(children=children, attrs=attrs)
