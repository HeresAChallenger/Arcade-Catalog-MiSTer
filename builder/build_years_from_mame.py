#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, io, os, re, sys, zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

YEAR_EXACT = re.compile(r'^(19|20)\d{2}$')
YEAR_EST = re.compile(r'^((?:19|20)\d{2})\?$')


def clean(s: str | None) -> str:
    return (s or '').replace('\r',' ').replace('\n',' ').replace('\t',' ').strip()


def mra_tag(text: str, tag: str) -> str:
    m = re.search(rf'<{re.escape(tag)}\b[^>]*>(.*?)</{re.escape(tag)}>', text, re.I | re.S)
    if not m:
        return ''
    v = re.sub(r'<[^>]+>', '', m.group(1))
    return clean(v.replace('&amp;', '&'))


def read_mras(root: Path):
    rows=[]
    manifest={}
    mf=root/'_manifest.tsv'
    if mf.exists():
        with mf.open(encoding='utf-8') as f:
            next(f,None)
            for line in f:
                a=line.rstrip('\n').split('\t')
                if len(a)>=4: manifest[a[3]]=a[2]
    for p in sorted(root.rglob('*.mra'), key=lambda q:str(q).lower()):
        t=p.read_text(encoding='utf-8', errors='replace')
        rows.append({
            'filename': manifest.get(str(p.relative_to(root)), p.name),
            'name': mra_tag(t,'name') or p.stem,
            'setname': mra_tag(t,'setname'),
            'mra_year': mra_tag(t,'year'),
            'manufacturer': mra_tag(t,'manufacturer'),
            'category': mra_tag(t,'category'),
            'homebrew': mra_tag(t,'homebrew'),
            'bootleg': mra_tag(t,'bootleg'),
            'rbf': mra_tag(t,'rbf'),
        })
    return rows


def open_xml(path: Path):
    if zipfile.is_zipfile(path):
        z=zipfile.ZipFile(path)
        names=[n for n in z.namelist() if n.lower().endswith('.xml')]
        if not names:
            raise SystemExit(f'ZIP sem XML: {path}')
        # The official lx.zip has one huge driver XML. Pick the largest XML.
        name=max(names, key=lambda n:z.getinfo(n).file_size)
        return z.open(name, 'r'), z
    return path.open('rb'), None


def load_mame(path: Path):
    fh, keeper = open_xml(path)
    result={}
    try:
        for event, elem in ET.iterparse(fh, events=('end',)):
            if elem.tag != 'machine':
                continue
            name=clean(elem.attrib.get('name'))
            if not name:
                elem.clear(); continue
            y=clean(elem.findtext('year'))
            desc=clean(elem.findtext('description'))
            man=clean(elem.findtext('manufacturer'))
            isbios=(elem.attrib.get('isbios') == 'yes')
            isdevice=(elem.attrib.get('isdevice') == 'yes')
            runnable=(elem.attrib.get('runnable','yes') != 'no')
            result[name.lower()]={
                'setname':name,'year_raw':y,'description':desc,'manufacturer':man,
                'isbios':isbios,'isdevice':isdevice,'runnable':runnable,
            }
            elem.clear()
    finally:
        fh.close()
        if keeper: keeper.close()
    return result


def load_overrides(path: Path | None):
    out={}
    if not path or not path.exists():
        return out
    with path.open(encoding='utf-8', newline='') as f:
        r=csv.DictReader(f, delimiter='\t')
        for row in r:
            key=(row.get('setname') or '').strip().lower()
            if not key: continue
            out[key]={
                'year':(row.get('year') or '').strip(),
                'status':(row.get('status') or 'year').strip(),
                'note':(row.get('note') or '').strip(),
            }
    return out


def normalize_mame_year(raw: str):
    raw=clean(raw)
    if YEAR_EXACT.match(raw): return raw, 'exact'
    m=YEAR_EST.match(raw)
    if m: return m.group(1), 'estimated'
    return '', 'unknown'


def not_applicable(mra: dict, mame: dict | None):
    # These are containers/firmware, not individual historical arcade releases.
    cat=mra['category'].lower()
    name=mra['name'].lower()
    if 'multigame' in cat:
        return True, 'multigame'
    if 'system bios' in name or name.endswith(' bios'):
        return True, 'bios'
    if mame and mame.get('isbios'):
        return True, 'bios'
    return False, ''


