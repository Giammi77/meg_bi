# encoding: utf-8

class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('bonifico',name_long='Bonifico',name_plural='Bonifici', pkey='id',caption_field='caption_bonifico')
        self.sysFields(tbl,user_upd=True)
        tbl.column('anagrafica_id',size='22', group='_', name_long='Utente'
                    ).relation('bi.anagrafica.id', relation_name='bonifico', mode='foreignkey', onDelete='raise')
        tbl.column('banca_id',size='22', group='_', name_long='Istituto Bancario'
                    ).relation('bi.banca.id', relation_name='bonifico', mode='foreignkey', onDelete='raise')
        tbl.column('file_id',size='22', group='_', name_long='File origine dati'
                    ).relation('bi.file.id', relation_name='bonifico', mode='foreignkey', onDelete='setnull')
        tbl.column('tipo_record',name_long='tipo_record',legacy_name='tipo_record')
        tbl.column('tipo_fornitura',name_long='tipo_fornitura',legacy_name='tipo_fornitura')
        tbl.column('anno',dtype='L',name_long='anno',legacy_name='anno')
        tbl.column('ccodcat',name_long='ccodcat',legacy_name='ccodcat')
        tbl.column('codice_fiscale',name_long='codice_fiscale',legacy_name='codice_fiscale')
        tbl.column('abi',name_long='abi',legacy_name='abi')
        tbl.column('cab',name_long='cab',legacy_name='cab')
        tbl.column('data',dtype='D',name_long='data',legacy_name='data')
        tbl.column('da_eliminare', dtype='B')
        tbl.formulaColumn('caption_bonifico',"COALESCE($abi,'')||' '||COALESCE($cab,'')||' '||COALESCE($data,'')")

    def trigger_onInserting(self, record=None):
        esiste=self.readColumns(columns='$id',where='$cab=:cab and $abi=:abi and $data>=:data and $anagrafica_id=:anagrafica_id',
                            cab=record['cab'],
                            abi=record['abi'],
                            data=record['data'],
                            anagrafica_id=record['anagrafica_id'],
                            ignoreMissing=True)   
        record['da_eliminare'] = True if esiste else False  