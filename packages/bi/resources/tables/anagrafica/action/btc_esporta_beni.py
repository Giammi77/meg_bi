#import os
#from shutil import copyfile
from gnr.web.batch.btcaction import BaseResourceAction
from gnr.core.gnrlang import GnrException
# from gnr.lib.services.storage import StorageNode
# from gnr.core.gnrstring import slugify, splitAndStrip
caption = 'Esporta Beni'
description = 'Esporta Beni' 
tags='admin'

class Main(BaseResourceAction):
    batch_prefix = 'exp_b'
    batch_title = 'Esporta Beni'
    batch_cancellable = True
    batch_immediate = False
    batch_delay = 0.5
    
    def do(self):
        pkeys=self.get_selection_pkeys()
        if len(pkeys)==0:
             raise GnrException("Seleziona Soggetti")
        self.logs=[]
        self.esportati=0
        tabelle=['bi.conto_corrente','bi.bene_mobile','bi.bene_immobile','bi.datore_lavoro'] 
        
        for tbl in tabelle:
            current_esportati,sn_log=self.db.table(tbl).esporta_beni(btc=self.btc,anagrafica_ids=pkeys)
            self.esportati+=current_esportati
            if sn_log:
                self.logs.append(sn_log)

    def result_handler(self):  
        export_mode = 'zip'
        nomeFile='esportazione'
        zipNode = self.db.application.site.storageNode('site:esportazioni',export_mode,'%s.%s' % (nomeFile, export_mode), autocreate=-1)
        self.db.application.site.zipFiles(file_list=self.logs,zipPath=zipNode)
        url=zipNode.url()
        return f'Esportazione Completata <br>Beni Esportati = {self.esportati}',dict(url = url, document_name=nomeFile)                
                                