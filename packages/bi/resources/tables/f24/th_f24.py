#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice_fiscale')
        r.fieldcell('abi')
        r.fieldcell('cab')
        r.fieldcell('data_pagamento')
        r.fieldcell('codice_tributo')
        r.fieldcell('anno_tributo')

    def th_order(self):
        return 'codice_fiscale'

    def th_query(self):
        return dict(column='codice_fiscale', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('codice_fiscale' )
        fb.field('abi' )
        fb.field('cab' )
        fb.field('data_pagamento' )
        fb.field('codice_tributo' )
        fb.field('anno_tributo' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
