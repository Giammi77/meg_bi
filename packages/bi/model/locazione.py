# encoding: utf-8


class Table(object):
    def config_db(self, pkg):
        tbl =  pkg.table('locazione',name_long='Locazione',name_plural='Locazioni', pkey='id', caption_field='caption_locazione')
        self.sysFields(tbl,user_upd=True)

        tbl.column('anagrafica_id',size='22', group='_', name_long='Contribuente'
                    ).relation('bi.anagrafica.id', relation_name='locazione', mode='foreignkey', onDelete='raise')
        tbl.column('file_id',size='22', group='_', name_long='File origine dati'
                    ).relation('bi.file.id', relation_name='locazione', mode='foreignkey', onDelete='setnull')
        tbl.column('codice',name_long='codice',legacy_name='code')
        tbl.column('regcontr',dtype='D',name_long='regcontr',legacy_name='regcontr')
        tbl.column('ufficio',name_long='ufficio',legacy_name='ufficio')
        tbl.column('serie',name_long='serie',legacy_name='serie')
        tbl.column('numero',name_long='numero',legacy_name='numero')
        tbl.column('tipologia',name_long='tipologia',legacy_name='tipologia')
        tbl.column('durata_dal',dtype='D',name_long='durata_dal',legacy_name='durata_dal')
        tbl.column('durata_al',dtype='D',name_long='durata_al',legacy_name='durata_al')
        tbl.column('data_stipula',dtype='D',name_long='data_stipula',legacy_name='data_stipula')
        tbl.column('importo_canone',dtype='N',name_long='importo_canone',legacy_name='importo_canone')
        tbl.column('d_a',name_long='d_a',legacy_name='d_a')
        tbl.column('identificativo_soggetto',name_long='identificativo_soggetto',legacy_name='identificativo_soggetto')
        tbl.column('inizio_rapporto',dtype='D',name_long='inizio_rapporto',legacy_name='inizio_rapporto')
        tbl.column('fine_rapporto',dtype='D',name_long='fine_rapporto',legacy_name='fine_rapporto')
        tbl.column('codice_comune',name_long='codice_comune',legacy_name='codice_comune')
        tbl.column('t_u',name_long='t_u',legacy_name='t_u')
        tbl.column('i_p',name_long='i_p',legacy_name='i_p')
        tbl.column('sezione_urbana',name_long='sezione_urbana',legacy_name='sezione_urbana')
        tbl.column('foglio',name_long='foglio',legacy_name='foglio')
        tbl.column('particella',name_long='particella',legacy_name='particella')
        tbl.column('sub',name_long='sub',legacy_name='sub')
        tbl.column('da_eliminare', dtype='B')
        tbl.formulaColumn('caption_locazione',"COALESCE($foglio,'')||' '||COALESCE($foglio,'')||' '||COALESCE($foglio,'')")

    # def trigger_onInserting(self, record=None):
    #     esiste=self.readColumns(columns='$id',where='$cab=:cab and $abi=:abi and $data>=:data and $anagrafica_id=:anagrafica_id',
    #                         cab=record['cab'],
    #                         abi=record['abi'],
    #                         data=record['data'],
    #                         anagrafica_id=record['anagrafica_id'],
    #                         ignoreMissing=True)   
    #     record['da_eliminare'] = True if esiste else False  