# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        meg_bi = root.branch(u"Meg Bi")
        meg_bi.thpage(u"!!Anagrafiche", table="bi.anagrafica", viewResource='ViewBase')
        meg_bi.thpage(u"!!Locazioni", table="bi.locazione")
        meg_bi.thpage(u"!!Bonifici", table="bi.bonifico")
        meg_bi.thpage(u"!!F24", table="bi.f24")