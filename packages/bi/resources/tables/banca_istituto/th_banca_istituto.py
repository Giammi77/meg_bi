#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('istituto')
        r.fieldcell('abi')

    def th_order(self):
        return 'istituto'

    def th_query(self):
        return dict(column='istituto', op='contains', val='')

    def th_bottom_custom(self,bottom):
        bar = bottom.slotToolbar('*,importatore,*')
        bar.importatore.formbuilder().dropUploader(label='Drop the file to import here', width='300px', onUploadedMethod=self.db.table('bi.banca_istituto').importaFileJson,
                        onResult="FIRE .runQueryDo", progressBar=True)
        # bar.importatore.PaletteImporter(paletteCode='file_importer' , title='!!Importa json',
        #                                     dockButton_iconClass='iconbox inbox',
        #                                     dockButton_label='Importa',
        #                                     dockButton_showLabel=True,  # !
        #                                     importButton_label='Importa',
        #                                     dockButton_disabled=False, #'^current.current_partition_value?=!#v'
        #                                     importButton_action="""
        #                                                         genro.publish('importa',{file_path:imported_file_path,
        #                                                         })

class Form(BaseComponent):
    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top',height='6%',splitter=True).formbuilder(cols=1, border_spacing='4px', datapath='.record')
        fb.field('istituto')
        fb.field('abi')
        tab = bc.tabContainer(region='center', margin='2px')
        tab.contentPane(title='Filiali').inlineTableHandler(relation='@banca_filiale',datapath='#FORM.banca_filiale', viewResource='ViewFromBancaIstituto',configurable=True)    

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