def resolve(mra, mame_db, overrides):
    sn=mra['setname'].lower()
    ov=overrides.get(sn)
    if ov:
        if ov['status'] in ('not-applicable','na'):
            return '', 'not-applicable', 'override', 'exact', ov['note']
        if YEAR_EXACT.match(ov['year']):
            return ov['year'], 'year', 'override', 'exact', ov['note']

    mm=mame_db.get(sn) if sn else None
    na, reason=not_applicable(mra, mm)
    if na:
        return '', 'not-applicable', f'policy-{reason}', 'exact', ''

    if mm:
        y,conf=normalize_mame_year(mm['year_raw'])
        if y:
            return y, 'year', 'mame', conf, ''

    my=clean(mra['mra_year'])
    if YEAR_EXACT.match(my):
        return my, 'year', 'mra-fallback', 'fallback', ''
    return '', 'unknown', 'none', 'unknown', ''


def main():
    ap=argparse.ArgumentParser(description='Gera arcade_years.tsv usando MAME como fonte canonica de ano.')
    ap.add_argument('--mame-xml', type=Path, required=True, help='mameNNNNlx.zip ou XML de -listxml')
    ap.add_argument('--mra-dir', type=Path, required=True)
    ap.add_argument('--overrides', type=Path)
    ap.add_argument('--out-dir', type=Path, required=True)
    args=ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    mras=read_mras(args.mra_dir)
    mame=load_mame(args.mame_xml)
    overrides=load_overrides(args.overrides)

    out=[]; audit=[]; seen=set()
    for r in mras:
        dk=(r['filename'].lower(), r['setname'].lower())
        if dk in seen: continue
        seen.add(dk)
        y,status,source,confidence,note=resolve(r,mame,overrides)
        mm=mame.get(r['setname'].lower()) if r['setname'] else None
        my=r['mra_year'] if YEAR_EXACT.match(r['mra_year']) else ''
        out.append({
            'filename':r['filename'],'setname':r['setname'],'year':y,'status':status,
            'source':source,'confidence':confidence,
        })
        canonical=y if status=='year' else ''
        if status!='year' or my != canonical or source!='mame':
            audit.append({
                'filename':r['filename'],'setname':r['setname'],'mra_year':r['mra_year'],
                'canonical_year':canonical,'status':status,'source':source,'confidence':confidence,
                'mame_year_raw': mm['year_raw'] if mm else '',
                'mame_description': mm['description'] if mm else '',
                'category':r['category'],'note':note,
            })

    fields=['filename','setname','year','status','source','confidence']
    with (args.out_dir/'arcade_years.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(out)
    af=['filename','setname','mra_year','canonical_year','status','source','confidence','mame_year_raw','mame_description','category','note']
    with (args.out_dir/'arcade_year_audit.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=af,delimiter='\t',lineterminator='\n'); w.writeheader(); w.writerows(audit)

    total=len(out); exact=sum(r['source']=='mame' and r['confidence']=='exact' for r in out)
    est=sum(r['source']=='mame' and r['confidence']=='estimated' for r in out)
    fall=sum(r['source']=='mra-fallback' for r in out); na=sum(r['status']=='not-applicable' for r in out)
    unk=sum(r['status']=='unknown' for r in out); diverg=sum(1 for a in audit if a['mra_year'] and a['canonical_year'] and a['mra_year'] != a['canonical_year'])
    text=(
        'Arcade Catalog - auditoria de anos\n'
        '=================================\n'
        f'MRAs:                     {total}\n'
        f'MAME exato:               {exact}\n'
        f'MAME estimado (YYYY?):     {est}\n'
        f'Fallback do MRA:           {fall}\n'
        f'Sem ano aplicavel:         {na}\n'
        f'Ano desconhecido:          {unk}\n'
        f'Divergencias MRA x canon:  {diverg}\n'
    )
    (args.out_dir/'year_coverage.txt').write_text(text,encoding='utf-8')
    print(text,end='')
    if unk:
        print('AVISO: ainda existem anos desconhecidos.', file=sys.stderr)

if __name__=='__main__':
    main()
