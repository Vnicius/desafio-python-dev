#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Mandato:
    def __init__(self):
        self.cargo = ""
        self.inicio = ""
        self.fim = ""

    def __repr__(self):
        return """\t\tCargo: {self.cargo}
                Data Inicio: {self.inicio}
                Data Fim: {self.fim}""".format(self=self)

    def toJSON(self):
        return self.__dict__
