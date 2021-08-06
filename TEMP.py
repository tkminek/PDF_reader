import re
from re import finditer

# text="""
# FAKTURA - DANOVY DOKLAD č. AF7777
# Evidenční číslo 7
# Datum vystavení:14/06/2018
# Datum zdanitelného plnění: 14.06.2018
# Datum splatnosti: 24. 06. 2018
# Forma úhrady: Bankovním převodem
# Variabilní symbol: 7
# Číslo bankovního účtu: 12345678910/0800
# IBAN: CZ4055000000004040337001
# SWIFT: GIBACZPX
# ODBĚRATEL DODAVATEL
# Firma s.r.o Jan Novák
# Stará 1 Smetanova 6
# 21212, Praha 10000, Lhota
# Česká republika Česká republika
# IČ: 1345678  IČ: 87654321
# DIČ: CZ87654321 Plátce DPH
# Počet Popis Sazba DPH Cena Celkem
# 1,00 Ks Poskytování softwaru 21% 500,00 Kč 605,00 Kč
# 1,00 Ks Technická podpora 21% 400,00 Kč 484,00 Kč
# Sazba DPH Základ DPH Celkem
# 21% 900,00 Kč 189,00 Kč 1 089,00 Kč
# Celkem 900,00 Kč 189,00 Kč 1 089,00 Kč
# Celkem k úhradě 1 089.00 Kč
# Společnost je zapsaná do obchodního rejstříku vedeného Městským soudem v Praze, oddíl C, vložka 12345.
# Vystavil(a): Alena Suchá Vygenerováno pomocí FakturaOnline.cz"""



def create_pattern(text):
    # cislo faktury #
    try:
        faktura_dict=dict()
        p = "[Ff][Aa][Kk][Tt][Uu][Rr][Aa]\s+-\s+[Dd][Aa]\D[Oo][Vv][YyÝý]\s+[Dd][Oo][Kk][Ll][Aa][Dd]\s+\D+[.:]\s{0,10000}\D{0,2}\d+"
        for match in finditer(p,text):
            hodnota=match.group()
            value=hodnota.split("č.")[-1].strip()
            if "cislo_faktury" not in faktura_dict:
                faktura_dict["cislo_faktury"]=value
    except:
            faktura_dict["cislo_faktury"] = "unknow"


    # datumy #
    try:
        p= "\Datum\D+[:\s+]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,2}[\/.]\s{0,10000}\d{1,4}"
        for match in finditer(p,text):
            hodnota=match.group()
            pozice=match.span()
            key=re.findall(r'\D+', hodnota)[0].strip()
            value=re.findall(r'\d+', hodnota)
            faktura_dict[key]="-".join(value).strip()
    except:
        faktura_dict["datumy"] = "unknow"

    # odberatel dodavatel + ICO#
    try:
        p_od= "[O][Dd][Bb]\D[Rr][Aa][Tt][Ee][Ll]"
        for match in finditer(p_od,text):
            hodnota_od=match.group()
            pozice_od=int(match.span()[0])
        p_do= "[D][Oo][Dd][Aa][Vv][Aa][Tt][Ee][Ll]"
        for match in finditer(p_do,text):
            hodnota_do=match.group()
            pozice_do=int(match.span()[0])
        if pozice_od<pozice_do:
            poradi=[hodnota_od,hodnota_do]
        else:
            poradi=[hodnota_do,hodnota_od]

        p_ico= "[Ii][ČčCc]\s{0,10000}[:-]\s{0,10000}\d+|[Ii][ČčCc]\s{0,10000}\s{0,10000}\d+"
        index_ico=0
        for match in finditer(p_ico,text):
            hodnota_ico=match.group()
            pozice_ico=int(match.span()[0])
            if index_ico<2:
                faktura_dict[poradi[index_ico]]=re.findall(r'\d+', hodnota_ico)[0]
            index_ico+=1
    except:
        faktura_dict["ODBERATEL"] ="unknow"
        faktura_dict["DODAVATEL"] = "unknow"


        # castka#
    try:
        p_castka= "[Cc][Ee][Ll][Kk][Ee][Mm]\s{0,10000}[Kk]\D+\d+\s{0,10000}\d{3}[,.]\d{2}\s{0,10000}[Cc][Zz][Kk]|[Cc][Ee][Ll][Kk][Ee][Mm]\s{0,10000}\D+\d+\s{0,10000}\d{3}[,.]\d{2}\s{0,10000}[Kk][CcČč]"
        vysledek=re.findall(p_castka,text)
        suma=re.findall("[-\d]+",vysledek[0])
        castka="".join(suma[:-1])+"."+str(suma[-1])
        faktura_dict["Castka"]=castka
    except:
        faktura_dict["Castka"] = "unknow"

    return(faktura_dict)    
    
        
        

# faktura_info=create_pattern(text)
# print(faktura_info)
     