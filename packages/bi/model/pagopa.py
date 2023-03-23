# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('pagopa', pkey='id', name_long='PagoPa', name_plural='PagoPa',caption_field='caption_pagopa')
        self.sysFields(tbl)
        tbl.column('anagrafica_id',size='22', group='_', name_long='Utente'
                    ).relation('bi.anagrafica.id', relation_name='pagopa', mode='foreignkey', onDelete='raise')
        tbl.column('file_id',size='22', group='_', name_long='File origine dati'
                    ).relation('bi.file.id', relation_name='pagopa', mode='foreignkey', onDelete='setnull')
        tbl.column('banca_istituto_id',size='22', group='_', name_long='Istituto Bancario'
                    ).relation('bi.banca_istituto.id', relation_name='pagopa', mode='foreignkey', onDelete='raise')
        tbl.column('banca_filiale_id',size='22', group='_', name_long='Filiale'
                    ).relation('bi.banca_filiale.id', relation_name='pagopa', mode='foreignkey', onDelete='raise')
        tbl.column('idpa', name_long='') 
        tbl.column('codice_fiscale', name_long='Codice Fiscale - Piva') 
        tbl.column('id_station', name_long='id_station')
        tbl.column('importo', name_long='importo')
        tbl.column('descrizione', name_long='descrizione')
        tbl.column('nominativo', name_long='nominativo')
        tbl.column('indirizzo', name_long='indirizzo')
        tbl.column('cap', name_long='cap')
        tbl.column('citta', name_long='citta')
        tbl.column('provincia', name_long='provincia')
        tbl.column('iban', name_long='iban')
        tbl.column('id_psp', name_long='id_psp')
        tbl.column('data', name_long='data')
        tbl.column('ente_creditore', name_long='Ente Creditore')
        tbl.column('da_eliminare', dtype='B')
        tbl.column('caricato', dtype='B')
        tbl.formulaColumn('caption_pagopa',"COALESCE($iban,'')||' '||COALESCE($data,'')")

    def trigger_onInserting(self, record=None):
        esiste=self.readColumns(columns='$id',where='$iban=:iban and $data>=:data and $anagrafica_id=:anagrafica_id',
                            iban=record['iban'],
                            data=record['data'],
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

    def get_dict_flds(self):
        return dict(
                    idPA='idpa',
                    entityUniqueIdentifierValue='codice_fiscale',
                    idStation='id_station',
                    paymentAmount='importo',
                    description='descrizione',
                    fullName='nominativo',
                    streetName='indirizzo',
                    postalCode='cap',
                    city='citta',
                    stateProvinceRegion='provincia',
                    IBAN='iban',
                    idPSP='id_psp',
                    paymentDateTime='data',
                    companyName='ente_creditore',
                    )