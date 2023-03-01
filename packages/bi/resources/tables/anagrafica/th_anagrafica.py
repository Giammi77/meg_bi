#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):
    css_requires = 'rcweb'
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cognome')
        r.fieldcell('email')
        r.fieldcell('pec')
        r.fieldcell('societa')
        r.fieldcell('codice_fiscale')
        r.fieldcell('indirizzo')
        r.fieldcell('cap')
        r.fieldcell('comune_di_residenza')
        r.fieldcell('prov')
        r.fieldcell('cod_utente')
        r.fieldcell('n_ord')
        r.fieldcell('datanascita')
        r.fieldcell('luogonascita')
        r.fieldcell('provnascita')
        r.fieldcell('invita')
        r.fieldcell('datadecesso')
        r.fieldcell('note')
        r.fieldcell('nazione')
        r.fieldcell('ultimoaggiornamento')
        r.fieldcell('trasferito_ts')

    def th_order(self):
        return 'cognome'

    def th_query(self):
        return dict(column='cognome', op='contains', val='')

class ViewBase(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('conta_f24',hidden=True)
        r.fieldcell('conta_bonifico',hidden=True)
        r.fieldcell('conta_locazione',hidden=True)
        r.fieldcell('nominativo')
        r.fieldcell('codice_fiscale')
        r.fieldcell('comune_di_residenza')
        r.fieldcell('indirizzo')
        r.fieldcell('prov')
        r.fieldcell('nazione')
        r.fieldcell('societa')
        r.cell('semaforo_f24', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_f24;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='4em', name='F24')
        r.cell('semaforo_locazione', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_locazione;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='4em', name='Loc')

        r.cell('semaforo_bonifico', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_bonifico;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='4em', name='BB')


class Form(BaseComponent):

    def th_form(self, form):
        bc=form.center.borderContainer(datapth='.record')
        fb = bc.contentPane(region='top').formbuilder(cols=4, border_spacing='4px')
        fb.field('cognome')
        fb.field('nome')
        fb.field('datanascita')
        fb.field('luogonascita')
        fb.field('provnascita')
        fb.field('comune_di_residenza')
        fb.field('indirizzo')
        fb.field('nazione')
        fb.field('prov')
        fb.field('cap')
        fb.field('societa')
        fb.field('codice_fiscale')
        fb.field('email')
        fb.field('pec')
        fb.field('cod_utente')
        fb.field('n_ord')
        fb.field('invita')
        fb.field('datadecesso')
        fb.field('note')
        fb.field('ultimoaggiornamento')
        fb.field('trasferito_ts')


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
