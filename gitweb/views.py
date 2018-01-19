# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import os

from django.conf import settings
from django.shortcuts import render
from django.http import Http404

from .utils import human_filesize, pygmentize
from .models import Repository
# Create your views here.

def repository_list(request):
    repository_list = Repository.objects.visible_repositories_for_user(request.user)
    return render(request, 'repository_list.html', locals())

def repository_summary(request, slug):
    try:
        repository = Repository.objects.visible_repositories_for_user(request.user).get(slug=slug)
    except Repository.DoesNotExist:
        raise Http404

    clone_url = settings.GIT_CLONE_URL % os.path.split(repository.path)[1]
    return render(request, 'repository_summary.html', locals())

def repository_log(request, slug, branch=None):
    try:
        repository = Repository.objects.visible_repositories_for_user(request.user).get(slug=slug)
    except Repository.Repository.DoesNotExist:
        raise Http404

    # if branch == None:
    #     logs = repository.logs()
    #     branch = "All"
    # else:
    #     logs = repository.logs(branch)
    if branch == None:
        logs = repository.gitt().log()
        branch = "All"
    else:
        logs = repository.gitt().log(branch)          #type(logs), logs is a unicode str

    # logs = logs.replace('\n', '\"</br>\"')
    # logs = logs.encode('utf8')
    return render(request, 'repository_log.html', locals())

def repository_tree(request, slug, branch, path):
    try:
        repository = Repository.objects.visible_repositories_for_user(request.user).get(slug=slug)
    except Repository.DoesNotExist:
        raise Http404

    tree = repository.repo().tree(branch)

    for element in path.split('/'):
        element = element.encode('utf8')
        if len(element):
            tree = tree / element

    if hasattr(tree, 'mime_type'):
        is_blob = True
    else:
        is_blob = False
        tree = [{'path': os.path.join(path, e.name), 'e': e, 'human_size': human_filesize(getattr(e, 'size', 0))} for e in tree.trees + tree.blobs]
        # tree = [{'path': os.path.join(path, e.name), 'e': e, 'human_size': human_filesize(getattr(e, 'size', 0))} for e in tree.values()]

    path = os.path.join('/', path)
    prev_path = '/'.join(path.split('/')[0:-1])

    if is_blob:
        blob_human_size = human_filesize(tree.size)
        blob_lines = range(len(tree.data_stream.read().splitlines()))
        blob_pygmentized = pygmentize(tree.mime_type, tree.data_stream.read())

    return render(request, 'repository_tree.html', locals())


def repository_commit(request, slug, commit, template_name='repository_commit.html'):
    try:
        repository = Repository.objects.visible_repositories_for_user(request.user).get(slug=slug)
    except Repository.DoesNotExist:
        raise Http404

    try:
        commit = repository.repo().commit(commit)
    except:
        raise Http404

    NEWEST_commit = repository.repo().commit()
    diffs = repository.repo().git.diff(commit, NEWEST_commit)   # or diffs = repository.repo().git.diff(commit)
    parents = commit.parents
    # diffs = repository.repo().git.diff(commit, commit.parents)
    return render(request, template_name, locals())