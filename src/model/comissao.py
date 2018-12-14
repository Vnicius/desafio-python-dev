#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Comissao:
    def __init__(self):
        self.titulo = ""
        self.url = ""
        self.data_inicio = ""
        self.participacao = ""

    def __repr__(self):
        return """\t\tTitulo: {self.titulo}
                URL: {self.url}
                Inicio: {self.data_inicio}
                Participacao: {self.participacao}\n""".format(self=self)

    def toJSON(self):
        return self.__dict__
