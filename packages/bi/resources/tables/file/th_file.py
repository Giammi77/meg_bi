#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from giammi import unzip

class View(BaseComponent):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('__ins_ts')
        r.fieldcell('nome_file',width='30em')
        r.fieldcell('tipo_file_id')

    def th_order(self):
        return 'nome_file'

    def th_query(self):
        return dict(column='nome_file', op='contains', val='')

    def th_top_custom(self,top):
        top.slotToolbar('sections@tipo_file_id,*', childname='lower', _position='>bar')
 
    def th_bottom_custom(self,bottom):
        bar = bottom.slotToolbar('tipo_file,importatore,*,elimina')  # '20,trasferisci,*,importatore,*'
        # ESEMPIO PER PASSARE UN VALORE DA DATA STORE ALLA Rpc
        # bar.importatore.PaletteImporter(paletteCode='file_importer' , title='!!Importa File',
        #                                     dockButton_iconClass='iconbox inbox',
        #                                     dockButton_label='Importa',
        #                                     dockButton_showLabel=True,  # !
        #                                     importButton_label='Importa',
        #                                     dockButton_disabled=False, #'^current.current_partition_value?=!#v'
        #                                     importButton_tipo_file_id = '=tipo_file_id',
        #                                     importButton_action="""
        #                                                         genro.publish('importa',{filepath:imported_file_path,
        #                                                         tipo_file_id:tipo_file_id})
        #                                                          """)

        #FUNZIONA LASCIO COME ESEMPIO PER LANCIARE LA ASK
        # bar.importatore.PaletteImporter(paletteCode='file_importer' , title='!!Importa File',
        #                                     dockButton_iconClass='iconbox inbox',
        #                                     dockButton_label='Importa',
        #                                     dockButton_showLabel=True,  # !
        #                                     importButton_label='Importa',
        #                                     dockButton_disabled=False, #'^current.current_partition_value?=!#v'
        #                                     importButton_tipo_file_id = '=tipo_file_id',
        #                                     importButton_ask=dict(title='!!Seleziona Tipo File',fields=[dict(name='tipo_file_id',
        #                                                     lbl='Tipo File', width='240px',tag='dbselect', table='bi.tipo_file', order_by='$codice',hasDownArrow=True,
        #                                                     validate_notnull=True),
        #                                     ]),
        #                                     keepFilename=True,
        #                                     matchColumns='*',
        #                                     importButton_action="""
        #                                                         genro.mainGenroWindow.genro.publish('open_batch');
        #                                                         genro.publish('importa',{file_path:imported_file_path,
        #                                                         tipo_file_id:tipo_file_id})
        #                                                             """)

        # TEST MULTIUPLOADER
        # fb = bar.uploader.formbuilder()
        # uploader = fb.button('Importa files')
        # uploader.dataController("""
        #                         genro.dlg.multiUploaderDialog('Importa files',{
        #                                     uploadPath:uploadPath,
        #                                     onResult:function(){
        #                                         genro.publish("floating_message",{message:"Upload completato", messageType:"message"});
        #                                         genro.publish('trigger_action',{tipo_file_id:tipo_file_id}); }
        #                                     });""", 
        #                                     uploadPath=':import_queue', 
        #                                     _ask=dict(title='Seleziona bTipo files', 
        #                                               fields=[dict(name='tipo_file_id',
        #                                                     lbl='Tipo File', width='240px',tag='dbselect', table='bi.tipo_file', order_by='$codice',hasDownArrow=True,
        #                                                     validate_notnull=True),
        #                                     ]))


        # fb.dataRpc(self.triggerAnAction, subscribe_trigger_action=True)o
        
        fb = bar.tipo_file.formbuilder()
        fb.dbSelect(value='^tipo_file_id', dbtable='bi.tipo_file',
                    order_by = '$codice',
                    lbl='Scegli Tipo File', hasDownArrow=True, width='16em', placeholder='nessuna selezione',validate_notnull=True)
        fb = bar.importatore.formbuilder()
        fb.dropUploader(label='Drop the file to import here', width='300px', uploadPath=':temp_import_file',
                        onResult="""var tipo_file_id = GET tipo_file_id;var uploadPath = ':temp_import_file';
                                    genro.mainGenroWindow.genro.publish('open_batch');
                                    genro.publish('importa',{tipo_file_id:tipo_file_id,temp_import_path:uploadPath});""",
                                    tipo_file_id='=tipo_file_id',
                                    progressBar=True,
                                    disabled='^tipo_file_id?=!#v'
                                    )
        bar.dataRpc(None,self.importaFile,_onResult="FIRE .runQueryDo",
                    subscribe_importa=True)
        fb = bar.elimina.formbuilder()
        fb.button('Elimina').dataRpc(self.eliminaFileTemp)
        
    @public_method
    def eliminaFileTemp(self,*args,**kwargs):
        sn = self.db.application.site.storageNode(':temp_import_file')
        sn_unzip=self.db.application.site.storageNode('site:unzip',autocreate=-1)
        sn.delete()
        sn_unzip.delete()

    @public_method
    def importaFile(self,*args,**kwargs):

        # kwargs{'filepath': 'page:file_importer_uploader/file_importerlatest.xls', 'tipo_file_id': 'x5RxNuVCNbiwNJV3WwZ0_A'}
        sn_zip=None
        temp_import_path=kwargs['temp_import_path']
        tipo_file_id=kwargs['tipo_file_id']
        sn = self.db.application.site.storageNode(temp_import_path)
        sn_children = sn.children()
        if len(sn_children)==0:
            return
        sn_file_path = self.db.application.site.storageNode(sn_children[0])
        is_zip = sn_file_path.basename.endswith('.zip')
        if is_zip:
            sn_zip=sn_file_path
            sn_unzip=self.db.application.site.storageNode('site:unzip',autocreate=-1)
            unzip(sn_unzip, sn_file_path)
            unzip_children=sn_unzip.children()
            if len(unzip_children)==0:
                return
            sn_children = unzip_children
        result=self.tblobj.importFile(sn_children=sn_children,tipo_file_id=tipo_file_id,sn_zip=sn_zip)
        self.db.commit()
        sn.delete()
        if is_zip:
            sn_unzip.delete()
        return dict(closeImporter=True)


    # @public_method
    # def triggerAnAction(self, user_id=None, category=None, **kwargs):
    #     print(x)
    #     sn = self.db.application.site.storageNode('site:import_queue')
    #     for node in sn.children():
    #         node.move('site:files/{user}/'.format(user=user_id))
    #         print('FILE MOVED: ', node.internal_path)

