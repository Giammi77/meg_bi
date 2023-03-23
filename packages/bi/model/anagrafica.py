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

        tbl.formulaColumn('conta_pagopa',name_long='PagoPa',select=dict(table='bi.pagopa',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L') 

        tbl.formulaColumn('conta_bene_mobile',name_long='Bene Mobile',select=dict(table='bi.bene_mobile',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L') 

        tbl.formulaColumn('conta_bene_immobile',name_long='Bene Immobile',select=dict(table='bi.bene_immobile',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L') 

        tbl.formulaColumn('conta_conto_corrente',name_long='Conto Corrente',select=dict(table='bi.conto_corrente',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L') 

        tbl.formulaColumn('conta_datore_lavoro',name_long='Datore Lavoro',select=dict(table='bi.datore_lavoro',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L') 

        tbl.formulaColumn('bene_aggredibile',
                            """
                            case 
                                when 
                                    $conta_bene_mobile > 0 or
                                    $conta_bene_immobile > 0 or
                                    $conta_conto_corrente >0 or
                                    $conta_datore_lavoro > 0
                                then true 
                                else false 
                                end 
                            """, dtype='B')