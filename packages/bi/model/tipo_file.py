# jncoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tipo_file', pkey='id', name_long='Tipo File', name_plural='Tipo File', caption_field='codice')
        self.sysFields(tbl)
        tbl.column('codice', size=':22', name_long='Codice')
        tbl.column('descrizione', name_long='Descrizione')
        tbl.column('note', name_long='Note')
        tbl.column('str_validazione_row', name_long='Stringa Validazione Riga')
        tbl.column('is_xml', dtype='B', name_long='XML')
        tbl.column('is_json', dtype='B', name_long='JSON')
        tbl.column('drop_first', dtype='B', name_long='Salta Prima Linea',name_short='S.P')
        tbl.column('drop_last', dtype='B', name_long='Salta Ultima Linea',name_short='S.L.')
        tbl.column('tblinfo_tblid', size=':50', name_long='Tabella'
                    ).relation('adm.tblinfo.tblid', relation_name='tipo_file', mode='foreignkey', onDelete='raise')
        # TIPO FILE = FB24....
        # TIPO FILE = FB24....
        # TIPO FILE = FB24....
        # TIPO FILE = FB24...dsajkf
        # 