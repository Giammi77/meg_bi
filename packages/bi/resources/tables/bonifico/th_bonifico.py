#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tipo_record')
        r.fieldcell('tipo_fornitura')
        r.fieldcell('anno')
        r.fieldcell('ccodcat')
        r.fieldcell('codice_fiscale')
        r.fieldcell('abi')
        r.fieldcell('cab')
        r.fieldcell('data')

    def th_order(self):
        return 'abi'

    def th_query(self):
        return dict(column='abi', op='contains', val='')

class ViewFromAnagrafica(View):
    pass

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('tipo_record' )
        fb.field('tipo_fornitura' )
        fb.field('anno' )
        fb.field('ccodcat' )
        fb.field('codice_fiscale' )
        fb.field('abi' )
        fb.field('cab' )
        fb.field('data' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
