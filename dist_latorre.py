try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os
import pandas as pd
from datetime import datetime

contenido = os.listdir('.\imagenes')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
completo=[pytesseract.image_to_string(Image.open('./imagenes/'+i)).split('\n') for i in contenido]

n_fact=[]
for k in range(len(completo)):
    for i,j in enumerate(completo[k]):
        if('No.' in j):
            linea_factura=completo[k][i].split()
            for line in reversed(linea_factura):
                try:
                    float(line)
                    n_fact.append(int(line))
                    break
                except:
                    print('Not')
                    continue
            break
    if (k>len(n_fact)-1):
        n_fact.append(0)

fecha=[]
for k in range(len(completo)):
    for i,j in enumerate(completo[k]):
        if('/202' in j):
            linea_fecha=completo[k][i].split()
            for line in reversed(linea_fecha):
                print(line)
                try:
                    pd.to_datetime(line)
                    fecha.append(pd.to_datetime(line))
                    break
                except:
                    continue
            break
    if (k>(len(fecha)-1)):
            fecha.append('None')

linea_art=[]
for k in range(len(completo)):
    for i,j in enumerate(completo[k]):
        if ('Descrip' in j) or ('Precio' in j):
            linea_art.append(i)
            print(i)
            break
    if (k>(len(linea_art)-1)):
            linea_art.append(len(completo[k]))
            print(len(completo[k]))

linea_final=[]
for k in range(len(completo)):
    for i,j in enumerate(completo[k]):
        if ('Observ' in j) or ('bruto' in j):
            linea_final.append(i)
            break
    if (k>(len(linea_final)-1)):
        linea_final.append(len(completo[k]))
        print(len(completo[k]))

dffinal=pd.DataFrame(columns=["codigo","cantidad","producto","desc","precio","iva_porc",
                "precio_iva","iva","inc","subt","Fecha","N_factura"])
for h in range(len(completo)):    
    dicprod = {"codigo":[],"cantidad":[],"producto":[],"desc":[],"precio":[],
               "iva_porc":[],"precio_iva":[],"iva":[],"inc":[],"subt":[],"Fecha":[],"N_factura":[]}
    for k in range(linea_art[h]+1,linea_final[h]):
        data=completo[h][k].split()
        print(data)
        if (len(data)>9):
            dicprod['subt'].append(data.pop())
            dicprod['inc'].append(data.pop())
            dicprod['iva'].append(data.pop())
            dicprod['precio_iva'].append(data.pop())
            dicprod['iva_porc'].append(data.pop())
            dicprod['precio'].append(data.pop())
            dicprod['desc'].append(data.pop())
            data[2]=data[2].replace(',','.')
            try:
                float(data[2])
                data.pop(0)
                dicprod['codigo'].append(data.pop(0))
                dicprod['cantidad'].append(data.pop(0))
            except:
                dicprod['codigo'].append(data.pop(0))
                dicprod['cantidad'].append(data.pop(0))
            dicprod['producto'].append(" ".join(data))
            dicprod['Fecha'].append(fecha[h])
            dicprod['N_factura'].append(n_fact[h])
    df=pd.DataFrame(dicprod)
    dffinal=pd.concat([dffinal,df])

dffinal.to_excel('Resultados/Resultado_latorre.xlsx')

                    
            