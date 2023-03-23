# encoding: utf-8
from giammi import scriviDebug

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('datore_lavoro', pkey='id', name_long='Datore Lavoro', name_plural='Datori Lavoro',caption_field='datore')
        self.sysFields(tbl,user_upd=True)

        tbl.column('anagrafica_id', size='22', group='_', name_long='Codice Fiscale - Piva'
                    ).relation('bi.anagrafica.id', relation_name='datore_lavoro', mode='foreignkey', onDelete_sql='cascade')
        tbl.column('data_siatel', dtype='D', name_long='Data Siatel')
        tbl.column('datore', size=':100', name_long='Datore di Lavoro')
        tbl.column('ind', size=':100', name_long='Indirizzo')
        tbl.column('cap', size='5', name_long='CAP')
        tbl.column('comune', name_long='Comune')
        tbl.column('pr', size='2', name_long='Provincia')
        tbl.column('p_iva', size=':16', name6long='Part.IVA')
        tbl.column('email', size=':150', name_long='e-mail')
        tbl.column('pec', size=':50', name_long='PEC')

    def esporta_beni(self,btc=None,anagrafica_ids=None):
        esportati=0
        if not anagrafica_ids:
            return esportati,None
        rec=self.query(where='$anagrafica_id in :anagrafica_ids',anagrafica_ids=anagrafica_ids).fetch()
        if len(rec)==0:
            return esportati,None
        rows=[''.join(f'{k};' for k in rec[0].keys())[:-1]]
        for r in btc.thermo_wrapper(rec,message='Elaborazione'):
            row=''
            for k,v in r.items():
                if v is None:
                    v=''
                row+=f'{v};'
            rows.append(row)
            esportati+=1
        if len(rows)>0:
            nome_file_elaborazione='datori_lavoro.csv'
            sn = self.db.application.site.storageNode('site:esportazioni',nome_file_elaborazione)
            scriviDebug(self,dati=rows,sn=sn)
        return esportati,sn
    