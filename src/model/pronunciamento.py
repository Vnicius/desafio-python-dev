#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Pronunciamento:
    def __init__(self):
        self.data = ""
        self.tipo = ""
        self.casa = ""
        self.partido = ""
        self.uf = ""
        self.resumo = ""

    def __repr__(self):
        return """\n\t\tData: {self.data}
                Tipo: {self.tipo}
                Casa: {self.casa}
                Partido: {self.partido}
                UF: {self.uf}
                Resumo: {self.resumo}""".format(self=self)

    def toJSON(self):
        return self.__dict__
