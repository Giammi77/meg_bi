# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        develop = root.branch(u"Develop", tags="admin")
        develop.packageBranch("System", pkg='sys', tags="admin")
        develop.packageBranch("admin", pkg='adm', tags="admin")
        develop.packageBranch("Glbl", pkg='glbl', tags="admin")
        develop.packageBranch("Test", pkg='test', tags="admin")
        meg_bi = root.branch(u"Meg Bi")
        meg_bi.thpage(u"!!File Importati", table="bi.file")
        meg_bi.thpage(u"!!Anagrafiche", table="bi.anagrafica", viewResource='ViewBase')
        meg_bi.thpage(u"!!Locazioni", table="bi.locazione")
        meg_bi.thpage(u"!!Bonifici", table="bi.bonifico")
        meg_bi.thpage(u"!!F24", table="bi.f24")
        config = root.branch(u"Configurazioni", tags="admin")  
        config.thpage(u"!!Parametri file", table="bi.parametro_file")
        config.thpage(u"!!Tipi file", table="bi.tipo_file")
        config.thpage(u"!!Istituti Bancari", table="bi.banca")