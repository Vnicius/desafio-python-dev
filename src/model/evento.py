#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Evento:
    def __init__(self):
        self.titulo = ""
        self.periodo = ""
        self.documento = ""

    def toJSON(self):
        return self.__dict__
