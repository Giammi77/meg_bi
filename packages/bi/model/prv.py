# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('prv', pkey='id', name_long='prv')
        tbl.column('campo_a', dtype='N')
        tbl.column('campo_b')