# Copyright 2015 Sun Jingyun
#
# Python version: 3.4
#
# An SVN post-commit hook for posting to Lesschat. Using it with following steps.
#  
# Step 1:
#       Setup the channel and integration first, then get the url for the new service of SVN.
# Step 2:
#       rename the post-commit.tmpl (under the [svn repository folder]\hooks\) with the new name as it say.
#       add your code to excute the subversion.py with two parameters. $1 for repo and $2 for revision.
#       note: the parameters should be %1 and %2 in windows.
# Step 3: 
#       replace the specail url with the one come from Lesschat.
# Step 4:
#       try to commit something and check your channel.


# POST https://hook.lesschat.com/svn/xxxxxxxxxxxxxxxx
# Content-Type: application/json
# Body: {"payload": {"repo_name": "xxxx", "author": "xxxx", "log": "xxxx", "rev": "xxxx"}}

import sys
import os
import urllib
import urllib.parse
import urllib.request
import json

def get_content(repo, rev):
        repo_name = get_repo_name(repo)
        author = get_author(repo_name, rev)
        log = get_log(repo_name, rev)
        content = {'repo_name': repo_name, 'author': author, 'log': log, 'rev': rev}
        return content
def get_repo_name(repo):
        return os.path.basename(repo)
def get_author(repo_name, rev):
        cmd = '%s author -r %s %s' % (svnlook_bin_path, rev, repo_name)
        output = os.popen(cmd).read()
        return output
def get_log(repo_name, rev):
        cmd = '%s log -r %s %s' % (svnlook_bin_path, rev, repo_name)
        output = os.popen(cmd).read()
        return output
def post(content):
        url = "https://hook.lesschat.com/svn/xxxxxxxxxxxxxxxx"
        data = {'payload': content}
        data = json.dumps(data).encode(encoding='UTF8')
        
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data, headers)
        res_data = urllib.request.urlopen(req)
        res = res_data.read()
        return
    
global svnlook_bin_path
# svnlook_bin_path is the path of svnlook, usually you can can find it under the subversion\bin.
svnlook_bin_path = 'xxxxx\subversion\bin\svnlook' 
# switch the work path to the parent path of the repository
# for example, your repository path is \usr\bin\myrepository, then switch to the path of \usr\bin
os.chdir("xxxxxxxxxxxxx")

content = get_content(sys.argv[1], sys.argv[2])
post(content)

