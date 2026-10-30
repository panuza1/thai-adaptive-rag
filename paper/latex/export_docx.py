"""Export authoritative LaTeX through Pandoc and the retained AUCC Word layout."""
import importlib.util
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree as E

ROOT=Path(__file__).resolve().parent

def main():
    tex=(ROOT/'main.tex').read_text()
    tex=re.sub(r'\\citep\{ref(\d+)\}',r'[\1]',tex)
    bbl=(ROOT/'submission_anonymous.bbl').read_text()
    bbl=re.sub(r'\\bibinfo\{[^}]+\}','',bbl)
    bbl=re.sub(r'\\bibitem\[.*?\]\{ref(\d+)\}',lambda m:'['+m[1]+'] ',bbl,flags=re.S)
    tex=tex.replace('\\bibliography{references}',r'\section*{References}'+'\n'+bbl)
    with tempfile.TemporaryDirectory(prefix='aucc_docx_') as directory:
        tmp=Path(directory);(tmp/'expanded.tex').write_text(tex)
        subprocess.run(['pandoc',str(tmp/'expanded.tex'),'-f','latex','-t','gfm','--wrap=none','-o',str(tmp/'draft.md')],check=True,cwd=ROOT)
        md=(tmp/'draft.md').read_text();md=re.sub(r'<[^>]+>','',md)
        md=re.sub(r'!\[.*?\]\(.*?\)(?:\{.*?\})?','',md)
        # Existing template builder places the identical two imported figures.
        title='Adaptive Retrieval Strategy for Cost-Efficient and Reliable Thai RAG Systems'
        md='# '+title+'\n\n'+md[md.index('## Abstract'):]
        for i,name in enumerate(['Introduction','Related Work','Proposed Method','Experimental Setup','Results','Discussion','Limitations','Conclusion'],1):
            md=md.replace('## '+name+'\n','## '+str(i)+'. '+name+'\n')
        (tmp/'draft.md').write_text(md)
        (tmp/'qa').mkdir()
        for name in ['aucc_oral_english.docx']:shutil.copy(ROOT.parent/name,tmp/name)
        shutil.copy(ROOT.parent/'qa/template_inventory.json',tmp/'qa/template_inventory.json')
        for source,dest in [('retrieval.png','retrieval_figure.png'),('ablations.png','ablation_figure.png')]:shutil.copy(ROOT/'figures'/source,tmp/'qa'/dest)
        spec=importlib.util.spec_from_file_location('aucc_word',ROOT.parent/'build_manuscript.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.ROOT=tmp;module.main()
        with ZipFile(tmp/'aucc2027_manuscript.docx') as z:parts={n:z.read(n) for n in z.namelist()}
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'};doc=E.fromstring(parts['word/document.xml'])
        for p in list(doc.findall('w:body/w:p',ns)):
            value=''.join(p.xpath('.//w:t/text()',namespaces=ns))
            if value in ['Panupong Chaichun','Affiliation pending','Corresponding author: panuponghaichun@gmail.com','Advisor pending | Working manuscript']:
                if value=='Panupong Chaichun':
                    ts=p.findall('.//w:t',ns);ts[0].text='Anonymous review manuscript'
                else:p.getparent().remove(p)
        parts['word/document.xml']=E.tostring(doc,xml_declaration=True,encoding='UTF-8',standalone=True)
        core=E.fromstring(parts['docProps/core.xml'])
        for node in core:
            if E.QName(node).localname in ['creator','lastModifiedBy']:node.text=''
        parts['docProps/core.xml']=E.tostring(core,xml_declaration=True,encoding='UTF-8',standalone=True)
        with ZipFile(ROOT/'submission_anonymous.docx','w',ZIP_DEFLATED) as z:
            for n,b in parts.items():z.writestr(n,b)
        assert not any(x.encode() in parts['word/document.xml'] for x in ['Panupong','panuponghaichun@gmail.com','KMUTT'])
        shutil.copy(tmp/'draft.md',ROOT/'qa/docx_export.md')
    print(ROOT/'submission_anonymous.docx')

if __name__=='__main__':main()
