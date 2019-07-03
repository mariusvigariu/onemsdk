from unittest import TestCase

from pydantic import ValidationError

from model.tag import PTag, HeaderTag, ATag, LiTag, UlTag, BrTag, get_tag_cls, FormTag, \
    InputTag, InputTagAttrs


class TestModels(TestCase):

    def test_header_tag(self):
        with self.assertRaises(ValidationError) as context:
            _ = HeaderTag(children=[])
            self.assertTrue('Header tag must have 1 text child' in context.exception)

        with self.assertRaises(ValidationError) as context:
            _ = HeaderTag(children=['First child', 'second child'])
            self.assertTrue('Header tag must have 1 text child' in context.exception)

        header = HeaderTag(children=['One child'])

        self.assertEqual('One child', header.children[0])

    def test_li_tag(self):
        a_tag = ATag(children=['one child'])

        with self.assertRaises(ValidationError) as context:
            _ = LiTag(children=[a_tag, 'oops'])

        self.assertTrue('<li> must have 1 child' in str(context.exception))

        header_tag = HeaderTag(children=['One child'], oops='3')
        with self.assertRaises(ValidationError) as context:
            _ = LiTag(children=[header_tag])

        self.assertTrue('<header> cannot be a child for <li>' in str(context.exception))

        li_tag = LiTag(children=[a_tag])
        self.assertEqual(a_tag, li_tag.children[0])
        self.assertEqual('one child', li_tag.children[0].children[0])

    def test_ul_tag(self):
        with self.assertRaises(ValidationError) as context:
            _ = UlTag(children=[
                HeaderTag(children=['bad child'])
            ])

        self.assertTrue('<header> cannot be a child for <ul>' in str(context.exception))

        with self.assertRaises(ValidationError) as context:
            _ = UlTag(children=[])

        self.assertTrue('<ul> must have at least 1 <li> child', str(context.exception))

        ul_tag = UlTag(children=[
            LiTag(children=['First list item']),
            LiTag(children=['Second list item'])
        ])

        self.assertEqual('First list item', ul_tag.children[0].children[0])

    def test_p_tag(self):
        with self.assertRaises(ValidationError) as context:
            _ = PTag(children=['first child', 'second child'])

        self.assertTrue('<p> must have 1 text child')

        with self.assertRaises(ValidationError) as context:
            _ = PTag(children=[HeaderTag(children=['bad child'])])

        self.assertTrue('<header> cannot be a child for <p>')

        p_tag = PTag(children=['one child'])

        self.assertEqual('one child', p_tag.children[0])

    def test_br_tag(self):
        with self.assertRaises(ValidationError) as context:
            _ = BrTag(children=['child'])

        self.assertTrue('<br> cannot have children' in str(context.exception))

        br_tag = BrTag(children=[])
        self.assertIsNone(br_tag.children)

        br_tag = BrTag()
        self.assertIsNone(br_tag.children)

    def test_input_tag(self):
        with self.assertRaises(ValidationError) as context:
            _ = InputTag(children=['child'])

        self.assertTrue('<input> cannot have children' in str(context.exception))

        input_tag = InputTag(children=[], attrs=InputTagAttrs(name='', type=''))
        self.assertIsNone(input_tag.children)

        input_tag = InputTag(attrs=InputTagAttrs(name='', type=''))
        self.assertIsNone(input_tag.children)

    def test_get_tag_cls(self):
        tag_cls = get_tag_cls('form')

        self.assertEqual(tag_cls, FormTag)
