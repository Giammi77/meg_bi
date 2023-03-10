# encoding: utf-8

class Table(object): 
    def config_db(self,pkg):
        tbl =  pkg.table('anagrafica', name_long='Anagrafica', pkey='id', name_plural='Anagrafiche', caption_field='codice_fiscale')
        self.sysFields(tbl,user_upd=True)
        tbl.column('codice_fiscale',name_long='Codice Fiscale - Piva',validate_nodup=True)