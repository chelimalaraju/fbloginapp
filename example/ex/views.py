from django.shortcuts import render
import datetime
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
import urllib
import json
from social.apps.django_app.default.models import *

import urllib2, urllib
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, defaultfilters
from django.http import HttpResponse, Http404
from django.core.cache import cache
 
from django.conf import settings

fql_url = 'https://api.facebook.com/method/fql.query'
cache_expires = getattr(settings, 'CACHE_EXPIRES', 30)

def get_fql_result(fql):
    cachename = 'fbgallery_cache_' + defaultfilters.slugify(fql)
    data = None
    if cache_expires > 0:
        data = cache.get(cachename)
    if data == None:
        options ={
            'query':fql,
            'format':'json',
        }
        f = urllib2.urlopen(urllib2.Request(fql_url, urllib.urlencode(options)))
        response = f.read()
        f.close()
        data = json.loads(response)
        if cache_expires > 0:
            cache.set(cachename, data, cache_expires*60)
    return data
    
def home(request):
    """Home view, displays login mechanism"""
    #https://graph.facebook.com/oauth/authorize?client_id=645661332187773&redirect_uri=http://test1.com:8000&scope=albums,photos
    if request.user.is_authenticated():
        return redirect('/done')
    return render_to_response('home.html', {}, RequestContext(request))


@login_required
def done(request):
    """Login complete view, displays user data"""
    user = User.objects.get(email=request.user.email)
    us = UserSocialAuth.objects.get(user=user)
    fb_id = str(us.uid)
    fql = "select aid, cover_pid, name from album where owner=%s" % fb_id;
    albums = get_fql_result(fql)
    for i in range(len(albums)):
        """ Get the main photo for each Album """
        fql = "select src from photo where pid = '%s'" % albums[i]['cover_pid'];
        for item in get_fql_result(fql):
            albums[i]['src'] = item['src']
    print albums
    return render_to_response('done.html', {'user': request.user,'albums':albums},
                              RequestContext(request))
def logout_view(request):
    logout(request)
    return redirect('/')

