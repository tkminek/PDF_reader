import re
from re import finditer
from re import findall




# text="""
# Variabilní symbol: 8477 FAKTURA - DAŇOVÝ DOKLAD
# (2) -1 Specifický symbol: 202136687 Číslo faktury: 202136687
# buumémení m9) Klientské číslo; 8477
# Dodavatel Odběratel Korespondenční adresa
# C2NET s.r.o Aporéma CZ s.r.o p
# J.V.Sládka 84 Potoční 1094
# 73801 Frýdek Místek 73801 Frýdek-Místek, Frýdek
# cz Česká Republika ;
# IČO: 28584996 IČO: 27830322 Aporéma CZ s.r.o
# DIČ: CZ28584996 DIČ: CZ27830322 Potoční 1094
# Tel.: 558 111 111 73801 Frýdek-Místek, Frýdek
# Email: infoec2net.cz Česká Republika
# Číslo účtu: 5005024100 Typ úhrady: Bankovní převod Datum vystavení: 01.08.2021
# Banka: 5500 Vystavil: Barbora Cvičková Datum splatnosti: 15.08.2021
# Zdanitelné plnění: 01.08.2021
# Popis položky MJ Počet Cena Mj Sazba DPH DPH Cena bez DPH Cena s DPH
# . Internet za období 8/2021 měs 1 600,00 21% 126,00 600,00 726,00
# Celkem 126,00 600,00 726,00 KU
# CELKEM K ÚHRADĚ včetně DPH = 726,00 Kč
# r ) PR 0 | r l ">
# v era: R
# nd ton A nz. M :
# A
# C0 1E= l sira.
# 20 te G0 KALY Fvdok Mistek
# ME 2849790 07 0/2 24644991,
# Číslo faktury: 202136687 Strana: 1/1
# """





# cislo faktury #
def cislo_faktury(text):     
    cislo_faktury_dict=dict()      
    p = "[Ff][Aa][Kk][Tt][Uu][Rr][Aa]\s+-\s+[Dd][Aa]\D[Oo][Vv][YyÝý]\s+[Dd][Oo][Kk][Ll][Aa][Dd]\s+\D+[.:]\s{0,10000}\D{0,2}\d+"
    if findall(p,text)!=[]:
        for match in finditer(p,text):
            hodnota=match.group()
            value=hodnota.split("č.")[-1].strip()
            if "cislo_faktury" not in cislo_faktury_dict:
                cislo_faktury_dict["cislo_faktury"]=value
    else:             
        cislo_faktury_dict["cislo_faktury"] = "unknow"
    return(cislo_faktury_dict) 
    


# datumy #      
def datums_vystaveni(text):
    datums_vystaveni_dict=dict()
    p= "Datum\s{0,10000}[Vv][Yy][Ss][Tt][Aa][Vv][Ee][Nn][IiÍí][:\s+]\D{0,10000}\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}"
    if findall(p,text)!=[]:
        for match in finditer(p,text):
            hodnota=match.group()
            value=re.findall(r'\d+', hodnota)
            datums_vystaveni_dict["Datum vystaveni"]="-".join(value).strip()
    else:
        datums_vystaveni_dict["Datum vystaveni"]="unknow"
    return(datums_vystaveni_dict)     

def datums_splatnosti(text):
    datums_splatnosti_dict=dict()
    p= "Datum\s{0,10000}[Ss][Pp][Ll][Aa][Tt][Nn][Oo][Ss][Tt][IiÍí][:\s+]\D{0,10000}\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}"
    if findall(p,text)!=[]:
        for match in finditer(p,text):
            hodnota=match.group()
            value=re.findall(r'\d+', hodnota)
            datums_splatnosti_dict["Datum splatnosti"]="-".join(value).strip()
    else:
        datums_splatnosti_dict["Datum splatnosti"]="unknow"
    return(datums_splatnosti_dict)

def datums_zdaneni(text):
    datums_zdaneni_dict=dict()
    p= "Datum\s{0,10000}\D{0,10000}[Zz][Dd][Aa][NnŇň]\D{0,10000}[:\s+]\D{0,10000}\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}"
    if findall(p,text)!=[]:
        for match in finditer(p,text):
            hodnota=match.group()
            value=re.findall(r'\d+', hodnota)
            datums_zdaneni_dict["Datum zdaneni"]="-".join(value).strip()
    else:
        datums_zdaneni_dict["Datum zdaneni"]="unknow"
    return(datums_zdaneni_dict)    

 # odberatel dodavatel + ICO#      
def odberatel_dodavatel(text):
    odberatel_dodavatel_dict=dict()
    p_od= "[O][Dd][Bb]\D[Rr][Aa][Tt][Ee][Ll]"
    p_do= "[D][Oo][Dd][Aa][Vv][Aa][Tt][Ee][Ll]"
    p_ico= "[Ii][ČčCc]\s{0,10000}[:-]\s{0,10000}\d+|[Ii][ČčCc]\s{0,10000}\s{0,10000}\d+"
    if findall(p_od,text)!=[] and findall(p_do,text)!=[] and findall(p_ico,text)!=[]: 
        for match in finditer(p_od,text):
            hodnota_od=match.group()
            pozice_od=int(match.span()[0])        
        for match in finditer(p_do,text):
            hodnota_do=match.group()
            pozice_do=int(match.span()[0])
        if pozice_od<pozice_do:
            poradi=[hodnota_od,hodnota_do]
        else:
            poradi=[hodnota_do,hodnota_od]
        
        index_ico=0
        for match in finditer(p_ico,text):
            hodnota_ico=match.group()
            if index_ico<2:
                odberatel_dodavatel_dict[poradi[index_ico]]=re.findall(r'\d+', hodnota_ico)[0]
            index_ico+=1
    else:
        odberatel_dodavatel_dict["ODBERATEL"] ="unknow"
        odberatel_dodavatel_dict["DODAVATEL"] = "unknow"
    return(odberatel_dodavatel_dict)        

# castka#     
def castka(text):
    castka_dict=dict()    
    p_castka= "[Cc][Ee][Ll][Kk][Ee][Mm]\s{0,10000}[Kk]\D+\d+\s{0,10000}\d{3}[,.]\d{2}\s{0,10000}[Cc][Zz][Kk]|[Cc][Ee][Ll][Kk][Ee][Mm]\s{0,10000}\D+\d+\s{0,10000}\d{3}[,.]\d{2}\s{0,10000}[Kk][CcČč]"
    vysledek=re.findall(p_castka,text)
    if vysledek!=[]:
        suma=re.findall("[-\d]+",vysledek[0])
        castka="".join(suma[:-1])+"."+str(suma[-1])
        castka_dict["Castka"]=castka
    else:
        castka_dict["Castka"] = "unknow"

    return(castka_dict)    
    
        
#print(castka(text))        

     