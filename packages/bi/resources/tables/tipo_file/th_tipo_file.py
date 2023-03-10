#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice')
        r.fieldcell('descrizione')
        r.fieldcell('note')

    def th_order(self):
        return 'codice'

    def th_query(self):
        return dict(column='codice', op='contains', val='')

   


class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.tipoFileTestata(bc.contentPane(region='top', datapath='.record', height='150px'))

        tab = bc.tabContainer(region='center', margin='2px')
        tab.contentPane(title='Parametri').inlineTableHandler(relation='@parametro_file',datapath='#FORM.parametri', viewResource='ViewFromTipoFile',configurable=True)    

    def tipoFileTestata(self, bc):
        left = bc.roundedGroup(title='Dati file',
                            region='left', width='300px')
        fb = left.formbuilder(cols=1, border_spacing='4px')
        fb.field('codice')
        fb.field('descrizione')
        fb.field('note')
        fb.field('tblinfo_tblid', condition="$pkgid='bi'", 
                        validate_notnull=True, hasDownArrow=True)
        fb.field('str_validazione_row' )

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
