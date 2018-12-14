#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Resumo:
    def __init__(self):
        self.titulo = ""
        self.url = ""
        self.quantidade = ""

    def __repr__(self):
        return """\t\tTitulo: {self.titulo}
                URL: {self.url}
                Quantidade: {self.quantidade}""".format(self=self)

    def toJSON(self):
        return self.__dict__
