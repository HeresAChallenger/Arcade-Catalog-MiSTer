#!/usr/bin/env python3
from __future__ import annotations
import argparse, io, json, re, sys, urllib.request, zipfile
from pathlib import Path

UA='Arcade-Catalog-MiSTer-Builder/0.3'

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':UA})
    with urllib.request.urlopen(req,timeout=90) as r: return r.read()

def load_db(raw):
    if raw[:2] == b'PK':
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            js=[n for n in z.namelist() if n.lower().endswith('.json')]
            if not js: raise ValueError('zip sem json')
            return json.loads(z.read(max(js,key=lambda n:z.getinfo(n).file_size)))
    return json.loads(raw)

def iter_files(db):
    files=db.get('files',{}) if isinstance(db,dict) else {}
    if isinstance(files,dict):
        for path,meta in files.items(): yield str(path),meta

def file_url(meta):
    if isinstance(meta,str) and meta.startswith(('http://','https://')): return meta
    if isinstance(meta,dict):
        for k in ('url','download_url'):
            v=meta.get(k)
            if isinstance(v,str) and v.startswith(('http://','https://')): return v
    return ''

def is_main_arcade(path):
    p=path.replace('\\','/').lstrip('/')
    if not p.lower().endswith('.mra'): return False
    parts=p.split('/')
    try: i=next(i for i,x in enumerate(parts) if x.lower()=='_arcade')
    except StopIteration: return False
    # Main library only: _Arcade/Foo.mra. _alternatives and generated folders excluded.
    return len(parts)==i+2

def safe_id(s): return re.sub(r'[^A-Za-z0-9_.-]+','_',s)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--sources',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    cfg=json.loads(args.sources.read_text(encoding='utf-8'))
    args.out.mkdir(parents=True,exist_ok=True)
    manifest=[]; failures=[]
    for src in cfg['sources']:
        sid=src['id']; required=bool(src.get('required'))
        print(f'[db] {sid}',file=sys.stderr)
        try: db=load_db(fetch(src['url']))
        except Exception as e:
            failures.append((sid,str(e),required));
            if required: raise
            print(f'[aviso] {sid}: {e}',file=sys.stderr); continue
        n=0
        for path,meta in iter_files(db):
            if not is_main_arcade(path): continue
            u=file_url(meta)
            if not u: continue
            try: data=fetch(u)
            except Exception as e:
                print(f'[aviso] {sid}:{path}: {e}',file=sys.stderr); continue
            name=Path(path.replace('\\','/')).name
            d=args.out/safe_id(sid); d.mkdir(parents=True,exist_ok=True)
            # Source prefix prevents collisions while preserving original filename in manifest.
            target=d/(safe_id(path.replace('/','__')))
            if not target.name.lower().endswith('.mra'): target=target.with_suffix('.mra')
            target.write_bytes(data)
            manifest.append((sid,path,name,str(target.relative_to(args.out))))
            n+=1
        print(f'[ok] {sid}: {n} MRAs',file=sys.stderr)
    with (args.out/'_manifest.tsv').open('w',encoding='utf-8') as f:
        f.write('source\tpath\tfilename\tlocal\n')
        for r in manifest: f.write('\t'.join(r)+'\n')
    print(f'Coletados: {len(manifest)} MRAs')

if __name__=='__main__': main()
