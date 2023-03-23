# encoding: utf-8
from gnr.core.gnrdecorator import public_method  
from giammi import scriviDebug
import json

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('banca_istituto', pkey='id', name_long='Istituto Bancario', name_plural='Istituti Bancari',caption_field='istituto')
        self.sysFields(tbl)
        tbl.column('istituto', name_long='Istituto')
        tbl.column('abi', name_long='ABI') 
        # {"istituto":"BANCA D'ITALIA","abi":"01000","cab":"01000","":"VIA ARSENALE, 8","citta":"TORINO","cap":"10121","prov":"TO",
        #  "sportello":"AG. VIA ARSENALE, 8"}

    @public_method
    def importaFileJson(self,*args,**kwargs):
        self.btc = self.db.currentPage.btc if self.db.currentPage else None  # oggetto "batch" (tab dove viene mostrato la progress bar)
        self.btc.batch_create(title='Import json istituti bancari')
        file_path=kwargs['file_path']
        sn_file_path = self.db.application.site.storageNode(file_path)
        with sn_file_path.open(mode='r') as myfile:
            lines=myfile.readlines()
            rows = json.loads(lines[0]) 
        # {"istituto":"BANCA D'ITALIA","abi":"01000","cab":"01000","":"VIA ARSENALE, 8","citta":"TORINO","cap":"10121","prov":"TO",
        #  "sportello":"AG. VIA ARSENALE, 8"}
            tbl_banca_filiale=self.db.table('bi.banca_filiale')
            for row in self.btc.thermo_wrapper(rows,message='Import json'):
                banca_istituto_id=self.readColumns(columns='$id',where='$abi=:abi and $istituto=:istituto',abi=row['abi']
                                                    ,istituto=row['istituto'], ignoreMissing=True)
                if not banca_istituto_id:
                    rec=self.newrecord()
                    rec['istituto']=row['istituto']
                    rec['abi']=row['abi']
                    self.insert(rec)
                banca_filiale_id=tbl_banca_filiale.readColumns(columns='$id',where='$cab=:cab',cab=row['cab'],ignoreMissing=True)
                if not banca_filiale_id:
                    rec=tbl_banca_filiale.newrecord()
                    rec['banca_istituto_id']=banca_istituto_id
                    rec['cab']=row['cab']
                    rec['indirizzo']=row['indirizzo']
                    rec['citta']=row['citta']
                    rec['sportello']=row['sportello']
                    rec['cap']=row['cap']
                    rec['prov']=row['prov']
                    tbl_banca_filiale.insert(rec)
                self.db.commit()
        self.btc.batch_complete('Completata',
                                result_attr=None)                
        return dict()