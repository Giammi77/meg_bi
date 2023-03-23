#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('anagrafica_id')
        r.fieldcell('banca_istituto_id')
        r.fieldcell('banca_filiale_id')
        r.fieldcell('file_id')

    def th_order(self):
        return 'anagrafica_id'

    def th_query(self):
        return dict(column='id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('anagrafica_id' )
        fb.field('banca_istituto_id' )
        fb.field('banca_filiale_id' )
        fb.field('file_id' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
