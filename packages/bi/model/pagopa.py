# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('pagopa', pkey='id', name_long='PagoPa', name_plural='PagoPa',caption_field='caption_pagopa')
        self.sysFields(tbl)
        tbl.column('anagrafica_id',size='22', group='_', name_long='Utente'
                    ).relation('bi.anagrafica.id', relation_name='pagopa', mode='foreignkey', onDelete='raise')
        tbl.column('file_id',size='22', group='_', name_long='File origine dati'
                    ).relation('bi.file.id', relation_name='pagopa', mode='foreignkey', onDelete='setnull')
        tbl.column('idpa', name_long='') 
        tbl.column('codice_fiscale', name_long='Codice Fiscale - Piva') 
        tbl.column('id_station', name_long='id_station')
        tbl.column('importo', name_long='importo')
        tbl.column('descrizione', name_long='descrizione')
        tbl.column('nominativo', name_long='nominativo')
        tbl.column('indirizzo', name_long='indirizzo')
        tbl.column('cap', name_long='cap')
        tbl.column('citta', name_long='citta')
        tbl.column('provincia', name_long='provincia')
        tbl.column('iban', name_long='iban')
        tbl.column('id_psp', name_long='id_psp')
        tbl.column('data', name_long='data')
        tbl.column('ente_creditore', name_long='Ente Creditore')
        tbl.column('da_eliminare', dtype='B')
        tbl.formulaColumn('caption_pagopa',"COALESCE($iban,'')||' '||COALESCE($data,'')")

    def trigger_onInserting(self, record=None):
        esiste=self.readColumns(columns='$id',where='$cab=:cab and $abi=:abi and $data_pagamento>=:data and $anagrafica_id=:anagrafica_id',
                            cab=record['cab'],
                            abi=record['abi'],
                            data=record['data_pagamento'],
                            anagrafica_id=record['anagrafica_id'],
                            ignoreMissing=True)   
        record['da_eliminare'] = True if esiste else False  
    def get_dict_flds(self):
        return dict(
                    idPA='idpa',
                    entityUniqueIdentifierValue='codice_fiscale',
                    idStation='id_station',
                    paymentAmount='importo',
                    description='descrizione',
                    fullName='nominativo',
                    streetName='indirizzo',
                    postalCode='cap',
                    city='citta',
                    stateProvinceRegion='provincia',
                    IBAN='iban',
                    idPSP='id_psp',
                    paymentDateTime='data',
                    companyName='ente_creditore',
                    )
"""
<ns2:paSendRTReq xmlns:ns2="http://pagopa-api.pagopa.gov.it/pa/paForNode.xsd">
<idPA>02174950697</idPA>
<idBrokerPA>16215731007</idBrokerPA>
<idStation>16215731007_01</idStation>
<receipt>
<receiptId>c30b24b5a5e9430684afdd8f08c0b695</receiptId>
<noticeNumber>302000000000810908</noticeNumber>
<fiscalCode>02174950697</fiscalCode>
<outcome>OK</outcome>
<creditorReferenceId>02000000000810908</creditorReferenceId>
<paymentAmount>181.66</paymentAmount>
<description>Intimazione ad adempiere VIOL CDS 2012 (D763_22_08087-8889)</description>
<companyName>RISCO SRL</companyName>
<debtor>
<uniqueIdentifier>
<entityUniqueIdentifierType>F</entityUniqueIdentifierType>
<entityUniqueIdentifierValue>LBRNDR74M29G482K</entityUniqueIdentifierValue>
</uniqueIdentifier>
<fullName>LIBERATORE ANDREA</fullName>
<streetName>VIA UMBRIA N 68 INT 10</streetName>
<postalCode>65122</postalCode>
<city>PESCARA</city>
<stateProvinceRegion>PE</stateProvinceRegion>
</debtor>
<transferList>
<transfer>
<idTransfer>1</idTransfer>
<transferAmount>181.66</transferAmount>
<fiscalCodePA>02174950697</fiscalCodePA>
<IBAN>IT94E0760115500001012531156</IBAN>
<remittanceInformation>/RFB/02000000000810908/181.66/TXT/INTIMAZIONE</remittanceInformation>
<transferCategory>9/0102100SA/</transferCategory>
</transfer>
</transferList>
<idPSP>ABI05387</idPSP>
<PSPCompanyName>BPER</PSPCompanyName>
<idChannel>97249640588_01</idChannel>
<channelDescription>NA</channelDescription>
<paymentMethod>other</paymentMethod>
<fee>0.00</fee>
<paymentDateTime>2023-01-02T10:47:47</paymentDateTime>
<applicationDate>2023-01-02</applicationDate>
<transferDate>2023-01-02</transferDate>
</receipt>
</ns2:paSendRTReq>
"""