#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Chapa:
    def __init__(self):
        self.nome_parlamentar = ""
        self.nome_completo = ""
        self.chapa = ""

    def __repr__(self):
        return """\t\tNome Parlamentar: {self.nome_parlamentar}
                Nome Completo: {self.nome_completo}
                Chapa: {self.chapa}\n""".format(self=self)

    def toJSON(self):
        return self.__dict__
