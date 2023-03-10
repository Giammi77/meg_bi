#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):
    css_requires = 'rcweb'
    def th_struct(self,struct):
        r = struct.view().rows()

        r.fieldcell('codice_fiscale',width='30em')


    def th_order(self):
        return 'codice_fiscale'

    def th_query(self):
        return dict(column='codice_fiscale', op='contains', val='')

class ViewBase(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice_fiscale')


class Form(BaseComponent):

    def th_form(self, form):
        bc=form.center.borderContainer(datapth='.record')
        fb = bc.contentPane(region='top').formbuilder(cols=4, border_spacing='4px')
        fb.field('codice_fiscale')

        tc = bc.tabContainer(region='center' ) 
        # tc.data('#FORM.anagrafica.pagina','')
        # tc.dataController("""
        #                 SET #FORM.pagina = 'f24'
        #                 SET #FORM.anagrafica.pagina = ''
        #                 """,
        #                 tags="^#FORM.controller.loaded")
        tc.contentPane(title='Bonifici').plainTableHandler(relation='@bonifico',
                                    datapath='#FORM.bonifico',
                                    viewResource='ViewFromAnagrafica',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    condition_onStart=True)

        tc.contentPane(title='Locazioni' ).plainTableHandler(relation='@locazione',
                                    datapath='#FORM.locazione',
                                    viewResource='ViewFromAnagrafica',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    condition_onStart=True)
        
        tc.contentPane(title='F24' ).plainTableHandler(relation='@f24',
                                    datapath='#FORM.f24',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    condition_onStart=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