class Form(BaseComponent):

    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"
                   

    def th_form(self, form):
        bc = form.center.borderContainer()
        
        top_bc = bc.roundedGroup(title='Dati File', region='top',height='10%', splitter = True)
        fb = top_bc.formbuilder(cols=2, border_spacing='4px', datapath='.record')
        fb.field('nome_file' )
        fb.field('tipo_file_id' )

        tc = bc.tabContainer(region='center', margin='2px')
        allegati_pane = tc.contentPane(title='Files')
        allegati_pane.attachmentGrid(margin='2px',uploaderButton=True)  # alternative: attachmentMultiButtonFrame() o attachmentGrid()
        tc.contentPane(title='Bonifici').plainTableHandler(relation='@bonifico',
                                    datapath='#FORM.bonifico',
                                    viewResource='ViewFromAnagrafica',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

        tc.contentPane(title='Locazioni' ).plainTableHandler(relation='@locazione',
                                    datapath='#FORM.locazione',
                                    viewResource='ViewFromAnagrafica',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)
        
        tc.contentPane(title='F24' ).plainTableHandler(relation='@f24',
                                    datapath='#FORM.f24',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

        tc.contentPane(title='PagoPa' ).plainTableHandler(relation='@pagopa',
                                    datapath='#FORM.pagopa',
                                    margin='2px',
                                    dialog_windowRatio='0.8',
                                    searchOn=True,
                                    pbl_classes=True,
                                    export=True,
                                    condition_onStart=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
        

