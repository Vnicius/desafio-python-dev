#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Missao:
    def __init__(self):
        self.evento = ""
        self.periodo = ""
        self.documento = ""

    def __repr__(self):
        return """\t\tEvento: {self.evento}
            Periodo: {self.periodo}
            Documento: {self.documento}\n""".format(self=self)

    def toJSON(self):
        return self.__dict__
