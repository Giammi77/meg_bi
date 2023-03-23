# encoding: utf-8
from giammi import scriviDebug

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bene_mobile', pkey='id', name_long='Bene Mobile', name_plural='Beni Mobili',caption_field='targa')
        self.sysFields(tbl,user_upd=True)

        tbl.column('anagrafica_id', size='22', group='_', name_long='Codice Fiscale - Piva'
                    ).relation('bi.anagrafica.id', relation_name='bene_mobile', mode='foreignkey', onDelete_sql='cascade')
        
        tbl.column('marca', size=':50', name_long='Marca')
        tbl.column('modello', size=':50', name_long='Modello')
        tbl.column('targa', size=':15', name_long='Targa')
        tbl.column('data_immatricolazione', dtype='D', name_long='Data Immatricolazione')
        tbl.column('altro_fermo_attore', size=':30', name_long='Altro Fermo da')
        tbl.column('altro_fermo_importo', dtype='N', name_long='Altro Fermo importo')

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
            nome_file_elaborazione='beni_mobili.csv'
            sn = self.db.application.site.storageNode('site:esportazioni',nome_file_elaborazione)
            scriviDebug(self,dati=rows,sn=sn)
        return esportati,sn