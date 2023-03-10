# encoding: utf-8
from gnr.core.gnrdecorator import public_method  
from giammi import scriviDebug
import json

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('banca', pkey='id', name_long='Istituto Bancario', name_plural='Istituti Bancari',caption_field='istituto')
        self.sysFields(tbl)
        tbl.column('istituto', name_long='Istituto')
        tbl.column('abi', name_long='Abi') 
        tbl.column('cab', name_long='Cab') 
        tbl.column('indirizzo', name_long='Indirizzo')
        tbl.column('sportello', name_long='Sportello')
        tbl.column('citta', name_long='Citta')
        tbl.column('prov', name_long='Provincia')
        tbl.column('cap', name_long='Cap')
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
            for row in self.btc.thermo_wrapper(rows,message='Import json'):
                rec=self.newrecord()
                rec['istituto']=row['istituto']
                rec['abi']=row['abi']
                rec['cab']=row['cab']
                rec['indirizzo']=row['indirizzo']
                rec['citta']=row['citta']
                rec['sportello']=row['sportello']
                rec['cap']=row['cap']
                rec['prov']=row['prov']
                self.insert(rec)
                self.db.commit()
        self.btc.batch_complete('Completata',
                                result_attr=None)                
        return dict()