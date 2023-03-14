import lxml
import lxml.etree as ET
import sys
import re
import html 
import codecs
import os

def lreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' starts 'string'.
    """
    return re.sub('^%s' % pattern, sub, string)

def rreplace(pattern, sub, string):
    """
    Replaces 'pattern' in 'string' with 'sub' if 'pattern' ends 'string'.
    """
    return re.sub('%s$' % pattern, sub, string)

def gettexttag(element):
    texttag=ET.tostring(element).strip().decode("utf-8")
    texttag=lreplace("<mrk .*?>","",texttag)
    texttag=rreplace("</mrk>","",texttag)
    texttag=html.unescape(texttag)
    return(texttag)

def getmid(element):
    mid=""
    try:
        mid=element.attrib['mid']
    except:
        print(sys.exc_info())
    return(mid)

def SDLXLIFF2tabtxt(filein,fileout,tags=False,append=False):
    if append:
        sortida=codecs.open(fileout,"a",encoding="utf-8")
    else:
        sortida=codecs.open(fileout,"w",encoding="utf-8")
    try:
        parser = ET.XMLParser(recover=True)
        tree = ET.parse(filein, parser=parser)
        root = tree.getroot()
        tuvs=root.findall('.//{urn:oasis:names:tc:xliff:document:1.2}trans-unit')
        sources={}
        targets={}
        for tuv in tuvs:
            childs=[]
            for ch in tuv.iter():
                childs.append(ch.tag)
            if "{urn:oasis:names:tc:xliff:document:1.2}seg-source" in childs:
                for segsource in tuv.findall('.//{urn:oasis:names:tc:xliff:document:1.2}seg-source'):
                    childs2=[]
                    for ch in segsource.iter():
                        childs2.append(ch.tag)
                    if "{urn:oasis:names:tc:xliff:document:1.2}mrk" in childs2:
                        try:
                            for mrk in segsource.findall('{urn:oasis:names:tc:xliff:document:1.2}mrk'):
                                mid=getmid(mrk)
                                text=gettexttag(mrk)
                                sources[mid]=text
                        except:
                            print(sys.exc_info())
            if "{urn:oasis:names:tc:xliff:document:1.2}target" in childs:
                for target in tuv.findall('.//{urn:oasis:names:tc:xliff:document:1.2}target'):
                    childs3=[]
                    for ch in target.iter():
                        childs3.append(ch.tag)
                    if "{urn:oasis:names:tc:xliff:document:1.2}mrk" in childs3:
                        try:
                            for mrk in target.findall('{urn:oasis:names:tc:xliff:document:1.2}mrk'):
                                mid=getmid(mrk)
                                text=gettexttag(mrk)
                                targets[mid]=text
                        except:
                            print(sys.exc_info())
        keys=sources.keys()
        
        for clau in keys:
            if clau in targets:
                cadena=sources[clau]+"\t"+targets[clau]
                print(cadena)
                sortida.write(cadena+"\n")

    except:
        print(sys.exc_info())

if __name__ == "__main__":
    direntrada=sys.argv[1]
    outfile=sys.argv[2]
    for root, dirs, files in os.walk(direntrada):
        for file in files:
            if file.endswith(".sdlxliff"):
                sdlxlifffile=os.path.join(root, file)
                SDLXLIFF2tabtxt(sdlxlifffile,outfile,append=True)


