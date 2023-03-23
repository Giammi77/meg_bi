#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('anagrafica_id')
        r.fieldcell('marca')
        r.fieldcell('modello')
        r.fieldcell('targa')
        r.fieldcell('data_immatricolazione')
        r.fieldcell('altro_fermo_attore')
        r.fieldcell('altro_fermo_importo')

    def th_order(self):
        return 'anagrafica_id'

    def th_query(self):
        return dict(column='targa', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('anagrafica_id' )
        fb.field('marca' )
        fb.field('modello' )
        fb.field('targa' )
        fb.field('data_immatricolazione' )
        fb.field('altro_fermo_attore' )
        fb.field('altro_fermo_importo' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
