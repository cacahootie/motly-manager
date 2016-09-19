
import mimetypes
import os
from StringIO import StringIO
from zipfile import ZipFile

import boto
from boto.s3.key import Key
import requests

from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.core.exceptions import PermissionDenied


cfg_url = os.environ['CFG_URL']
cfg = requests.get(cfg_url).json()


def process_filename(staticbase, pname, fname):
    return (
        fname,
        '{}/{}'.format(pname, fname.replace(staticbase, ''))
    )


def upload_file(fname, value):
    conn = boto.connect_s3(
        cfg['AWS_ACCESS_KEY_ID'], cfg['AWS_SECRET_ACCESS_KEY']
    )
    k = Key(conn.get_bucket('ldsn-static'))
    k.key = 'motly-static/{}'.format(fname)
    content_type = mimetypes.guess_type(fname)[0]
    k.set_metadata('Content-Type', content_type)
    k.set_contents_from_string(value)
    print "Uploaded {} to s3 with mimetype {}".format(k.key, content_type)


def deploy(request):
    try:
        token = request.GET['token']
        if os.environ['AUTH_TOKEN'] != token:
            raise PermissionDenied
    except KeyError:
        raise PermissionDenied
    try:
        gh_user = request.GET['gh_user']
        gh_repo = request.GET['gh_repo']
        tag = request.GET['tag']
    except KeyError:
        return HttpResponseBadRequest(
            "Either gh_user or gh_repo is not supplied or invalid"
        )
    release_url = "https://github.com/{gh_user}/{gh_repo}/archive/{tag}.zip"\
        .format(
            **locals()
        )
    print "Fetching {}".format(release_url)
    zipdata = requests.get(
        release_url,
        stream=True
    ).content
    z = ZipFile(StringIO(zipdata))
    filelist = z.namelist()
    base = filelist[0]
    staticbase = base + 'static/'
    staticfiles = [
        process_filename(staticbase, gh_repo, x) for x in filelist
        if x.startswith(staticbase) and x != staticbase
    ]
    for x in staticfiles:
        upload_file(x[1], z.read(x[0]))
    return JsonResponse({
        'files': filelist,
        'static_files': staticfiles
    })
