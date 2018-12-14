#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
from senatorsScrapper import SenatorsScrapper

QUANT_SENADORES = 81

class SenatorsScrapperTest(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(SenatorsScrapperTest, self).__init__(*args, **kwargs)
    self.scrapper = SenatorsScrapper()
    self.data = []

  def test_data(self):
    """
    Verificar se está pegando todos os senadores
    """
    self.data = self.scrapper.get_data()
    self.assertEqual(QUANT_SENADORES, len(self.data))
  
  def test_save_file(self):
    """
    Verificar se está salvando o arquivo
    """
    self.scrapper.get_data()
    self.scrapper.export_to_JSON("test")
    self.assertTrue(self.__check_file("test.json"))
  
  def __check_file(self, file_name):
    try:
      f = open(file_name, "r", encoding="utf-8")
      return f.readline() != ""

    except FileNotFoundError:
      return False

if __name__ == "__main__":
  unittest.main() 