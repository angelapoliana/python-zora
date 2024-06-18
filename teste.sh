read -p  "Digite o id do workspace: " ID

function get()
{
  echo Downloading $1 >&2
  curl -s "$1" \
  -H 'authority: zora-dashboard.undistro.io' \
  -H 'Cookie: __Secure-next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..MTApnyo9k7VGXHNF.K5zWZJn0fdYU8dKua2ynMeT4c7Y4mSFL4nfaOsp7bV5PKU4ZaRaJutzIoDDBYfmYEevO9shBT66nrDzfB7lKZ_VGLG0fTn9Ot62UEYQ0W5Imq6Xfn6aufXv8iLXpKPo55SruDK8x2-v4MyO2CWOzWpY2n80gnSr5i_V_YIJM4QCbhnL5wY3If3lz-E6Vo-xpRnvYXIhHA8SH19h0-bQQ2sbAqFwbPFObwY7xSaNRas87fEWZOybc1COGmpG65l8cIaK2BALu8I2pGglzRW8CTCS13d0WXZgtXPoCVihMhJOkjjWVqCi46FBMfUOJyg_lMk4aHYizpxbNmPvk1mw0IQ71EItuBRrWImAoWTg.xyh8c8Vb8-y-y_dcUDoYPQ' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.6' \
  -H 'cache-control: no-cache' \
  -H 'cookie: __Host-next-auth.csrf-token=c8464bd7e80c332e9b21b8fd2235856ebbad8b5d5e313b21d0213a86d79ea790%7C405aa72f8250a5848f882a1f8b05b5f72848d90d8f3ee34bb8d18735c0ffd8a3' \
  -H 'dnt: 1' \
  -H 'pragma: no-cache' \
  -H 'referer: https://zora-dashboard.undistro.io/' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'sec-gpc: 1' \
  -H 'user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36' \
  --compressed
}
get  "https://zora-dashboard.undistro.io/api/v2/clusters?workspace=$ID" > clusters.json
totalissues=`cat clusters.json| jq '.[]|.totalIssues'`
cat clusters.json | jq '.[]|.name' -r | while read cluster; do
    get "https://zora-dashboard.undistro.io/api/v2/workspaces/$ID/misconfigurations?clusterName=${cluster}&pageSize=$totalissues" > cluster-$cluster.json
done
./issues.py cluster-*.json > issues.csv