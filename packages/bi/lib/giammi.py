from gnr.core.gnrlang import GnrException
from PyPDF2 import PdfFileReader, PdfFileWriter
from decimal import Decimal
from datetime import datetime, date
import os,zipfile
import ftplib
try:
    import openpyxl
    from gnr.core.gnrxls import XlsxWriter as ExcelWriter
except:
    from gnr.core.gnrxls import XlsWriter as ExcelWriter

def genera_file_csv(dati=None,tipoDecimale=None,separatoreCsv=None,**writerPars):
    # writerPars = dict(columns=fields, coltypes=coltypes, headers=headers, filepath=xls_pagoPa_node) 
    headers = writerPars.get('headers')
    filepath = writerPars.get('filepath')
    lenHeaders = len(headers)
    n=1

    with filepath.open(mode='w') as f:
        for h in headers:
            if n<lenHeaders:
                f.write('%s%s'%(h,separatoreCsv))
            else:
                f.write('%s'%(h))
            n+=1
        f.write('\n')
        
        for row in dati:
            n=1
            for k,v in row.items():
                if v==None:
                    v=''
                chkDecimal=isinstance(v,Decimal)
                chkDate=isinstance(v,date)
                if chkDecimal :
                    v=str(round(v,2))
                    if tipoDecimale==',':
                        v=v.replace('.',',') 
                elif chkDate:
                    v=str(v)
                else:
                    v=str(v)
                    v=v.replace(',',' ')         
                if n<lenHeaders:
                    f.write('%s%s'%(v,separatoreCsv))
                else:
                    f.write('%s'%(v))
                n+=1
            f.write('\n')

def genera_file_xls(dati=None,**writerPars):
    writer = ExcelWriter(**writerPars)
    writer.writeHeaders()
    for row in dati:
        writer.writeRow(row)
    writer.workbookSave()

def getColtypes(tbl=None, fields=None):
    # RESITUISCE IL TIPO DI CAMPO IMPORTATO NEL MODEL
    coltypes = {}
    for f in fields:
        try:
            coltypes[f] = tbl.getAttr('dtype')
        except:
            coltypes[f] = 'T'
    return coltypes

def scriviDebug(self,dati=None,sn=None):
    if sn:
        filepath=sn
    else:
        filepath=self.db.application.site.storageNode('site:debug.csv')
    with filepath.open(mode='w') as f:
        for dato in dati:
            f.write(str(dato)+'\n')

def connectFtp(self):
    FTP_HOST = self.db.application.getPreference('ftp_host',pkg='rcweb')
    FTP_USER = self.db.application.getPreference('ftp_user',pkg='rcweb')
    FTP_PASS = self.db.application.getPreference('ftp_pass',pkg='rcweb')

    try:
        ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
        return ftp
    except: 
        raise GnrException("Errore di connessione FTP")

def inviaFileFtp(self,filePath=None,destFolder=None, prefisso=None, replace_baseName=None):
    ftp = connectFtp(self)
    chktest = self.db.application.getPreference('chktest',pkg='rcweb')
    if chktest:
        destFolder='/TEST/'
    else:
        destFolder='/IN/'
    try:
        if replace_baseName==True:
            baseName = os.path.basename(filePath).replace('_','-')
        else:
            baseName = os.path.basename(filePath)
        ftp.cwd(destFolder) #/PROVA/        
        with open(filePath, "rb") as file:
            # use FTP's STOR command to upload the file
            if prefisso:
                ftp.storbinary(f"STOR {prefisso}{baseName}", file)
            else:
                ftp.storbinary(f"STOR {baseName}", file)
        ftp.quit()
    except:
        raise GnrException("Errore nell'invio FTP")


def recuperaFileFtp(self, sourceDirectory=None, sn=None, filename=None):
    ftp = connectFtp(self)
    
    try:
        ftp.cwd(sourceDirectory)
        with sn.open(mode='wb') as file:
            ftp.retrbinary(f"RETR {filename}", file.write)
        ftp.quit()
    except:
        raise GnrException("Errore nel recupero file FTP")

def is_file(ftp,filename):
    current = ftp.pwd()
    try:
        ftp.cwd(filename)
    except:
        ftp.cwd(current)
        return True
    ftp.cwd(current)
    return False

def listaFilesFtp(self, sourceDirectory=None):
    files=[]
    ftp = connectFtp(self)
    try:
        ftp.cwd(sourceDirectory)
        data = ftp.nlst()
        for d in data:
            files.append(d) if is_file(ftp,d) else None 
        ftp.quit()
        return files
    except:
        raise GnrException("Errore nel recupero lista file FTP")

def spostaFileFtp(self,filename=None,sourceDirectory=None,destDirectory=None):
    ftp = connectFtp(self)
    try:
        ftp.cwd(sourceDirectory)
        # ftp.rename(filename,'/TEST/BACKUP/'+ filename)
        ftp.rename(filename,destDirectory+filename)
        ftp.quit()
    except:
        raise GnrException("Errore nello spostamento file FTP")

