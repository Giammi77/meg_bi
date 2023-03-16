#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('caption_pagopa')
        r.fieldcell('anagrafica_id')
        r.fieldcell('idpa')
        r.fieldcell('codice_fiscale')
        r.fieldcell('id_station')
        r.fieldcell('importo')
        r.fieldcell('descrizione')
        r.fieldcell('nominativo')
        r.fieldcell('indirizzo')
        r.fieldcell('cap')
        r.fieldcell('citta')
        r.fieldcell('provincia')
        r.fieldcell('iban')
        r.fieldcell('id_psp')
        r.fieldcell('data')
        r.fieldcell('ente_creditore')

    def th_order(self):
        return 'caption_pagopa'

    def th_query(self):
        return dict(column='caption_pagopa', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('anagrafica_id' )
        fb.field('idpa' )
        fb.field('codice_fiscale' )
        fb.field('id_station' )
        fb.field('importo' )
        fb.field('descrizione' )
        fb.field('nominativo' )
        fb.field('indirizzo' )
        fb.field('cap' )
        fb.field('citta' )
        fb.field('provincia' )
        fb.field('iban' )
        fb.field('id_psp' )
        fb.field('data' )
        fb.field('ente_creditore' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
