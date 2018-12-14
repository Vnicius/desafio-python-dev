#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Materia:
    def __init__(self):
        self.titulo = ""
        self.url = ""
        self.ementa = ""
        self.autor = ""
        self.data = ""

    def __repr__(self):
        return """\t\tTitulo: {self.titulo}
                URL: {self.url}
                Ementa: {self.ementa}
                Autor: {self.autor}
                Data: {self.data}""".format(self=self)

    def toJSON(self):
        return self.__dict__
