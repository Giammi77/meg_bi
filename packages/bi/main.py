#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='bi package',sqlschema='bi',sqlprefix=True,
                    name_short='Bi', name_long='Business Intelligence', name_full='Bi')
                    
    def config_db(self, pkg):
        pass
        
class Table(GnrDboTable):
    pass
