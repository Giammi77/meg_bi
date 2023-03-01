#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_id')
        r.fieldcell('code')
        r.fieldcell('regcontr')
        r.fieldcell('ufficio')
        r.fieldcell('serie')
        r.fieldcell('numero')
        r.fieldcell('tipologia')
        r.fieldcell('durata_dal')
        r.fieldcell('durato_al')
        r.fieldcell('data_stipula')
        r.fieldcell('importo_canone')
        r.fieldcell('_id_1')
        r.fieldcell('code_1')
        r.fieldcell('d_a')
        r.fieldcell('identificativo_soggetto')
        r.fieldcell('inizio_rapporto')
        r.fieldcell('fine_rapporto')
        r.fieldcell('_id_2')
        r.fieldcell('code_2')
        r.fieldcell('codice_comune')
        r.fieldcell('t_u')
        r.fieldcell('i_p')
        r.fieldcell('sezione_urbana')
        r.fieldcell('foglio')
        r.fieldcell('particella')
        r.fieldcell('sub')

    def th_order(self):
        return 'caption_locazione'

    def th_query(self):
        return dict(column='caption_locazione', op='contains', val='')

class ViewFromAnagrafica(View):
    pass

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('_id' )
        fb.field('code' )
        fb.field('regcontr' )
        fb.field('ufficio' )
        fb.field('serie' )
        fb.field('numero' )
        fb.field('tipologia' )
        fb.field('durata_dal' )
        fb.field('durato_al' )
        fb.field('data_stipula' )
        fb.field('importo_canone' )
        fb.field('_id_1' )
        fb.field('code_1' )
        fb.field('d_a' )
        fb.field('identificativo_soggetto' )
        fb.field('inizio_rapporto' )
        fb.field('fine_rapporto' )
        fb.field('_id_2' )
        fb.field('code_2' )
        fb.field('codice_comune' )
        fb.field('t_u' )
        fb.field('i_p' )
        fb.field('sezione_urbana' )
        fb.field('foglio' )
        fb.field('particella' )
        fb.field('sub' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
