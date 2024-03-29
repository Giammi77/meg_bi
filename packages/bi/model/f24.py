# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('f24',name_long='F24',name_plural='F24',pkey='id',caption_field='caption_f24')
        self.sysFields(tbl,user_upd=True)
        tbl.column('anagrafica_id',size='22', group='_', name_long='Utente'
                    ).relation('bi.anagrafica.id', relation_name='f24', mode='foreignkey', onDelete='raise')
        tbl.column('banca_istituto_id',size='22', group='_', name_long='Istituto Bancario'
                    ).relation('bi.banca_istituto.id', relation_name='f24', mode='foreignkey', onDelete='raise')
        tbl.column('banca_filiale_id',size='22', group='_', name_long='Filiale'
                    ).relation('bi.banca_filiale.id', relation_name='f24', mode='foreignkey', onDelete='raise')
        tbl.column('file_id',size='22', group='_', name_long='File origine dati'
                    ).relation('bi.file.id', relation_name='f24', mode='foreignkey', onDelete='setnull')
        tbl.column('codice_fiscale',name_long='codice_fiscale',legacy_name='codice_fiscale')
        tbl.column('abi',name_long='abi',legacy_name='abi')
        tbl.column('cab',name_long='cab',legacy_name='cab')
        tbl.column('data_pagamento',dtype='D',name_long='data_pagamento',legacy_name='data_pagamento')
        tbl.column('codice_tributo',name_long='codice_tributo',legacy_name='codice_tributo')
        tbl.column('anno_tributo',dtype='L',name_long='anno_tributo',legacy_name='anno_tributo')
        tbl.column('log_errore',name_long='Log Errore')
        tbl.column('da_eliminare', dtype='B')
        tbl.column('caricato', dtype='B')
        tbl.formulaColumn('caption_f24',"COALESCE($abi,'')||' '||COALESCE($cab,'')||' '||COALESCE($data_pagamento,'')")

    def trigger_onInserting(self, record=None):
        esiste=self.readColumns(columns='$id',where='$cab=:cab and $abi=:abi and $data_pagamento>=:data and $anagrafica_id=:anagrafica_id',
                            cab=record['cab'],
                            abi=record['abi'],
                            data=record['data_pagamento'],
                            anagrafica_id=record['anagrafica_id'],
                            ignoreMissing=True)   
        record['da_eliminare'] = True if esiste else False  
    
    def carica_beni(self,btc):
        caricati=0
        tbl_cc=self.db.table('bi.conto_corrente')
        r_beni=self.query(where='$caricato is not true').fetch()
        for r in btc.thermo_wrapper(r_beni,message='Elaborazione'):
            rec=tbl_cc.newrecord()
            rec['anagrafica_id']=r['anagrafica_id']
            rec['banca_istituto_id']=r['banca_istituto_id']
            rec['banca_filiale_id']=r['banca_filiale_id']
            rec['file_id']=r['file_id']
            tbl_cc.insert(rec)
            caricati+=1
            with self.recordToUpdate(id=r['id']) as record:
                record['caricato'] = True
        return caricati

