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
    cislo_faktury_dict={"cislo_faktury":"unknow"}
    P_ide=[
        "[Ff][Aa][Kk][Tt][Uu][Rr][Aa]\s+-\s+[Dd][Aa]\D[Oo][Vv][YyÝý]\s+[Dd][Oo][Kk][Ll][Aa][Dd]\s+\D+[.:]\s{0,10000}\D{0,2}\d+",
        "[ČčCc][ÍíIi][Ss][Ll][Oo]\s{0,10000}[Ff][Aa][Kk][Tt]\D+[.:-]\s{0,10000}\d+"
        ]
    index_c=0
    while index_c<=len(P_ide)-1:        
        if findall(P_ide[index_c],text)!=[]:
            for match in finditer(P_ide[index_c],text):
                hodnota=match.group()
                value=hodnota.split(" ")[-1].strip()
                cislo_faktury_dict["cislo_faktury"]=value
        index_c+=1    
    return(cislo_faktury_dict) 
    


# datumy #      
def datums_vystaveni(text):
    datums_vystaveni_dict={"Datum vystaveni":"unknow"}
    P_dv=[
        "Datum\s{0,10000}[Vv][Yy][Ss][Tt][Aa][Vv][Ee][Nn][IiÍí][:\s+]\D{0,10000}\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}"
        ]
    index_dv=0
    while index_dv<=len(P_dv)-1:
        if findall(P_dv[index_dv],text)!=[]:
            for match in finditer(P_dv[index_dv],text):
                hodnota=match.group()
                value=re.findall(r'\d+', hodnota)
                datums_vystaveni_dict["Datum vystaveni"]="-".join(value).strip()
        index_dv+=1            
    return(datums_vystaveni_dict)  
   

def datums_splatnosti(text):
    datums_splatnosti_dict={"Datum splatnosti":"unknow"}
    P_ds=[
        "Datum\s{0,10000}[Ss][Pp][Ll][Aa][Tt][Nn][Oo][Ss][Tt][IiÍí][:\s+]\D{0,10000}\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}"
        ]
    index_ds=0
    while index_ds<=len(P_ds)-1:
        if findall(P_ds[index_ds],text)!=[]:
            for match in finditer(P_ds[index_ds],text):
                hodnota=match.group()
                value=re.findall(r'\d+', hodnota)
                datums_splatnosti_dict["Datum splatnosti"]="-".join(value).strip()
        index_ds+=1
    return(datums_splatnosti_dict)

def datums_zdaneni(text):
    datums_zdaneni_dict={"Datum zdaneni":"unknow"}
    P_dz=[
        "Datum\s{0,10000}\D{0,10000}[Zz][Dd][Aa][NnŇň]\D{0,10000}[:\s+]\D{0,10000}\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}",
        "[Zz][Dd][Aa][NnŇň]\D{0,10000}[:\s+]\D{0,10000}\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}"
        ]
    index_dz=0
    while index_dz<=len(P_dz)-1:
        if findall(P_dz[index_dz],text)!=[]:
            for match in finditer(P_dz[index_dz],text):
                hodnota=match.group()
                value=re.findall(r'\d+', hodnota)
                datums_zdaneni_dict["Datum zdaneni"]="-".join(value).strip()
        index_dz+=1
    return(datums_zdaneni_dict)    

     
# def odberatel_dodavatel(text):
#     odberatel_dodavatel_dict=dict()
#     p_od= "[O][Dd][Bb]\D[Rr][Aa][Tt][Ee][Ll]"
#     p_do= "[D][Oo][Dd][Aa][Vv][Aa][Tt][Ee][Ll]"
#     p_ico= "[Ii][ČčCc]\s{0,10000}[:-]\s{0,10000}\d+|[Ii][ČčCc]\s{0,10000}\s{0,10000}\d+|[Ii][ČčCc][Oo]\s{0,10000}[:-]\s{0,10000}\d+"
#     if findall(p_od,text)!=[] and findall(p_do,text)!=[] and findall(p_ico,text)!=[]: 
#         for match in finditer(p_od,text):
#             hodnota_od=match.group()
#             pozice_od=int(match.span()[0])        
#         for match in finditer(p_do,text):
#             hodnota_do=match.group()
#             pozice_do=int(match.span()[0])
#         if pozice_od<pozice_do:
#             poradi=[hodnota_od,hodnota_do]
#         else:
#             poradi=[hodnota_do,hodnota_od]
        
