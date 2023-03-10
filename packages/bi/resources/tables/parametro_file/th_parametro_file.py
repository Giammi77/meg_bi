#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('tipo_file_id')
        r.fieldcell('parametro',width='25em')
        r.fieldcell('i_low_slice',width='3em')
        r.fieldcell('i_high_slice',width='3em')

    def th_order(self):
        return 'tipo_file_id'

    def th_query(self):
        return dict(column='tipo_file_id', op='contains', val='')

class ViewFromTipoFile(View):
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('parametro',edit=True)
        r.fieldcell('i_low_slice',edit=True)
        r.fieldcell('i_high_slice',edit=True)
        r.fieldcell('name_field',edit=True)


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('tipo_file_id')
        fb.field('parametro')
        fb.field('i_low_slice')
        fb.field('i_high_slice')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
