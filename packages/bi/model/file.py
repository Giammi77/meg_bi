# encoding: utf-8
from gnr.core.gnrdecorator import public_method  
from giammi import scriviDebug,getAbiCab_fromIban
from gnr.core.gnrbag import Bag  

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('file', pkey='id', name_long='File', name_plural='Files',caption_field='nome_file')
        self.sysFields(tbl)
        tbl.column('nome_file', name_long='Nome File')
        tbl.column('tipo_file_id',size='22', group='_', name_long='Tipo File'
                    ).relation('bi.tipo_file.id', relation_name='file', mode='foreignkey', onDelete='raise')
    @public_method
    def importFile(self, sn_children=None,tipo_file_id=None,sn_zip=None):
        self.trovati=0
        # A SECONDA DEL TIPO DI FILE VADO A ELABORARLO
        # ALIMENTO LE TABELLE DI IMPORTAZIONE A SECONDA DEL TIPO DI FILE 
        self.btc = self.db.currentPage.btc if self.db.currentPage else None  # oggetto "batch" (tab dove viene mostrato la progress bar)
        self.btc.batch_create(title=f"Elaborazione File")
        if sn_zip:
            nome_file=sn_zip.basename 
            esiste_file=self.readColumns(columns='$nome_file', where='$nome_file=:nome_file',nome_file=nome_file, ignoreMissing=True)
            if esiste_file:
                self.btc.batch_complete(f'File già importato in precedenza',
                                result_attr=dict())                
                return
            rec_file=self.newrecord()
            rec_file['nome_file']=nome_file
            rec_file['tipo_file_id']=tipo_file_id
            self.insert(rec_file)
            file_id=rec_file['id']
            self.db.table('bi.file_atc').addAttachment(maintable_id=rec_file['id'],
                                description = nome_file,
                                origin_filepath = sn_zip.internal_path,
                                moveFile = True)
            for sn_file_path in self.btc.thermo_wrapper(sn_children,message='Elaborazione'):
                tbl_name = self.elabora_file_run(sn_file_path,tipo_file_id,file_id)
                # nome_file_elaborazione=sn_elaborazione.basename
                # self.db.table('bi.file_atc').addAttachment(maintable_id=rec_file['id'],
                #                     description = nome_file_elaborazione,
                #                     origin_filepath = sn_elaborazione.internal_path,
                #                     moveFile = True)
        else:
            for sn_file_path in self.btc.thermo_wrapper(sn_children,message='Elaborazione'):
                nome_file=sn_file_path.basename 
                esiste_file=self.readColumns(columns='$nome_file', where='$nome_file=:nome_file',nome_file=nome_file, ignoreMissing=True)
                if esiste_file:
                    self.btc.batch_complete(f'File già importato in precedenza',
                                result_attr=dict())                
                    return
                rec_file=self.newrecord()
                rec_file['nome_file']=nome_file
                rec_file['tipo_file_id']=tipo_file_id
                self.insert(rec_file)
                file_id=rec_file['id']
                tbl_name = self.elabora_file_run(sn_file_path,tipo_file_id,file_id)
                self.db.table('bi.file_atc').addAttachment(maintable_id=rec_file['id'],
                                    description = nome_file,
                                    origin_filepath = sn_file_path.internal_path,
                                    moveFile = True)
                # nome_file_elaborazione=sn_elaborazione.basename
                # self.db.table('bi.file_atc').addAttachment(maintable_id=rec_file['id'],
                #                     description = nome_file_elaborazione,
                #                     origin_filepath = sn_elaborazione.internal_path,
                #                     moveFile = True)

        self.db.table(tbl_name).deleteSelection(where='$file_id=:id and $da_eliminare is true', id=file_id)
        trovati=self.db.table(tbl_name).query(where='$file_id=:id', id=file_id).count()
        self.btc.batch_complete(f'Elaborazione Completata <br> Beni Trovati: {trovati}',
                                result_attr=dict())                

    def elabora_file_run(self,sn_file_path,tipo_file_id=None,file_id=None, **kwargs):
        qry_param=self.db.table('bi.parametro_file').query(where='$tipo_file_id =:tipo_file_id',tipo_file_id=tipo_file_id)
        parametri_tipo_file=qry_param.fetch() 
        parametri_per_header=qry_param.fetchGrouped(key='header_parametro')
        dict_intestazioni=dict()
        intestazioni_qry=[]
        for h,parametri in parametri_per_header.items():
            dict_intestazioni[h]=[]
            for p in parametri:
                dict_intestazioni[h].append((['parametro'],p['i_low_slice'],p['i_high_slice'],p['name_field'],p['dtype']))
                if not p['parametro'] in intestazioni_qry:
                    intestazioni_qry.append(p['parametro'])
        for header in parametri_per_header:
            if header:
                self.create_tbl(name=header, parametri=dict_intestazioni[header])
        descrizione,codice,str_validazione_row,tbl_name,drop_first,drop_last,is_xml=self.db.table('bi.tipo_file'
                            ).readColumns(columns='$descrizione,$codice,$str_validazione_row,$tblinfo_tblid,$drop_first,$drop_last,$is_xml',
                                            where='$id =:id',id=tipo_file_id)
        rows=[]
        intestazione=[(p['parametro'],p['i_low_slice'],p['i_high_slice'],p['name_field'],p['datapath']) for p in parametri_tipo_file]
        rows.append(''.join(f'{param[0]};' for param in intestazione)[:-1])
        step=[1,2]
        for i in self.btc.thermo_wrapper(step,message='Elaborazione dati'):
            if i==1:
                with sn_file_path.open(mode='r') as myfile:
                    lines=myfile.readlines()
                    if drop_first:
                        lines=lines[1:]
                    if drop_last:
                        lines=lines[:-1]
                    if is_xml:
                        dict_row=self.read_xml(str_xml=lines[0],intestazione=intestazione)
                        rec = self.inserisci_row(tbl_name,dict_row,file_id)
                    else:   
                        for l in self.btc.thermo_wrapper(lines,message=descrizione):
                            if len(dict_intestazioni)>1:
                                self.inserisci_row_tbl(dict_intestazioni, l)
                                continue
                            row=''
                            dict_row=dict()
                            for param in intestazione:
                                v=l[param[1]:param[2]]
                                row+=f'{v};'
                                dict_row[param[3]]=v
                                continue
                            if str_validazione_row:
                                if l.startswith(str_validazione_row):
                                    rec = self.inserisci_row(tbl_name,dict_row,file_id)
                                    if rec['da_eliminare']is not True:
                                        rows.append(row[:-1])
                                continue
                            rec= self.inserisci_row(tbl_name,dict_row,file_id)
                            if rec['da_eliminare']is not True:
                                rows.append(row[:-1])
            elif i==2:
                if len(dict_intestazioni)>1:
                    rows=[]
                    qry=self.qry_locazione()
                    q=qry[0]
                    lista_intestazioni_csv=list()
                    for c in qry[0].keys():
                        lista_intestazioni_csv.append(c)
                    rows.append(''.join(f'{k};' for k in qry[0].keys())[:-1])
                    for r in self.btc.thermo_wrapper(qry,message='Inserimento dati qry'):
                        row='' 
                        riga=[]
                        for i in lista_intestazioni_csv:
                            v=r[i]
                            if v is None:
                                v=''
                            row+=f'{v};'
                        rec = self.inserisci_row(tbl_name,r,file_id)
                        if rec['da_eliminare']is not True:
                            rows.append(row[:-1])
            # else:
            #     if len(rows)>0:
            #         nome_file_elaborazione=f'{codice.lower()}_elaborazione.csv'
            #         sn_elaborazione = self.db.application.site.storageNode('site:elaborazioni',nome_file_elaborazione)
            #         scriviDebug(self,dati=rows,sn=sn_elaborazione)
            #         url=sn_elaborazione.url()
        return tbl_name

    def inserisci_row(self,tbl_name,dict_row,file_id):
        tbl_istituto=self.db.table('bi.banca_istituto')
        tbl_filiale=self.db.table('bi.banca_filiale')
        lista_per_banca=['bi.bonifico','bi.f24','bi.pagopa']
        codice_fiscale=dict_row.get('codice_fiscale') or dict_row.get('identificativo_soggetto')
        tbl_anagrafica=self.db.table('bi.anagrafica')
        anagrafica_id=tbl_anagrafica.readColumns(columns='$id',where='$codice_fiscale=:codice_fiscale',codice_fiscale=codice_fiscale,ignoreMissing=True)
        if not anagrafica_id:
            with tbl_anagrafica.recordToUpdate(codice_fiscale=codice_fiscale,
                                    insertMissing=True) as record:
                record['codice_fiscale'] = codice_fiscale
            anagrafica_id=record['id']
        tbl=self.db.table(tbl_name)
        rec=tbl.newrecord()
        rec['file_id']=file_id
        for k,v in dict_row.items():
            if v=='':
                v=None
            rec[k]=v
        rec['anagrafica_id']=anagrafica_id
        if tbl_name in lista_per_banca:
            abi,cab=getAbiCab_fromIban(dict_row.get('iban'))
            abi=dict_row.get('abi',abi)
            cab=dict_row.get('cab',cab)
            banca_istituto_id=self.db.table('bi.banca_istituto'
                    ).readColumns(columns='$id',
                                  where='$abi=:abi',abi=abi,ignoreMissing=True)
            banca_filiale_id=self.db.table('bi.banca_filiale'
                    ).readColumns(columns='$id',
                                  where='$cab=:cab',cab=cab,ignoreMissing=True)
            if not banca_istituto_id:
                rec_banca_istituto=tbl_istituto.newrecord() 
                rec_banca_istituto['abi']=abi
                tbl_istituto.insert(rec_banca_istituto) 
            if not banca_filiale_id:
                rec_banca_filiale=tbl_filiale.newrecord() 
                rec_banca_filiale['cab']=cab
                rec_banca_filiale['banca_istituto_id']=banca_istituto_id or rec_banca_istituto['id']
                tbl_filiale.insert(rec_banca_filiale)
            rec['banca_istituto_id']=banca_istituto_id 
            rec['banca_filiale_id']=banca_filiale_id 
        tbl.insert(rec)
        return rec 

    # FUNZIONE DEPRECATA, SIAMO PASSATI AD USAREL LE TABELLE TMP
    def elabora_per_headers(self,dict_intestazioni, l):
        header=l[0]
        intestazione=dict_intestazioni[header]
        dict_row=dict()
        for param in intestazione:
            v=l[param[1]:param[2]]
            if param[3]=='codice':
                codice=v
            dict_row[param[3]]=v
        return codice,header,dict_row       

    def inserisci_row_tbl(self,dict_intestazioni, l):
        header=l[0]
        values= ','.join(''.join(f"'{l[param[1]:param[2]].strip()}'") for param in dict_intestazioni[header])
        flds=self.get_flds(parametri=dict_intestazioni[header],for_insert=True)
        sql_insert=f"INSERT INTO  bi.bi_tmp{header.lower()} ({flds}) VALUES({values});"
        self.db.execute(sql_insert)
        self.db.commit()

    def create_tbl(self,name=None,parametri=None):
        flds=self.get_flds(parametri)
        sql_create_tbl=f"CREATE TABLE IF NOT EXISTS bi.bi_tmp{name} ({flds});"
        sql_truncate_tbl=f"TRUNCATE TABLE bi.bi_tmp{name};"
        self.db.execute(sql_create_tbl)
        self.db.execute(sql_truncate_tbl)
        self.db.commit()

    def get_flds(self,parametri=None, for_insert=None):
        campi=[]
        for p in parametri:
            field=dict(nome=p[3],dtype=p[4])
            campi.append(field)
        if for_insert:
            return ','.join(''.join(f"{campo['nome']}") for campo in campi)
        return ','.join(''.join(f'"{campo["nome"]}" {campo.get("dtype")}') for campo in campi)

    def qry_locazione(self):
        qry="""
        SELECT  a.codice, a.regcontr, a.ufficio, a.serie, a.numero, a.tipologia, a.durata_dal, a.durata_al, a.data_stipula, a.importo_canone,
                b.d_a, b.identificativo_soggetto, b.inizio_rapporto, b.fine_rapporto, 
                i.codice_comune, i.t_u, i.i_p, i.sezione_urbana, i.foglio, i.particella, i.sub
        FROM bi.bi_tmpa a
        INNER JOIN bi.bi_tmpb b ON a.codice = b.codice
        INNER JOIN bi.bi_tmpi i ON a.codice = i.codice
        WHERE b.fine_rapporto = '';
        """
        qry=self.db.execute(qry).fetchall()
        return qry

    def read_xml(self,str_xml=None, intestazione=None):
        dict_row=dict()
        bag=Bag()
        bag.fromXml(str_xml)
        for param in intestazione:
            v=bag[f'#0.{param[4]}']
            dict_row[param[3]]=v
        return dict_row