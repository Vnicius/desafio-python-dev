#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Academico:
    def __init__(self):
        self.curso = ""
        self.grau = ""
        self.estabelecimento = ""
        self.local = ""

    def __repr__(self):
        return """\t\tCurso: {self.curso}
                Grau: {self.grau}
                Estabelecimento: {self.estabelecimento}
                Local: {self.local}""".format(self=self)

    def toJSON(self):
        return self.__dict__
