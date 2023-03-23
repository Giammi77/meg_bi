# encoding: utf-8
from gnr.core.gnrdecorator import public_method  # rendere un metodo "chiamabile" dalla TH
from gnr.core.gnrlist import getReader  # per Excel
from gnr.core.gnrlang import GnrException
from datetime import date
from gnr.core.gnrbag import Bag  # una Bag non si nega a nessuno
from giammi import scriviDebug

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('conto_corrente', pkey='id', name_long='Conto Corrente', name_plural='Conti Corrente',caption_field='istituto')
        self.sysFields(tbl,user_upd=True)

        tbl.column('anagrafica_id', size='22', group='_', name_long='Codice Fiscale - Piva'
                    ).relation('bi.anagrafica.id', relation_name='conto_corrente', mode='foreignkey', onDelete_sql='cascade')
        tbl.column('banca_istituto_id',size='22', group='_', name_long='Istituto Bancario'
                    ).relation('bi.banca_istituto.id', relation_name='conto_corrente', mode='foreignkey', onDelete='raise')
        tbl.column('banca_filiale_id',size='22', group='_', name_long='Filiale'
                    ).relation('bi.banca_filiale.id', relation_name='conto_corrente', mode='foreignkey', onDelete='raise')
        tbl.column('file_id',size='22', group='_', name_long='File origine dati'
                    ).relation('bi.file.id', relation_name='conto_corrente', mode='foreignkey', onDelete='setnull')
        
        tbl.aliasColumn('istituto', '@banca_istituto_id.istituto',static=True)
        tbl.aliasColumn('cab', '@banca_filiale_id.cab',static=True)
        tbl.aliasColumn('indirizzo', '@banca_filiale_id.indirizzo',static=True)
        tbl.aliasColumn('sportello', '@banca_filiale_id.sportello',static=True)
        tbl.aliasColumn('citta', '@banca_filiale_id.citta',static=True)
        tbl.aliasColumn('prov', '@banca_filiale_id.prov',static=True)
        tbl.aliasColumn('cap', '@banca_filiale_id.cap',static=True)
        tbl.aliasColumn('p_iva', '@banca_filiale_id.p_iva',static=True)
        tbl.aliasColumn('mail', '@banca_filiale_id.mail',static=True)
        tbl.aliasColumn('pec', '@banca_filiale_id.pec',static=True)

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
            nome_file_elaborazione='conti_correnti.csv'
            sn = self.db.application.site.storageNode('site:esportazioni',nome_file_elaborazione)
            scriviDebug(self,dati=rows,sn=sn)
        return esportati,sn
