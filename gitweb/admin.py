# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Member, Repository
from .forms import RepositoryForm

# Register your models here.



class MemberInline(admin.TabularInline):
    model = Member
    extra = 2


class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_public', 'path')
    save_on_top = True
    form = RepositoryForm
    inlines = (MemberInline,)

    def changelist_view(self, request):
        sync_result = Repository.objects.sync_with_fs()
        return super(RepositoryAdmin, self).changelist_view(request, {'sync_result': sync_result})


admin.site.register(Repository, RepositoryAdmin)