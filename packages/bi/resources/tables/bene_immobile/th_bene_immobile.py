#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('anagrafica_id')
        r.fieldcell('catasto')
        r.fieldcell('fg')
        r.fieldcell('num')
        r.fieldcell('sub')
        r.fieldcell('categoria')
        r.fieldcell('ubicazione')
        r.fieldcell('data_siatel')
        r.fieldcell('note')
        r.fieldcell('loc_nome')
        r.fieldcell('loc_indirizzo')
        r.fieldcell('loc_cap')
        r.fieldcell('loc_comune')
        r.fieldcell('loc_pr')
        r.fieldcell('loc_cf')
        r.fieldcell('loc_anno')
        r.fieldcell('loc_uff_terr')
        r.fieldcell('loc_num')
        r.fieldcell('loc_data')
        r.fieldcell('loc_volume')
        r.fieldcell('loc_email')

    def th_order(self):
        return 'anagrafica_id'

    def th_query(self):
        return dict(column='loc_cf', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('anagrafica_id' )
        fb.field('catasto' )
        fb.field('fg' )
        fb.field('num' )
        fb.field('sub' )
        fb.field('categoria' )
        fb.field('ubicazione' )
        fb.field('data_siatel' )
        fb.field('note' )
        fb.field('loc_nome' )
        fb.field('loc_indirizzo' )
        fb.field('loc_cap' )
        fb.field('loc_comune' )
        fb.field('loc_pr' )
        fb.field('loc_cf' )
        fb.field('loc_anno' )
        fb.field('loc_uff_terr' )
        fb.field('loc_num' )
        fb.field('loc_data' )
        fb.field('loc_volume' )
        fb.field('loc_email' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
