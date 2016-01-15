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
    services_list = ['xorilog/docker-webhook', 'surycat/wings-appreminder']
    final_services_list = []
    with open(store_file, 'r') as f_in:
        for line in f_in:
            data = json.loads(line)
            store.append(data)
#    for item in store:
#        docker_image=item['repository']['repo_name']
#        version=item['push_data']['tag']
#        print "{ service_name: \"" + str(docker_image).split("/")[1] + "@1\", docker_image: \"" + str(docker_image) + "\", version: \"" + str(version) + "\"}"
    temp_dict = dict()
    for i in xrange(len(store)):
        if store[i]['repository']['repo_name'] not in temp_dict:
            temp_dict[store[i]['repository']['repo_name']]=[]
        if store[i]['push_data']['tag'] not in temp_dict[store[i]['repository']['repo_name']]:
            if version_patern.match(store[i]['push_data']['tag']):
                temp_dict[store[i]['repository']['repo_name']].append(store[i]['push_data']['tag'])
    
    print temp_dict
    print "Listing Max services"
    for service in services_list:
        final_services_list.append([service, max(temp_dict[service])])
    print final_services_list
    print "Surycat configuration for install-machine :"
    for f in final_services_list:
        for item in store:
            if (f[0] in item['repository']['repo_name']) and (f[1] in item['push_data']['tag']) :
                docker_image=item['repository']['repo_name']
                version=item['push_data']['tag']
                print "{ service_name: \"" + str(docker_image).split("/")[1] + "@1\", docker_image: \"" + str(docker_image) + "\", version: \"" + str(version) + "\"}"
#    for item in temp_list:
#        for i in xrange(len(store)):
#            if store[i]
        

if __name__ == "__main__":
    main()
