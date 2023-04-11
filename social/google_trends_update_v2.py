

import os
os.getcwd()
import sys
sys.path.append('C:\\Users\\danie\\Documents\\GitHub\\pytrends\\pytrends')


#importo los paquetes
from pytrends.request import TrendReq
import pandas as pd
from tqdm import tqdm
import datetime as dt
import time


#country_dic = {"AR":"Argentina", "BR": "Brazil", "CL":"Chile","MX":"Mexico",
#                "DO":"Dominican Republic","SV":"El Salvador","PA":"Panama","UY":"Uruguay", "CO":"Colombia",  
#                "NL":"Netherlands", "FR":"France","DE":"Germany", "US":"United States"}


country_dic = {"AR":"Argentina", "BR": "Brazil", "CL":"Chile","MX":"Mexico",
                "DO":"Dominican Republic","SV":"El Salvador","PA":"Panama",
                "UY":"Uruguay", "CO":"Colombia"  }



paises = list(country_dic.keys())
Codigos = ["/m/01pmdg","/m/026t_c7", "/m/0k4j"]
Nombres= ["Autos electricos", "Autos Hibridos", "Autos"]

def QueryGTrnsd(codigo, nombre):
    pytrend = TrendReq(hl='en-GB', tz=360)

    ##################################################


    #ACA ACTUALIZAR LAS FECHAS A LO ULTIMO USADO

    """
    Empieza a hacer la consulta:
    1.) Crea un dataframe base con el primer país en la lista con la infromación del pytrend.build_payload
    2.) Itera por cada país definido
    3.) Realiza las consultas respectivas
    4.) Crea un dataframe temporal con la infromación del pais i
    5.) Pega el dataset temporal y el dataset base para ir creando cada vez un dataset más grande
    """
    print(paises[0]) 
    #keywords = ["/m/0k4j"]
    keywords = [str(codigo)]
    pytrend.build_payload( kw_list=keywords, cat= str(47), timeframe= '2010-01-01 2022-12-31', geo= str(paises[0]))
    data = pytrend.interest_over_time()
    data["Country"] = str(paises[0])
    data = data.drop(labels=['isPartial'],axis='columns')

    for i in range(1,len(paises)):
        print(paises[i]) 
        #keywords =['/m/0k4j'] #usa el id para la busqueda global de "carros"
        keywords = [str(codigo)]
        # es el comando donde se le ingresan los parametros del query
        pytrend.build_payload( kw_list=keywords, cat= str(47), timeframe= '2010-01-01 2022-12-31', geo= str(paises[i]))
        # ejecuta el pytrend y hace la busqueda
        temp_data = pytrend.interest_over_time()
        """construye el dataframe con los resultados"""
        if not data.empty:
            temp_data = temp_data.drop(labels=['isPartial'],axis='columns')
            temp_data["Country"] = paises[i]
            data = pd.concat([data, temp_data], axis = 0)
        time.sleep(60)

    ##################################



    #for para cambiar el codigo pais por el pais real
    new_countries =[]
    for code in data["Country"]:
        new_country = country_dic[code]
        new_countries.append(new_country)

    data["Country"] = new_countries # reemplaza la columna de codigos con la nueva lista de paises en el dataframe
    data.columns = [str(nombre), "Country"] # renombra la columna con el topic_id 

    #############################


    data.reset_index(inplace = True)
    data["Month"] = data["date"].dt.to_period('M')
    data

    ############################

    data.to_csv("google_trends"+" "+str(nombre)+".csv")
    time.sleep(10)
    print("guardado")




#
Codigos = ["/m/01pmdg","/m/026t_c7", "/m/0k4j"]
Nombres= ["Autos electricos", "Autos Hibridos", "Autos"]



#EV = /m/01pmdg
#Hybrid = /m/026t_c7

#for i in tqdm(range(0,len(Nombres))):
#    print(Nombres[i])
#    QueryGTrnsd(Codigos[i], Nombres[i])
    
QueryGTrnsd(Codigos[2], Nombres[2])
    