#         index_ico=0
#         for match in finditer(p_ico,text):
#             hodnota_ico=match.group()
#             if index_ico<2:
#                 odberatel_dodavatel_dict[poradi[index_ico]]=re.findall(r'\d+', hodnota_ico)[0]
#             index_ico+=1
#     else:
#         odberatel_dodavatel_dict["ODBERATEL"] ="unknow"
#         odberatel_dodavatel_dict["DODAVATEL"] = "unknow"
#     return(odberatel_dodavatel_dict) 

# odberatel dodavatel + ICO#      
def odberatel_dodavatel(text):
    odberatel_dodavatel_dict={"Odberatel":"unknow","Dodavatel": "unknow"}
    P_od= [
        "[O][Dd][Bb]\D[Rr][Aa][Tt][Ee][Ll]"
           ]
    P_do= [
        "[D][Oo][Dd][Aa][Vv][Aa][Tt][Ee][Ll]"
        ]
    P_ico=[
        "[Ii][ČčCc]\s{0,10000}[:-]\s{0,10000}\d+",
        "[Ii][ČčCc]\s{0,10000}\s{0,10000}\d+",
        "[Ii][ČčCc][Oo]\s{0,10000}[:-]\s{0,10000}\d+"
        ]
    for i in range(len(P_od)):
        for j in range(len(P_do)):
            if findall(P_od[i],text)!=[] and findall(P_do[j],text)!=[]: 
                for match in finditer(P_od[i],text): 
                    pozice_od=int(match.span()[0])        
                for match in finditer(P_do[j],text):
                    pozice_do=int(match.span()[0])                    
                if pozice_od<pozice_do:
                    poradi=["Odberatel","Dodavatel"]
                else:
                    poradi=["Dodavatel","Odberatel"]
    for k in range(len(P_ico)):
        index_ico=0
        for match in finditer(P_ico[k],text):
            hodnota_ico=match.group()
            if index_ico<2:
                odberatel_dodavatel_dict[poradi[index_ico]]=re.findall(r'\d+', hodnota_ico)[0]
            index_ico+=1

    return(odberatel_dodavatel_dict)        

# castka#     
def castka(text):
    castka_dict={"Castka":"unknow"}    
    P_c=[
        "[Cc][Ee][Ll][Kk][Ee][Mm]\s{0,10000}[Kk]\D+\d+\s{0,10000}\d{0,10000}[,.]\d{0,10000}\s{0,10000}[Cc][Zz][Kk]|[Cc][Ee][Ll][Kk][Ee][Mm]\s{0,10000}\D+\d+\s{0,10000}\d{0,10000}[,.]\d{0,10000}\s{0,10000}[Kk][CcČč]"
        ]
    index_c=0
    while index_c<=len(P_c)-1:
        vysledek=re.findall(P_c[index_c],text)
        if vysledek!=[]:
            suma=re.findall("[-\d]+",vysledek[0])
            castka="".join(suma[:-1])+"."+str(suma[-1])
            castka_dict["Castka"]=castka
        index_c+=1
    return(castka_dict)    
    
        
# print(cislo_faktury(text))
# print(datums_vystaveni(text)) 
# print(datums_splatnosti(text)) 
# print(datums_zdaneni(text))
# print(odberatel_dodavatel(text)) 
# print(castka(text)) 
        

     