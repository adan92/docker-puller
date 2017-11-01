#!/usr/bin/python
# -*- coding: utf-8 -*-
import json, re

'''
{ service_name: "webhook-tester-repo@1", docker_image: "biscarch/webhook-tester-repo", version: "toto"}

{"push_data": {"pushed_at": 1449017033, "images": [], "tag": "toto", "pusher": "biscarch"}, "callback_url": "https://registry.hub.docker.com/u/biscarch/webhook-tester-repo/hook/2i5e3gj1bi354asb3f05gchi4ccjg0gas/", "repository": {"status": "Active", "repo_name": "biscarch/webhook-tester-repo", "description": "", "namespace": "biscarch", "is_trusted": false, "full_description": null, "comment_count": 0, "star_count": 0, "repo_url": "https://registry.hub.docker.com/u/biscarch/webhook-tester-repo/", "owner": "biscarch", "date_created": 1449016916, "is_official": false, "is_private": false, "name": "webhook-tester-repo"}}
'''
store = []
def main():
    store_file="logs/testing.log"
    version_patern = re.compile("^\d+\.\d+\.\d+$")
    services_list = ['xorilog/docker-webhook', 'surycat/nginx', 'surycat/ldap', 'surycat/prosody', 'surycat/wings', 'surycat/wings-appreminder', 'surycat/nyuki-idshost', 'surycat/nyuki-appreminder', 'surycat/nyuki-dashboard', 'surycat/nyuki-hlseven', 'surycat/nyuki-infobip', 'surycat/nyuki-smtp', 'surycat/nyuki-thecallr', 'surycat/nyuki-swagger', 'surycat/nyuki-auth', 'surycat/wings-auth', 'surycat/wings-idshost', 'surycat/wings-users']

    final_services_list = []
    with open(store_file, 'r') as f_in:
        for line in f_in:
            data = json.loads(line)
            store.append(data)
    temp_dict = dict()
    for i in xrange(len(store)):
        if version_patern.match(store[i]['push_data']['tag']):
            if store[i]['repository']['repo_name'] not in temp_dict:
                temp_dict[store[i]['repository']['repo_name']]=[]
            if store[i]['push_data']['tag'] not in temp_dict[store[i]['repository']['repo_name']]:
                temp_dict[store[i]['repository']['repo_name']].append(store[i]['push_data']['tag'])
    
#    print temp_dict
#    print "Listing Max services"
    for service in services_list:
        if service in temp_dict:
            final_services_list.append([service, max(temp_dict[service])])
#    print final_services_list
    print "Surycat configuration for install-machine :"
    for f in final_services_list:
        docker_image=f[0]
        version=f[1]
        print "{ service_name: \"" + str(docker_image).split("/")[1] + "@1\", docker_image: \"" + str(docker_image) + "\", version: \"" + str(version) + "\"}"

if __name__ == "__main__":
    main()
