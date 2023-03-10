#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from giammi import scriviDebug

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('istituto')
        r.fieldcell('abi')
        r.fieldcell('cab')
        r.fieldcell('indirizzo')
        r.fieldcell('sportello')
        r.fieldcell('citta')
        r.fieldcell('prov')
        r.fieldcell('cap')

    def th_order(self):
        return 'istituto'

    def th_query(self):
        return dict(column='istituto', op='contains', val='')

    def th_bottom_custom(self,bottom):
        bar = bottom.slotToolbar('*,importatore,*')
        bar.importatore.formbuilder().dropUploader(label='Drop the file to import here', width='300px', onUploadedMethod=self.db.table('bi.banca').importaFileJson,
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
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('istituto' )
        fb.field('abi' )
        fb.field('cab' )
        fb.field('indirizzo' )
        fb.field('sportello' )
        fb.field('citta' )
        fb.field('prov' )
        fb.field('cap' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
