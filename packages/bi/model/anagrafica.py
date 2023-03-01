# encoding: utf-8

class Table(object): 
    def config_db(self,pkg):
        tbl =  pkg.table('anagrafica', name_long='Anagrafica', pkey='id', name_plural='Anagrafiche', caption_field='nominativo')
        self.sysFields(tbl,user_upd=True)
        tbl.column('email',name_long='email',legacy_name='Email')
        tbl.column('pec',name_long='pec',legacy_name='Pec')###
        tbl.column('societa', dtype='B', name_long='societa',legacy_name='societa')
        tbl.column('codice_fiscale',name_long='codice_fiscale',legacy_name='codice_fiscale')
        tbl.column('cognome',name_long='cognome',legacy_name='cognome')
        tbl.column('nome',name_long='nome',legacy_name='nome')
        tbl.column('indirizzo',name_long='indirizzo',legacy_name='indirizzo')###
        tbl.column('cap',size='5',name_long='cap',legacy_name='cap')###
        tbl.column('comune_di_residenza',name_long='comune_di_residenza',legacy_name='comune_di_residenza')###
        tbl.column('prov',name_long='prov',legacy_name='prov')###
        tbl.column('cod_utente',name_long='cod_utente',legacy_name='cod_utente')
        tbl.column('n_ord',name_long='n_ord',legacy_name='n_ord')
        tbl.column('datanascita',dtype='D',name_long='data_nascita')
        tbl.column('luogonascita',name_long='luogonascita',legacy_name='luogonascita')
        tbl.column('provnascita',name_long='provnascita',legacy_name='provnascita')
        tbl.column('invita',dtype='B', name_long='invita',legacy_name='invita')
        tbl.column('datadecesso',dtype='D',name_long='data_decesso')
        tbl.column('note',name_long='note')
        tbl.column('nazione', size='2', name_long='Nazione')
        tbl.column('ultimoaggiornamento',dtype='D',name_long='ultimo aggiornamento')###
        tbl.column('trasferito_ts', dtype='DH', name_long='trasferito ts')
    
        tbl.formulaColumn('nominativo', "COALESCE($cognome,'')||' ' || COALESCE($nome,'')", name_long='Nominativo')

        tbl.formulaColumn('conta_f24',select=dict(table='bi.f24',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L')

        tbl.formulaColumn('conta_bonifico',select=dict(table='bi.bonifico',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L')       

        tbl.formulaColumn('conta_locazione',select=dict(table='bi.locazione',
                                                    columns='COALESCE(COUNT($id),0)',
                                                    where="""$anagrafica_id=#THIS.id
                                                    """),dtype='L')                                                   