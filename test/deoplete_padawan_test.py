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

    def test_get_complete_position_for_static_method_call_w_namespace(self):
        position = self.source.get_complete_position(
            {'input': '     \Some\Class::getInst'})
        #             '0....5....0....5..^ <- 18
        self.assertEqual(position, 18)

    def test_get_complete_position_for_fluent_method_calls(self):
        position = self.source.get_complete_position(
            {'input': '$db->select("*")->from("table")->whe'})
        #             '0....5....0....5....0....5....0..^ <- 33
        self.assertEqual(position, 33)

    def test_get_complete_position_for_use_statement(self):
        position = self.source.get_complete_position(
            {'input': '  use Class\\'})
        #             '0....5^ <- 6
        self.assertEqual(position, 6)

    def test_get_complete_position_for_long_use_statement(self):
        position = self.source.get_complete_position(
            {'input': '   use Class\With\Lon'})
        #             '0....5.^ <- 7
        self.assertEqual(position, 7)

    def test_get_complete_position_for_new_statement(self):
        position = self.source.get_complete_position(
            {'input': ' $ala = new Class\\'})
        #             '0....5....0.^ <- 12
        self.assertEqual(position, 12)

    def test_get_complete_position_for_long_new_statement(self):
        position = self.source.get_complete_position(
            {'input': ' $x = new Class\With\Ver'})
        #             '0....5....^ <- 10
        self.assertEqual(position, 10)

    def test_get_complete_position_for_new_with_root_namespace(self):
        position = self.source.get_complete_position(
            {'input': '      new \Date'})
        #             '0....5....0^ <- 11
        self.assertEqual(position, 11)
