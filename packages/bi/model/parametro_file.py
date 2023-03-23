# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('parametro_file', pkey='id', name_long='Parametro File', name_plural='Parametri File',caption_field='parametro')
        self.sysFields(tbl)
        tbl.column('tipo_file_id',size='22', group='_', name_long='Tipo File'
                    ).relation('bi.tipo_file.id', relation_name='parametro_file', mode='foreignkey', onDelete='raise')
        tbl.column('parametro', name_long='Parametro')
        tbl.column('header_parametro', name_long='Header Parametro')
        tbl.column('i_low_slice', dtype='I', name_long='Indice minore per slice')
        tbl.column('i_high_slice', dtype='I', name_long='Indice maggiore per slice')
        tbl.column('name_field', name_long='Nome campo')
        tbl.column('dtype', name_long='Tipo campo')
        tbl.column('datapath', name_long='Datapath')
#  intestazione=[('ABI',39,44),('CAB',45,50),('DATA BONIFICO',22,30),('CODICE FISCALE',49,65)]       