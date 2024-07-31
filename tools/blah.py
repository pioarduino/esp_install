#!/usr/bin/python

import json
import requests
import hashlib


tool_file = "tools.json"
#out_tool_file = "esp_install/tools/tools_out.json"
tool_src_file = "tools_source.json"

def load_data():
    f = open(tool_file)
    data = json.load(f)
    f.close()
    f = open(tool_src_file)
    pkg = json.load(f)
    f.close()
    return data, pkg

def rehash_pkg(url):
    m = hashlib.sha256()
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            print("bad response!")
            return False, 0, 0

        total =  int(r.headers['content-length'])
        for i in r.iter_content():
            m.update(i)
        return True, total, m.hexdigest()


def update_tool_manifest(dict, name, platform, url, size, hash):
    for tool in dict["tools"]:
        if tool["name"] != name:
            continue

        print("Updating pkg:", name)
        d = tool["versions"][0][platform] = {}
        tool["versions"][0][platform]["url"] = url
        tool["versions"][0][platform]["size"] = size
        tool["versions"][0][platform]["sha256"] = hash




tool_data = None # loaded from tools.json
tool_pkg  = None # loaded from tools_source.json

tool_data, tool_pkg = load_data()

for pkg, pkg_data in tool_pkg["pkg"].items():
    if not pkg_data["rehash"]:
        continue
    print("\nPkg:", pkg)
    for platform in pkg_data["platforms"]:
        full_url = tool_pkg["registry_url"] + "raw/main/" + platform + "/" + tool_pkg["suffix"] + "/" + pkg_data["file"]
        print("\nhashing: " + full_url)
        status, size, hash = rehash_pkg(full_url)

        if (status):
            print("Size:", size)
            print("Hash:", hash)
            update_tool_manifest(tool_data, pkg, platform, full_url, size, hash)
    
    pkg_data["rehash"] = False


    #rehash_pkg(tool_pkg["registry_url"], tool_pkg["suffix"], pkg_data)

# Serializing to json
with open( tool_file, "w" ) as f:
    json.dump( tool_data , f, indent = 2 )

with open( tool_src_file, "w" ) as f:
    json.dump( tool_pkg , f, indent = 2 )


#print("JSON string = ", tool_pkg)
#print()

#    if not os.path.exists(tmp_dir):
#        os.makedirs(tmp_dir)
