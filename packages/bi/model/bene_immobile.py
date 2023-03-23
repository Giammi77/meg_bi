# encoding: utf-8
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from giammi import scriviDebug

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bene_immobile', pkey='id', name_long='Bene Immobile', name_plural='Beni Immobili',caption_field='loc_cf')
        self.sysFields(tbl,user_upd=True)
        tbl.column('anagrafica_id', size='22', group='_', name_long='Codice Fiscale - Piva'
                    ).relation('bi.anagrafica.id', relation_name='bene_immobile', mode='foreignkey', onDelete_sql='cascade')
        tbl.column('catasto', size=':20', name_long='catasto')
        tbl.column('fg', size=':10', name_long='Foglio')
        tbl.column('num', size=':10', name_long='Num')
        tbl.column('sub', size=':10', name_long='Sub')
        tbl.column('categoria', size=':15', name_long='Categoria')
        tbl.column('ubicazione', size=':100', name_long='Ubicazione')
        tbl.column('data_siatel', dtype='D', name_long='Data Siatel')
        tbl.column('note', name_long='Note')
        tbl.column('loc_nome', name_long='Locatario')
        tbl.column('loc_indirizzo', name_long='Indirizzo')
        tbl.column('loc_cap', size=':5', name_long='CAP')
        tbl.column('loc_comune', name_long='Comune')
        tbl.column('loc_pr', size='2', name_long='Pr')
        tbl.column('loc_cf',  size=':16', name_long='CF')
        tbl.column('loc_anno', name_long='Anno')
        tbl.column('loc_uff_terr', name_long='Uff. territoriale')
        tbl.column('loc_num', name_long='Num contratto')
        tbl.column('loc_data', dtype='D', name_long='Data Contratto')
        tbl.column('loc_volume', name_long='Num volume')
        tbl.column('loc_email', name_long='pec')        

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
            nome_file_elaborazione='beni_immobili.csv'
            sn = self.db.application.site.storageNode('site:esportazioni',nome_file_elaborazione)
            scriviDebug(self,dati=rows,sn=sn)
        return esportati,sn