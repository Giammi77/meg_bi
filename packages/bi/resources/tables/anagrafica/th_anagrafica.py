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

    def th_hiddencolumns(self):
        return """$conta_f24,$conta_bonifico,$conta_locazione,$conta_pagopa,$conta_conto_corrente,$conta_bene_mobile,$conta_bene_immobile,$conta_datore_lavoro"""
        
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice_fiscale',width='30em')
        origine_dati = r.columnset('origine_dati', name='Origine Dati',
                                    background='rgba(40, 148, 0, 0.9)')
        origine_dati.cell('semaforo_f24', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_f24;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='F24')
        origine_dati.cell('semaforo_locazione', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_locazione;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='Locazioni')

        origine_dati.cell('semaforo_bonifico', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_bonifico;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='Bonifici')

        origine_dati.cell('semaforo_pagopa', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_pagopa;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='PagoPa')

        beni_aggredibili = r.columnset('beni_aggredibili', name='Beni Aggredibili',
                                    background='rgba(255, 26, 26)')
        beni_aggredibili.cell('semaforo_conto_corrente', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_conto_corrente;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='C.Correnti')

        beni_aggredibili.cell('semaforo_bene_mobile', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_bene_mobile;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='B.Mobili')

        beni_aggredibili.cell('semaforo_bene_immobile', _customGetter="""function(row){
            var _class = '';
            var num = row.conta_bene_immobile;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='B.Immobili')

        beni_aggredibili.cell('semaforo_datore_lavoro', _customGetter="""function(row){
            var _class = '';
            var num = row.datore_lavoro;
             if (num > 0){
                _class = 'semaforo_verde';
             }
             return '<div class="'+_class+'">&nbsp;</div>';
        }
        """, width='6em', name='D.Lavoro')



    def th_top_custom(self,top):
        top.slotToolbar('sections@origine_dati,*,sections@beni', childname='lower', _position='>bar')

    def th_sections_origine_dati(self):
        return [
            dict(caption='Tutti'), 
            dict(caption='F24', condition="$conta_f24 >0", virtual_columns='$conta_f24'),
            dict(caption='Bonifici', condition="$conta_bonifico >0", virtual_columns='$conta_bonifico'),
            dict(caption='PagoPa', condition="$conta_pagopa >0", virtual_columns='$conta_pagopa'),
            dict(caption='Locazioni', condition="$conta_locazione >0", virtual_columns='$conta_locazione'),
            ]
    def th_sections_beni(self):
        return [
            dict(caption='Tutti'), 
            dict(caption='Conti Corrente', condition="$conta_conto_corrente >0", virtual_columns='$conta_conto_corrente'),
            dict(caption='Beni Mobili', condition="$conta_bene_mobile >0", virtual_columns='$conta_bene_mobile'),
            dict(caption='Beni Immobili', condition="$conta_bene_immobile >0", virtual_columns='$conta_bene_immobile'),
            dict(caption='Datori Lavoro', condition="$conta_datore_lavoro >0", virtual_columns='$conta_datore_lavoro'),
            dict(caption='Tutti Beni', condition='$bene_aggredibile is true', virtual_columns='$bene_aggredibile'),
            ]

    def th_bottom_custom(self,bottom):
        bar = bottom.slotToolbar('*,trasferisci_b_aggr,3,esporta_beni,*')  # '20,trasferisci,*,importatore,*'
        bar.trasferisci_b_aggr.slotButton('Carica Beni',action="genro.mainGenroWindow.genro.publish('open_batch');").dataRpc(self.carica_beni)
        bar.esporta_beni.slotButton('Esporta',
                                    action="""genro.mainGenroWindow.genro.publish('open_batch');
                                            FIRE .th_batch_run = {resource:'btc_esporta_beni',res_type:'action'};
                                            """)

    @public_method
    def carica_beni(self,*args,**kwargs):
        caricati=0
        btc = self.db.currentPage.btc if self.db.currentPage else None  # oggetto "batch" (tab dove viene mostrato la progress bar)
        btc.batch_create(title=f"Carica Beni")
        tabelle=['bi.f24','bi.bonifico','bi.pagopa','bi.locazione'] 
        
        for tbl in tabelle:
            caricati+=self.db.table(tbl).carica_beni(btc=btc)
        self.btc.batch_complete(f'Caricamento Completato <br>Beni Caricati = {caricati}',
                                result_attr=dict())                
        self.db.commit()

class Form(BaseComponent):

    def th_form(self, form):
        bc=form.center.borderContainer(datapth='.record')
        fb = bc.contentPane(region='top',datapath='.record').formbuilder(cols=4, border_spacing='4px')
        fb.field('codice_fiscale')

        tc = bc.tabContainer(region='center' ) 
        # tc.data('#FORM.anagrafica.pagina','')
        # tc.dataController("""
        #                 SET #FORM.pagina = 'f24'
        #                 SET #FORM.anagrafica.pagina = ''
        #                 """,
        #                 tags="^#FORM.controller.loaded")
        tc.contentPane(title='Bonifici').dialogTableHandler(relation='@bonifico',
                                    datapath='#FORM.bonifico',
                                    viewResource='ViewFromAnagrafica',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

        tc.contentPane(title='Locazioni' ).dialogTableHandler(relation='@locazione',
                                    datapath='#FORM.locazione',
                                    viewResource='ViewFromAnagrafica',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)
        
        tc.contentPane(title='F24' ).dialogTableHandler(relation='@f24',
                                    datapath='#FORM.f24',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

        tc.contentPane(title='PagoPa' ).dialogTableHandler(relation='@pagopa',
                                    datapath='#FORM.pagopa',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)
                                    
        tc.contentPane(title='Conti Correnti Associati' ).dialogTableHandler(relation='@conto_corrente',
                                    datapath='#FORM.conto_corrente',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

        tc.contentPane(title='Beni Mobili Associati' ).dialogTableHandler(relation='@bene_mobile',
                                    datapath='#FORM.bene_mobile',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

        tc.contentPane(title='Beni Immobili Associati' ).dialogTableHandler(relation='@bene_immobile',
                                    datapath='#FORM.bene_immobile',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

        tc.contentPane(title='Datori Lavoro Associati' ).dialogTableHandler(relation='@datore_lavoro',
                                    datapath='#FORM.datore_lavoro',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')