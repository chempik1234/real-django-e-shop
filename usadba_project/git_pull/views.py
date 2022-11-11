from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git


@csrf_exempt
def github_update_pythonanywhere(request):
    if request.method == 'POST':
        repo = git.Repo('./', search_parent_directories=True)
        _git = repo.git
        _git.checkout('master')
        _git.pull()
        return HttpResponse('pulled_success')
    else:
        return HttpResponse('get_request', status=400)