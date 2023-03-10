# encoding: utf-8
from gnr.core.gnrdecorator import public_method  
from giammi import scriviDebug


class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('file', pkey='id', name_long='File', name_plural='Files',caption_field='nome_file')
        self.sysFields(tbl)
        tbl.column('nome_file', name_long='Nome File')
        tbl.column('tipo_file_id',size='22', group='_', name_long='Tipo File'
                    ).relation('bi.tipo_file.id', relation_name='file', mode='foreignkey', onDelete='raise')
    @public_method
    def importFile(self, sn_file_path=None,tipo_file_id=None):
        # A SECONDA DEL TIPO DI FILE VADO A ELABORARLO
            # ALIMENTO LE TABELLE DI IMPORTAZIONE A SECONDA DEL TIPO DI FILE 
        p=sn_file_path.move(self.db.application.site.storageNode(':documenti/', sn_file_path.basename, autocreate=-1)) 
        nome_file=sn_file_path.basename 
        esiste_file=self.readColumns(columns='$nome_file', where='$nome_file=:nome_file',nome_file=nome_file, ignoreMissing=True)
        if esiste_file:
            return
        rec_file=self.newrecord()
        rec_file['nome_file']=nome_file
        rec_file['tipo_file_id']=tipo_file_id
        self.insert(rec_file)
        sn_elaborazione = self.elabora_file_run(sn_file_path,tipo_file_id)
        self.db.table('bi.file_atc').addAttachment(maintable_id=rec_file['id'],
                            description = nome_file,
                            origin_filepath = sn_file_path.internal_path,
                            moveFile = True)
        
        nome_file_elaborazione=sn_elaborazione.basename
        self.db.table('bi.file_atc').addAttachment(maintable_id=rec_file['id'],
                            description = nome_file_elaborazione,
                            origin_filepath = sn_elaborazione.internal_path,
                            moveFile = True)

    def elabora_file_run(self,sn_file_path,tipo_file_id=None, **kwargs):
        qry_param=self.db.table('bi.parametro_file').query(where='$tipo_file_id =:tipo_file_id',tipo_file_id=tipo_file_id)
        parametri_tipo_file=qry_param.fetch() 
        descrizione,codice,str_validazione_row,tbl_name=self.db.table('bi.tipo_file'
                            ).readColumns(columns='$descrizione,$codice,$str_validazione_row,$tblinfo_tblid',
                                            where='$id =:id',id=tipo_file_id)
        self.btc = self.db.currentPage.btc if self.db.currentPage else None  # oggetto "batch" (tab dove viene mostrato la progress bar)
        self.btc.batch_create(title=f"Elaborazione File {descrizione}")
        rows=[]
        #  tbl.column('parametro', name_long='Parametro')
        # tbl.column('i_low_slice', name_long='Indice minore per slice')
        # tbl.column('i_high_slice', name_long='Indice maggiore per slice')
        	
        # intestazione=[('ABI',39,44),('CAB',45,50),('DATA BONIFICO',22,30),('CODICE FISCALE',49,65)]                   
        intestazione=[(p['parametro'],p['i_low_slice'],p['i_high_slice'],p['name_field']) for p in parametri_tipo_file]
        rows.append(''.join(f'{param[0]};' for param in intestazione)[:-1])
        lista_escludi_rows=[]
        with sn_file_path.open(mode='r') as myfile:
                lines=myfile.readlines()
                lines=lines[1:-1]
                for l in self.btc.thermo_wrapper(lines,message=descrizione):
                    row=''
                    dict_row=dict()
                    for param in intestazione:
                        v=l[param[1]:param[2]]
                        row+=f'{v};'
                        dict_row[param[3]]=v
                    if str_validazione_row:
                        if l.startswith(str_validazione_row):
                            rows.append(row[:-1])
                            self.inserisci_row(tbl_name,dict_row)
                        continue
                    rows.append(row[:-1])
                    self.inserisci_row(tbl_name,dict_row)
        url=None
        if len(rows)>0:
            nome_file_elaborazione=f'{codice.lower()}_elaborazione.csv'
            sn_elaborazione = self.db.application.site.storageNode('site:elaborazioni',nome_file_elaborazione)
            scriviDebug(self,dati=rows,sn=sn_elaborazione)
            url=sn_elaborazione.url()
        self.btc.batch_complete('Elaborazione Completata',
                                result_attr=dict(url = url))                
        return sn_elaborazione
    
    def inserisci_row(self,tbl_name,dict_row):
        codice_fiscale=dict_row.get('codice_fiscale')
        tbl_anagrafica=self.db.table('bi.anagrafica')
        if codice_fiscale:
            with tbl_anagrafica.recordToUpdate(codice_fiscale=codice_fiscale,
                                    insertMissing=True) as record:
                record['codice_fiscale'] = codice_fiscale
        anagrafica_id=record['id']
        tbl=self.db.table(tbl_name)
        rec=tbl.newrecord()
        for k,v in dict_row.items():
            rec[k]=v
        rec['anagrafica_id']=anagrafica_id
        tbl.insert(rec)