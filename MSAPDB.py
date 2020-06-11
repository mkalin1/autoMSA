import requests
import urllib
import re
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
from subprocess import call

PDBalignNames=[]

with open('PDBalignNames.txt', 'r') as f:
    PDBalignNames=f.read().split('\n')
#print(PDBalignNames)
leng=len(PDBalignNames)




for i in range (0,leng):
    print(PDBalignNames[i])
    parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
    resp = urllib.request.urlopen("https://www.rcsb.org/structure/"+PDBalignNames[i])
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        uniID=link['href']
        #print(uniID.encode("utf-8"))

        qupdb='www.uniprot.org/uniprot/'
        if qupdb in uniID:
            uniID=uniID
            #print(uniID)
            uniIDNAME=re.search('uniprot/(.*)',uniID)
            print(uniIDNAME.group(1))

            parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
            resp = urllib.request.urlopen(uniID)
            soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
            
            for link in soup.find_all('a', href=True):
                families=link['href']

                qu='query=family:%22'
                if qu in families:
                    familylinks=(families)
                    #print(familylinks)
                    familyURL='https://www.uniprot.org'+familylinks
                    #print(familyURL)
                    familyNAME=re.search('%22(.*)%',familyURL)
                    print(familyNAME.group(1))                             ######## save this to file!!!

                    familyURL='https://www.uniprot.org'+familylinks+'&format=fasta&force=true&compress=yes'
                    #print(familyURL)
                    #pagePROT=requests.get(familyURL, allow_redirects=True)

                    urllib.request.urlretrieve(familyURL, '/Users/Michael/Downloads/'+'PDB_'+PDBalignNames[i]+'_UNI_'+uniIDNAME.group(1)+'_FAM_'+familyNAME.group(1)+'.gz')


    