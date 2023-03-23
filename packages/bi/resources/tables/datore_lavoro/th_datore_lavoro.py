#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('anagrafica_id')
        r.fieldcell('data_siatel')
        r.fieldcell('datore')
        r.fieldcell('ind')
        r.fieldcell('cap')
        r.fieldcell('comune')
        r.fieldcell('pr')
        r.fieldcell('p_iva')
        r.fieldcell('email')
        r.fieldcell('pec')

    def th_order(self):
        return 'anagrafica_id'

    def th_query(self):
        return dict(column='datore', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('anagrafica_id' )
        fb.field('data_siatel' )
        fb.field('datore' )
        fb.field('ind' )
        fb.field('cap' )
        fb.field('comune' )
        fb.field('pr' )
        fb.field('p_iva' )
        fb.field('email' )
        fb.field('pec' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
