"""
ACR 未使用進階 SKU 版本不提供內建之容器鏡像生命週期管理
自行撰寫腳本處理
需運行在 az cli 可正常運作的主機
"""
import os
import json

acrName = 'yourACR'
repos = json.loads(os.popen('az acr repository list --output json --name {} | jq'.format(acrName)).read())

for repo in repos:
    print(repo)
    # 清除未標記鏡像
    untag_manifests = json.loads(os.popen('az acr repository show-manifests --output json --name {} --repository {} --query "[?tags[0]==null].digest" | jq'.format(acrName, repo)).read())
    for digest in untag_manifests:
        print(digest)
        os.system('az acr repository delete --name {} --image {}@{} --yes'.format(acrName, repo, digest))

    manifests = json.loads(os.popen('az acr repository show-manifests --output json --name {} --repository {} --orderby time_desc | jq'.format(acrName, repo)).read())
    print(len(manifests))
    # 保留 50 個版本
    if len(manifests) > 50:
        for manifest in manifests[50:-1]:
            print(manifest['timestamp'])
            os.system('az acr repository delete --name {} --image {}@{} --yes'.format(acrName, repo, manifest['digest']))
