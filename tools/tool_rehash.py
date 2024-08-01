#!/usr/bin/python

import json
import requests
import hashlib


tool_file = "tools.json"
#out_tool_file = "tools_out.json"
#tool_src_file = "tools_source.json"

def load_data():
    f = open(tool_file)
    data = json.load(f)
    f.close()
    return data

def rehash_pkg(url):
    m = hashlib.sha256()
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            print("bad response!")
            return False, 0, 0

        total =  int(r.headers['content-length'])
        for i in r.iter_content(chunk_size=64*1024):
            m.update(i)
        return True, total, m.hexdigest()



tool_data = load_data()     # loaded from tools.json

for tool in tool_data["tools"]:
    for key, val in tool["versions"][0].items():
        if not isinstance(val, dict):
            continue

        if val.get("rehash", 0):
            print("Get hash for: ", tool["name"], ":", key)
            status, size, hash = rehash_pkg(val["url"])
            if (status):
                print("Size:", size, " Hash:",hash)
                val["size"] = size
                val["sha256"] = hash
                del val["rehash"]


# Serializing to json
with open( tool_file, "w" ) as f:
    json.dump( tool_data , f, indent = 2 )

