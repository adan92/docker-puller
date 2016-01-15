#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, ast
from pprint import pprint

'''
{ service_name: "webhook-tester-repo@1", docker_image: "biscarch/webhook-tester-repo", version: "toto"}

{"push_data": {"pushed_at": 1449017033, "images": [], "tag": "toto", "pusher": "biscarch"}, "callback_url": "https://registry.hub.docker.com/u/biscarch/webhook-tester-repo/hook/2i5e3gj1bi354asb3f05gchi4ccjg0gas/", "repository": {"status": "Active", "repo_name": "biscarch/webhook-tester-repo", "description": "", "namespace": "biscarch", "is_trusted": false, "full_description": null, "comment_count": 0, "star_count": 0, "repo_url": "https://registry.hub.docker.com/u/biscarch/webhook-tester-repo/", "owner": "biscarch", "date_created": 1449016916, "is_official": false, "is_private": false, "name": "webhook-tester-repo"}}
'''
store = []
def main():
    store_file="logs/testing.log"
    with open(store_file, 'r') as f_in:
        for line in f_in:
            data = json.loads(line)
            store.append(data)
    for item in store:
        docker_image=item['repository']['repo_name']
        version=item['push_data']['tag']
        print "{ service_name: \"" + str(docker_image).split("/")[1] + "@1\", docker_image: \"" + str(docker_image) + "\", version: \"" + str(version) + "\"}"
        

if __name__ == "__main__":
    main()
