from unittest import TestCase

from onemsdk.exceptions import ONEmSDKException
from onemsdk.parser import (PTag, HeaderTag, ATag, LiTag, UlTag, BrTag, get_tag_cls,
                            FormTag, InputTag, InputTagAttrs, SectionTag, FooterTag,
                            SectionTagAttrs, ATagAttrs, LiTagAttrs)


class TestTags(TestCase):

    def test_header_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = HeaderTag(children=['First child', 'second child'])
        self.assertIn('<header> must have max 1 text child', str(context.exception))

        header = HeaderTag(children=['One child'])

        self.assertEqual('One child', header.children[0])

    def test_li_tag(self):
        a_tag = ATag(attrs=ATagAttrs(href=""), children=['one child'])

        with self.assertRaises(ONEmSDKException) as context:
            _ = LiTag(children=[a_tag, 'oops'])

        self.assertIn('<li> must have 1 (text or <a>) child', str(context.exception))

        header_tag = HeaderTag(children=['One child'])
        with self.assertRaises(ONEmSDKException) as context:
            _ = LiTag(children=[header_tag])

        self.assertIn('<li> must have 1 (text or <a>) child', str(context.exception))

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

        self.assertIn('<ul> must have min 1 <li> child', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = UlTag(children=[])

        self.assertIn('<ul> must have min 1 <li> child',
                      str(context.exception))

        ul_tag = UlTag(children=[
            LiTag(children=['First list item'], attrs=LiTagAttrs()),
            LiTag(children=['Second list item'], attrs=LiTagAttrs())
        ])

        self.assertEqual('First list item', ul_tag.children[0].children[0])

    def test_p_tag(self):
        with self.assertRaises(ONEmSDKException) as context:
            _ = PTag(children=['first child', 'second child'])

        self.assertIn('<p> must have max 1 text child', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = PTag(children=[HeaderTag(children=['bad child'])])

        self.assertIn('<p> must have max 1 text child', str(context.exception))

        p_tag = PTag(children=['one child'])

        self.assertEqual('one child', p_tag.children[0])

    def test_br_tag(self):
        br_tag = BrTag()
        self.assertListEqual([], br_tag.children)

    def test_input_tag(self):
        input_tag = InputTag(attrs=InputTagAttrs(type='text'))
        self.assertEqual('text', input_tag.attrs.type)

    def test_section_tag(self):
        # with self.assertRaises(ONEmSDKException) as context:
        #     _ = SectionTag(attrs=SectionTagAttrs(), children=[])
        #
        # self.assertIn(
        #     '<section> must have at least 1 child different than <header> or <footer>',
        #     str(context.exception)
        # )
        #
        # with self.assertRaises(ONEmSDKException) as context:
        #     _ = SectionTag(attrs=SectionTagAttrs(), children=[
        #         HeaderTag(children=['Header'])
        #     ])
        #
        # self.assertIn(
        #     '<section> must have at least 1 child different than <header> or <footer>',
        #     str(context.exception)
        # )
        #
        # with self.assertRaises(ONEmSDKException) as context:
        #     _ = SectionTag(attrs=SectionTagAttrs(), children=[
        #         HeaderTag(children=['Header']),
        #         FooterTag(children=['Footer'])
        #     ])
        #
        # self.assertIn(
        #     '<section> must have at least 1 child different than <header> or <footer>',
        #     str(context.exception)
        # )

        # with self.assertRaises(ONEmSDKException) as context:
        #     _ = SectionTag(attrs=SectionTagAttrs(), children=[
        #         PTag(children=['Body']),
        #         HeaderTag(children=['Header'])
        #     ])
        #
        # self.assertIn('<header> must be first in a <section>', str(context.exception))
        #
        # with self.assertRaises(ONEmSDKException) as context:
        #     _ = SectionTag(attrs=SectionTagAttrs(), children=[
        #         FooterTag(children=['Footer']),
        #         PTag(children=['Body']),
        #     ])
        #
        # self.assertIn('<footer> must be last in a <section>', str(context.exception))
        #
        # with self.assertRaises(ONEmSDKException) as context:
        #     _ = SectionTag(attrs=SectionTagAttrs(), children=[
        #         PTag(children=['Body']),
        #         FooterTag(children=['Footer']),
        #         FooterTag(children=['Footer']),
        #     ])
        #
        # self.assertIn('1 <footer> per <section> permitted', str(context.exception))
        #
        # with self.assertRaises(ONEmSDKException) as context:
        #     _ = SectionTag(attrs=SectionTagAttrs(), children=[
        #         HeaderTag(children=['Header']),
        #         HeaderTag(children=['Header']),
        #         PTag(children=['Body']),
        #     ])
        #
        # self.assertIn('1 <header> per <section> permitted', str(context.exception))

        with self.assertRaises(ONEmSDKException) as context:
            _ = SectionTag(attrs=SectionTagAttrs(), children=[
                SectionTag(attrs=SectionTagAttrs(),
                           children=[PTag(children=['Text'])])
            ])

        self.assertIn('<section> cannot be child for <section>', str(context.exception))

    def test_get_tag_cls(self):
        tag_cls = get_tag_cls('form')

        self.assertEqual(tag_cls, FormTag)
