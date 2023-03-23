# encoding: utf-8
from gnr.core.gnrdecorator import public_method  
from giammi import scriviDebug
import json

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('banca_filiale', pkey='id', name_long='Filiale', name_plural='Filiali',caption_field='filiale')
        self.sysFields(tbl)
        tbl.column('banca_istituto_id',size='22', name_long='Istituto',
                    ).relation('bi.banca_istituto.id', relation_name='banca_filiale', mode='foreignkey', onDelete='cascade')
        tbl.column('cab', name_long='CAB') 
        tbl.column('indirizzo', name_long='Indirizzo')
        tbl.column('sportello', name_long='Sportello')
        tbl.column('citta', name_long='Citta')
        tbl.column('prov', name_long='Provincia')
        tbl.column('cap', name_long='Cap')
        tbl.column('p_iva', name_long='P.Iva')
        tbl.column('mail', name_long='Mail')
        tbl.column('pec', name_long='Pec')
        
        tbl.aliasColumn('istituto', '@banca_istituto_id.istituto', name_long='Istituto')
        tbl.formulaColumn('filiale',"COALESCE($istituto,'')||' '||COALESCE($indirizzo,'')", name_long='Filiale')

        #nome istituto - filiale - indirizzo filiale
        #aliasCol        istituto @banca_istituto.istituto
        #filliale formulaCol istituto || - Filiale -|| indirizzo 
