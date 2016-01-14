#!/bin/bash
for arg in "$@"
do
    case $arg in
        "--repo_name" )
           repo_name=$arg;;
        "--tag" )
           tag=$arg;;
        "--push_date" )
           push_date=$arg;;
   esac
done
short_name=$(echo "${repo_name}"|cut -d '/' -f 2)
echo '{ service_name: "nginx@1", docker_image: "surycat/nginx", version: "0.2.0" }'
line="{ service_name: "\"${short_name}\""@1, docker_image: "\"${repo_name}\"", version: "\"${tag}\""}, "
echo ${line} >> ansible-line.store
