from unittest import TestCase

from onemsdk.exceptions import ONEmSDKException
from onemsdk.parser import (PTag, HeaderTag, ATag, LiTag, UlTag, BrTag, get_tag_cls,
                            FormTag, InputTag, InputTagAttrs, SectionTag, FooterTag,
                            SectionTagAttrs, ATagAttrs, LiTagAttrs)


class TestModels(TestCase):

    def test_header_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = HeaderTag(children=[])
        self.assertIn('<header> must have 1 children', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = HeaderTag(children=['First child', 'second child'])
        self.assertIn('<header> must have 1 children', str(context.exception))

        header = HeaderTag(children=['One child'])

        self.assertEqual('One child', header.children[0])

    def test_li_tag(self):
        a_tag = ATag(attrs=ATagAttrs(href=""), children=['one child'])

        with self.assertRaises(ONEmSDKException) as context:
            _ = LiTag(children=[a_tag, 'oops'])

        self.assertIn('<li> must have 1 children', str(context.exception))

        header_tag = HeaderTag(children=['One child'], oops='3')
        with self.assertRaises(ONEmSDKException) as context:
            _ = LiTag(children=[header_tag])

        self.assertIn('<header> cannot be child for <li>', str(context.exception))

        li_tag = LiTag(children=[a_tag], attrs=LiTagAttrs())
        self.assertEqual(a_tag, li_tag.children[0])
        self.assertEqual('one child', li_tag.children[0].children[0])

        li_tag = LiTag(children=[a_tag])
        self.assertEqual(a_tag, li_tag.children[0])
        self.assertEqual('one child', li_tag.children[0].children[0])

    def test_ul_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = UlTag(children=[
                HeaderTag(children=['bad child'])
            ])

        self.assertIn('<header> cannot be child for <ul>', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = UlTag(children=[])

        self.assertIn('<ul> must have between 1 and 1000 children',
                      str(context.exception))

        ul_tag = UlTag(children=[
            LiTag(children=['First list item'], attrs=LiTagAttrs()),
            LiTag(children=['Second list item'], attrs=LiTagAttrs())
        ])

        self.assertEqual('First list item', ul_tag.children[0].children[0])

    def test_p_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = PTag(children=['first child', 'second child'])

        self.assertIn('<p> must have 1 children', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = PTag(children=[HeaderTag(children=['bad child'])])

        self.assertIn('<header> cannot be child for <p>', str(context.exception))

        p_tag = PTag(children=['one child'])

        self.assertEqual('one child', p_tag.children[0])

    def test_br_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = BrTag(children=['child'])

        self.assertIn('<br> must have 0 children', str(context.exception))

        br_tag = BrTag(children=[])
        self.assertListEqual([], br_tag.children)

        br_tag = BrTag()
        self.assertListEqual([], br_tag.children)

    def test_input_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = InputTag(children=['child'])

        self.assertIn('<input> must have 0 children', str(context.exception))

        input_tag = InputTag(children=[], attrs=InputTagAttrs(name='', type=''))
        self.assertListEqual([], input_tag.children)

        input_tag = InputTag(attrs=InputTagAttrs(name='', type=''))
        self.assertListEqual([], input_tag.children)

    def test_section_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[])

        self.assertIn('<section> must have between 1 and 1000 children',
                      str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                HeaderTag(children=['Header'])
            ])

        self.assertIn('<section> must contain a body', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                HeaderTag(children=['Header']),
                FooterTag(children=['Footer'])
            ])

        self.assertIn('<section> must contain a body', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                PTag(children=['Body']),
                HeaderTag(children=['Header'])
            ])

        self.assertIn('<header> must be first in a <section>', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                FooterTag(children=['Footer']),
                PTag(children=['Body']),
            ])

        self.assertIn('<footer> must be last in a <section>', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                PTag(children=['Body']),
                FooterTag(children=['Footer']),
                FooterTag(children=['Footer']),
            ])

        self.assertIn('1 <footer> per <section> permitted', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                HeaderTag(children=['Header']),
                HeaderTag(children=['Header']),
                PTag(children=['Body']),
            ])

        self.assertIn('1 <header> per <section> permitted', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                SectionTag(attrs=SectionTagAttrs(),
                           children=[PTag(children=['Text'])])
            ])

        self.assertIn('<section> cannot be child for <section>', str(context.exception))

    def test_get_tag_cls(self):
        tag_cls = get_tag_cls('form')

        self.assertEqual(tag_cls, FormTag)
