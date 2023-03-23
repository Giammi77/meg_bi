#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('filiale')
        r.fieldcell('banca_istituto_id')
        r.fieldcell('cab')
        r.fieldcell('indirizzo')
        r.fieldcell('sportello')
        r.fieldcell('citta')
        r.fieldcell('prov')
        r.fieldcell('cap')

    def th_order(self):
        return 'banca_istituto_id'

    def th_query(self):
        return dict(column='banca_istituto_id', op='contains', val='')
    

class ViewFromBancaIstituto(View):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cab',edit=True)
        r.fieldcell('indirizzo',edit=True)
        r.fieldcell('sportello',edit=True)
        r.fieldcell('citta',edit=True)
        r.fieldcell('prov',edit=True)
        r.fieldcell('cap',edit=True)



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('banca_istituto_id')
        fb.field('cab')
        fb.field('indirizzo')
        fb.field('sportello')
        fb.field('citta')
        fb.field('prov')
        fb.field('cap')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
