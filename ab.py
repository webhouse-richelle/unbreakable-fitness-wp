import os,sys,json,urllib.request,ssl,base64
ssl._create_default_https_context=ssl._create_unverified_context
BASE="https://syn04ae.syd5.hostyourservices.net/~unbreaka/"
USER="admin_6qxcmjpy"; PW="lkpm OYSl nYjf 4S0E vGBH SgyR"
AUTH=base64.b64encode(f"{USER}:{PW}".encode()).decode()
def call(route, method="GET", body=None, raw=False):
    url=BASE+"?rest_route="+route if route.startswith("/") else BASE+route
    data=None
    if body is not None:
        data=json.dumps(body).encode()
    req=urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization","Basic "+AUTH)
    req.add_header("Content-Type","application/json")
    req.add_header("User-Agent","Mozilla/5.0")
    try:
        r=urllib.request.urlopen(req, timeout=60)
        d=r.read().decode()
    except urllib.error.HTTPError as e:
        d=e.read().decode(); return {"__err":e.code,"body":d}
    if raw: return d
    try: return json.loads(d)
    except: return d
if __name__=="__main__":
    # quick test
    print(call("/wp/v2/pages/12&_fields=id,title,status,link"))
