# encoding: utf-8

class Table(object): 
    def config_db(self,pkg):
        tbl =  pkg.table('anagrafica', name_long='Anagrafica', pkey='id', name_plural='Anagrafiche', caption_field='codice_fiscale')
        self.sysFields(tbl,user_upd=True)
        tbl.column('codice_fiscale',name_long='Codice Fiscale - Piva',validate_nodup=True)
        tbl.formulaColumn('conta_f24',name_long='F24',select=dict(table='bi.f24',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L')

        tbl.formulaColumn('conta_bonifico',name_long='Bonifico',select=dict(table='bi.bonifico',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L')       

        tbl.formulaColumn('conta_locazione',name_long='Locazione',select=dict(table='bi.locazione',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L') 

        tbl.formulaColumn('pagopa',name_long='PagoPa',select=dict(table='bi.pagopa',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L') 