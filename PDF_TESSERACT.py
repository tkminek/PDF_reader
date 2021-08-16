import fitz
import cv2 
import pytesseract
import numpy as np
from pytesseract import Output
import TEMP as temp

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def pdf_page_number(name):
    doc = fitz.open(open("PDF/"+str(name)+".pdf"))
    number=doc.pageCount
    return(number)


def create_jpg(name,index):
    pdffile = "PDF/"+str(name)+".pdf"
    doc = fitz.open(pdffile)
    page = doc.loadPage(index)  # number of page
    pix = page.getPixmap(matrix=fitz.Matrix(300/72, 300/72))
    output = "PDF/"+str(name)+".jpg"
    pix.writePNG(output)
    return(output)


def uprava_jpg(jpg):
    image = cv2.imread(jpg)    
    image = cv2.resize(image, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.erode(image, kernel, iterations=1)
    image=cv2.threshold(cv2.GaussianBlur(image, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    return(image)

def vypis_txt(text,name):
    file_text=open("PDF/"+str(name)+".txt","a+",encoding='utf-8')
    file_text.write(text)
    file_text.close()


def prijata_faktura_txt(name,start,end):
    open("PDF/"+str(name)+".txt","w",encoding='utf-8').close()    
    for index in range(start,end):
        jpg=create_jpg(name,index)
        jpg_upravene=uprava_jpg(jpg)
        my_config=r'--oem 3 --psm 6 '
        text = pytesseract.image_to_string(jpg_upravene,lang='ces',config=my_config)
        #only for spyder start#
        arr = text.split('\n')[0:-1]
        text = '\n'.join(arr)
        #only for spyder end#
        vypis_txt(text,name)
        print("---------------")
        print(f"TXT file - Page number: {index} is DONE")




def whole_info(data):
    facture_number=temp.cislo_faktury(data)
    datums_vystaveni_info=temp.datums_vystaveni(data)
    datums_splatnosti_info=temp.datums_splatnosti(data)
    datums_zdaneni_info=temp.datums_zdaneni(data)
    ico_info=temp.odberatel_dodavatel(data)
    cost=temp.castka(data)
    whole_info_dict={**facture_number, **datums_vystaveni_info,**datums_splatnosti_info,**datums_zdaneni_info,**ico_info,**cost}
    return(whole_info_dict)


def main():
    #name="faktura1"
    name="faktury_prijate"
    end=pdf_page_number(name)
    start=2
    end=4
    prijata_faktura_txt(name,start,end)
    file_text = open("PDF/" + str(name) + ".txt", "r", encoding='utf-8')
    data = file_text.read()
    result=whole_info(data)
    print(result)





if __name__ == '__main__':
    main()