def readPdf(filePdf):
    # file=open('Avvisi.pdf','rb')
    file = open(filePdf,'rb')
    reader = PdfFileReader(file)
    page0 = reader.getPage(0)
    #print(reader.numPages)
    pdfData = page0.extractText()
    #print(pdfData)
    file.close()

def splitPdf(path, name_of_split):
    '''
    path = 'Avvisi.pdf'
    splitPdf(path, 'Pag_')
    '''
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        output = f'{name_of_split}{page+1}.pdf'
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)

def merge_pdfs(paths, snMergePdf):
    '''
    nomePdf = 'merge.pdf'
    paths=[]
    for n in newPages:
        paths.append('Pag_%s.pdf'%(str(n)))
    merge_pdfs(paths, output=nomePdf)
    '''
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(snMergePdf.local_path(mode='r'), 'wb') as out:
        pdf_writer.write(out)

def contaPagPdf(sn=None):
    if not sn:
        return False
    else:
        with sn.open(mode='rb') as pdf:
            reader = PdfFileReader(pdf)
            return reader.numPages

def pdfToPdfa(token,input_path,output_path):
  
    import sys
    import convertapi
    import datetime as date
    try:
        convertapi.api_secret = token
        convertapi.convert('pdfa', {'File': input_path},
                            from_format = 'pdf').save_files(output_path)
    except:
        raise GnrException("Errore Conversione Pdf/PdfA")
        # return False

# funzione ricorsiva
def NumberToTextInteger(n):
    if n == 0: 
        return ""
        
    elif n <= 19:
        return ("uno", "due", "tre", "quattro", "cinque", 
                "sei", "sette", "otto", "nove", "dieci", 
                "undici", "dodici", "tredici", 
                "quattordici", "quindici", "sedici", 
                "diciassette", "diciotto", "diciannove")[n-1]
                
    elif n <= 99:
        decine = ("venti", "trenta", "quaranta",
                "cinquanta", "sessanta", 
                "settanta", "ottanta", "novanta")
        letter = decine[int(n/10)-2]
        t = n%10
        if t == 1 or t == 8:
            letter = letter[:-1]
        return letter + NumberToTextInteger(n%10)
        
    elif n <= 199:
        return "cento" + NumberToTextInteger(n%100)
        
    elif n <= 999:
        m = n%100
        m = int(m/10)
        letter = "cent"
        if m != 8:
            letter = letter + "o"
        return NumberToTextInteger( int(n/100)) + \
            letter + \
            NumberToTextInteger(n%100)
        
    elif n<= 1999 :
        return "mille" + NumberToTextInteger(n%1000)
    
    elif n<= 999999:
        return NumberToTextInteger(int(n/1000)) + \
            "mila" + \
            NumberToTextInteger(n%1000)
        
    elif n <= 1999999:
        return "unmilione" + NumberToTextInteger(n%1000000)
        
    elif n <= 999999999:
        return NumberToTextInteger(int(n/1000000))+ \
            "milioni" + \
            NumberToTextInteger(n%1000000)
    elif n <= 1999999999:
        return "unmiliardo" + NumberToTextInteger(n%1000000000)
        
    else:
        return NumberToTextInteger(int(n/1000000000)) + \
            "miliardi" + \
            NumberToTextInteger(n%1000000000)

# funzione wrapper
def NumberToText(x, pos=2):
    """ Ritorna un numero tradotto in lettere
        secondo un formato 'finanziario'
    """
    sign = ""
    if x<0:
        sign = "meno"
        x = abs(x)
    x = round(x, pos)
    n = int(x)
    frmt = "{0:0."+"{0:d}".format(pos)+"f}"
    spic = frmt.format(x-n)[2:]
    if n == 0:
        num = "zero"
    else:
        num = NumberToTextInteger(n)
    return sign+num+"/"+spic

def _unzip(path=None, folder=None, file_name=None):
    file_zip = zipfile.ZipFile(file_name)                                    
    file_zip.extractall(folder)
    file_zip.close()
    
def unzip(sn_folder=None, sn_file=None):
    with sn_file.open(mode='rb') as file:
        file_zip = zipfile.ZipFile(file)                                    
        file_zip.extractall(sn_folder.internal_path)  

def getDictFromSnCsv(sn_csv, sep=';'):
    keys=[]
    rows=[]
    with sn_csv.open(mode='r') as myfile:
            lines=myfile.readlines()
            for n , l in enumerate(lines,0):
                if n==0:
                    keys=l.split(sep)                      
                else:
                    values=l.split(sep)                    
                    row={}
                    for nn,v in enumerate(values,0):
                        v = v.replace('\n','')
                        if v == '':
                            v=None
                        row[keys[nn].replace('\n','')]=v
                    rows.append(row)      
    return rows

def dateFromStrig(date_str=None, pattern='%d/%m/%Y'):
    '18/10/1977'
    dt = date_str[:10]
    return datetime.strptime(dt, pattern).date()

def getAbiCab_fromIban(iban):
    if not iban:
        return None,None
    abi= iban[5:10]
    cab= iban[10:15]
    return abi,cab