import unittest
from unittest.mock import Mock
import sys

sys.path.insert(0, './rplugin/python3/deoplete')
sys.modules['sources.base'] = __import__('mock_base')

from sources import deoplete_padawan  # noqa


class SourceTest(unittest.TestCase):

    def setUp(self):
        self.source = deoplete_padawan.Source(Mock())

    def test_get_complete_position_for_method_call(self):
        position = self.source.get_complete_position(
            {'input': '  $this->getSome'})
        #             '0....5...^ <- 9
        self.assertEqual(position, 9)

    def test_get_complete_position_for_variable(self):
        position = self.source.get_complete_position(
            {'input': '  $var'})
        #             '0..^ <- 3
        self.assertEqual(position, 3)

    def test_get_complete_position_for_method_param(self):
        position = self.source.get_complete_position(
            {'input': 'callWithParams("Hell'})
        #             '0....5....0....^ <- 15
        self.assertEqual(position, 15)

    def test_get_complete_position_for_method_variable_param(self):
        position = self.source.get_complete_position(
            {'input': '          set($var'})
        #             '0....5....0....^ <- 15
        self.assertEqual(position, 15)

    def test_get_complete_position_for_method_static_call_param(self):
        position = self.source.get_complete_position(
            {'input': '   call(self::getVa'})
        #             '0....5....0...^ <- 14
        self.assertEqual(position, 14)

    def test_get_complete_position_for_static_method_call(self):
        position = self.source.get_complete_position(
            {'input': '     Class::getInst'})
        #             '0....5....0.^ <- 12
        self.assertEqual(position, 12)

    def test_get_complete_position_for_fluent_method_calls(self):
        position = self.source.get_complete_position(
            {'input': '$db->select("*")->from("table")->whe'})
        #             '0....5....0....5....0....5....0..^ <- 33
        self.assertEqual(position, 33)
