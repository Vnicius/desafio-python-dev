#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Profissao:
    def __init__(self):
        self.nome = ""

    def __repr__(self):
        return """Nome: {self.nome}\n""".format(self=self)

    def toJSON(self):
        return self.__dict__
