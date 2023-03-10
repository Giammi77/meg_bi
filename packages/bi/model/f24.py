# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('f24',name_long='F24',name_plural='F24',pkey='id',caption_field='caption_f24')
        self.sysFields(tbl,user_upd=True)
        tbl.column('anagrafica_id',size='22', group='_', name_long='Utente'
                    ).relation('bi.anagrafica.id', relation_name='f24', mode='foreignkey', onDelete='raise')
        tbl.column('codice_fiscale',name_long='codice_fiscale',legacy_name='codice_fiscale')
        tbl.column('abi',name_long='abi',legacy_name='abi')
        tbl.column('cab',name_long='cab',legacy_name='cab')
        tbl.column('data_pagamento',dtype='D',name_long='data_pagamento',legacy_name='data_pagamento')
        tbl.column('codice_tributo',name_long='codice_tributo',legacy_name='codice_tributo')
        tbl.column('anno_tributo',dtype='L',name_long='anno_tributo',legacy_name='anno_tributo')
        tbl.formulaColumn('caption_f24',"COALESCE($abi,'')||' '||COALESCE($cab,'')||' '||COALESCE($data,'')")