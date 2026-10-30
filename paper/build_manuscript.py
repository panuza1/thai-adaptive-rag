"""Populate the retained AUCC template; preserve unrelated package parts."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
from zipfile import ZipFile,ZIP_DEFLATED
from io import BytesIO
from lxml import etree as E
from docx import Document
from docx.shared import Inches

ROOT=Path(__file__).resolve().parent
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
NS={'w':W,'r':R}
def el(tag,**attrs):return E.Element('{'+W+'}'+tag,{'{'+W+'}'+k:str(v) for k,v in attrs.items()})
def add(parent,tag,**attrs):v=el(tag,**attrs);parent.append(v);return v

def para(text,role='body'):
    p=el('p');pr=add(p,'pPr')
    if role=='title':add(pr,'pStyle',val='Title')
    alignment='center' if role in ['title','author','meta','heading','caption'] else ('left' if role in ['sub','reference'] else 'both')
    add(pr,'jc',val=alignment)
    add(pr,'spacing',before=160 if role in ['heading','sub'] else 0,after=100 if role in ['title','heading','meta'] else 40,line=240,lineRule='auto')
    if role in ['heading','sub','title','author','meta']:add(pr,'keepNext')
    if role=='reference':
        add(pr,'ind',left=280,hanging=280);add(pr,'keepLines')
    r=add(p,'r');rp=add(r,'rPr');add(rp,'rFonts',ascii='Times New Roman',hAnsi='Times New Roman',eastAsia='Times New Roman',cs='Times New Roman')
    size={'title':28,'author':24,'caption':16,'cell':17}.get(role,20)
    add(rp,'sz',val=size);add(rp,'color',val='000000')
    if role in ['title','heading','sub']:add(rp,'b')
    if role=='sub':add(rp,'i')
    t=add(r,'t');t.set('{http://www.w3.org/XML/1998/namespace}space','preserve');t.text=text
    return p

def table(lines):
    cells=[[s.strip() for s in l.strip('|').split('|')] for l in lines if not re.match(r'^\|[-:| ]+\|$',l)]
    t=el('tbl');pr=add(t,'tblPr');add(pr,'tblW',w=4660,type='dxa');add(pr,'tblLayout',type='fixed')
    borders=add(pr,'tblBorders')
    for k in ['top','bottom','insideH']:add(borders,k,val='single',sz=4,color='000000')
    grid=add(t,'tblGrid');width=4660//len(cells[0])
    for _ in cells[0]:add(grid,'gridCol',w=width)
    for i,row in enumerate(cells):
        tr=add(t,'tr');trp=add(tr,'trPr');add(trp,'cantSplit')
        if i==0:add(trp,'tblHeader')
        for value in row:
            value={'B1 dense':'B1','B2 hybrid':'B2','B3 hybrid + reranking':'B3','P1 adaptive':'P1'}.get(value,value)
            tc=add(tr,'tc');tcp=add(tc,'tcPr');add(tcp,'tcW',w=width,type='dxa');p=para(value,'cell')
            if i==0:add(p.find('w:r/w:rPr',NS),'b')
            tc.append(p)
    return t

def main():
    ref=ROOT/'aucc_oral_english.docx';inventory=json.loads((ROOT/'qa/template_inventory.json').read_text())
    assert hashlib.sha256(ref.read_bytes()).hexdigest()==inventory['reference_sha256']
    with ZipFile(ref) as z:parts={n:z.read(n) for n in z.namelist()}
    root=E.fromstring(parts['word/document.xml']);body=root.find('w:body',NS)
    sections=[deepcopy(s) for s in root.findall('.//w:sectPr',NS)]
    for child in list(body):body.remove(child)
    lines=(ROOT/'draft.md').read_text().splitlines();title=lines[0].lstrip('# ').upper()
    body.append(para(title,'title'));body.append(para('Panupong Chaichun','author'))
    body.append(para('Affiliation pending','meta'));body.append(para('Corresponding author: panuponghaichun@gmail.com','meta'))
    body.append(para('Advisor pending | Working manuscript','meta'))
    boundary=el('p');add(boundary,'pPr').append(sections[0]);body.append(boundary)
    active=False;paragraph=[];tablelines=[];refs=False;table_count=0
    pictures=[]
    def picture(filename,caption):
        temporary=Document();temporary.add_picture(str(ROOT/'qa'/filename),width=Inches(3.24))
        stream=BytesIO();temporary.save(stream)
        with ZipFile(stream) as z:
            tree=E.fromstring(z.read('word/document.xml'))
            p=deepcopy(tree.find('w:body/w:p',NS));rid='rIdResearchFigure'+str(len(pictures)+1)
            for node in p.iter():
                if '{'+R+'}embed' in node.attrib:node.set('{'+R+'}embed',rid)
            media=next(n for n in z.namelist() if n.startswith('word/media/'))
            target='media/research_figure_'+str(len(pictures)+1)+'.png'
            pictures.append((rid,target,z.read(media)))
        body.append(p);body.append(para(caption,'caption'))
    def flush():
        nonlocal paragraph,tablelines,table_count
        if paragraph:
            text=' '.join(paragraph).replace('**','').replace('`','')
            body.append(para(text,'reference' if refs else 'body'));paragraph=[]
        if tablelines:
            table_count+=1
            captions={1:'Table 1. Frozen primary retrieval comparison.',2:'Table 2. Removal of individual P1 components.'}
            body.append(para(captions.get(table_count,'Table '+str(table_count)+'. Direct request measurements.'),'caption'))
            body.append(table(tablelines));tablelines=[]
            if table_count==1:picture('retrieval_figure.png','Figure 1. Retrieval quality and latency. The horizontal axis uses a logarithmic scale.')
            if table_count==2:picture('ablation_figure.png','Figure 2. Change in measured nDCG after component removal. Source-derived relevance is non-exhaustive.')
    roman={1:'I',2:'II',3:'III',4:'IV',5:'V',6:'VI',7:'VII',8:'VIII'}
    for line in lines[1:]:
        if line.startswith('<!--'):continue
        if line=='## Abstract':active=True
        if not active:continue
        if not line.strip():flush();continue
        if line.startswith('|'):
            if paragraph:flush()
            tablelines.append(line);continue
        if tablelines:flush()
        if line.startswith('## '):
            flush();heading=line[3:];refs=heading=='References'
            m=re.match(r'(\d+)\. (.*)',heading)
            if m:heading=roman.get(int(m[1]),m[1])+'. '+m[2]
            body.append(para(heading.upper(),'heading'))
        elif line.startswith('### '):flush();body.append(para(line[4:],'sub'))
        else:paragraph.append(line)
    flush();body.append(sections[-1])
    parts['word/document.xml']=E.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    editable={'word/document.xml'}
    relname='word/_rels/document.xml.rels';rels=E.fromstring(parts[relname])
    for rid,target,data in pictures:
        E.SubElement(rels,'{http://schemas.openxmlformats.org/package/2006/relationships}Relationship',Id=rid,Type=R+'/image',Target=target)
        parts['word/'+target]=data
    parts[relname]=E.tostring(rels,xml_declaration=True,encoding='UTF-8',standalone=True);editable.add(relname)
    ct=E.fromstring(parts['[Content_Types].xml'])
    if not any(n.get('Extension')=='png' for n in ct):
        E.SubElement(ct,'{http://schemas.openxmlformats.org/package/2006/content-types}Default',Extension='png',ContentType='image/png')
        parts['[Content_Types].xml']=E.tostring(ct,xml_declaration=True,encoding='UTF-8',standalone=True);editable.add('[Content_Types].xml')
    for name in list(parts):
        if name.startswith('word/header') and name.endswith('.xml'):
            header=E.fromstring(parts[name]);nodes=header.findall('.//w:t',NS)
            if nodes:
                nodes[0].text='The Asia Undergraduate Conference on Computing AUCC 2027'
                for node in nodes[1:]:node.text=''
                for h in header.findall('.//w:highlight',NS):h.getparent().remove(h)
                parts[name]=E.tostring(header,xml_declaration=True,encoding='UTF-8',standalone=True);editable.add(name)
    output=ROOT/'aucc2027_manuscript.docx'
    with ZipFile(output,'w',ZIP_DEFLATED) as z:
        for name,data in parts.items():z.writestr(name,data)
    with ZipFile(output) as z:
        assert all(hashlib.sha256(z.read(n)).hexdigest()==h for n,h in inventory['parts'].items() if n not in editable)
    (ROOT/'qa/package_validation.json').write_text(json.dumps({'reference_unchanged':hashlib.sha256(ref.read_bytes()).hexdigest()==inventory['reference_sha256'],'unchanged_parts_verified':True,'changed_parts':sorted(editable),'body_word_count':len((ROOT/'draft.md').read_text().split())},indent=2))
    print(output)

if __name__=='__main__':main()
