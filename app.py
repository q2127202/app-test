#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import streamlit.components.v1 as components
import codecs
import pandas as pd
import numpy as np
from gurobipy import *
import os



# In[ ]:



def  main():
    """a new app with Streamlit"""
    
    menu = ["Home","データ","モデル","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    
    if choice == "データ":
        st.subheader("データ説明")
        df = pd.read_csv ("airland1.txt")
        st.write(df)
        st.write('The format of these data files is:')
        st.write('number of planes (p), freeze time')
        st.write('for each plane i (i=1,...,p):')
        st.write('appearance time, earliest landing time, target landing time,latest landing time, penalty cost per unit of time for landing before target, penalty cost per unit of time for landing after target')
        st.write('for each plane j (j=1,...p): separation time required after i lands before j can land')
        
    elif choice == "モデル":
        #st.subheader("モデル定式化")
        #st.write('P be the number of planes')
        #st.write('Ei be the earliest landing time for plane i (i=1,...,P)')
        #st.write('Li be the latest landing time for plane i (i=1,...,P)')
        #st.write('Ti be the target (preferred) landing time for plane i (i=1,...,P)')
        #st.write('Sij be the required separation time (≥ 0) between plane i landing and plane j landing')
        #st.write('(where plane i lands before plane j), i=1,...,P; j=1,...,P; i≠j')
        #st.write('gi be the penalty cost (≥ 0) per unit of time for landing before the target time Ti for plane i (i=1,...,P)')
        #st.write('hi be the penalty cost (≥ 0) per unit of time for landing after the target time Ti for plane i (i=1,...,P)')
        #st.write('xi =the landing time for plane i (i=1,...,P)')
        #st.write('αi =how soon plane i (i=1,...,P) lands before Ti')
        #st.write('βi =how soon plane i (i=1,...,P) lands after Ti')
        #st.write('δij = 1 if plane i lands before plane j (i=1,...,P; j=1,...,P; i≠j) = 0 otherwise')
       
        from PIL import Image
        image2 = Image.open('mode3.PNG')
        st.image(image2,use_column_width=True)    
        image = Image.open('mode1.PNG')
        st.image(image,use_column_width=True)
        image1 = Image.open('mode2.PNG')
        st.image(image1,use_column_width=True)
        
            
    elif choice == "About":
        st.subheader("About App")
        st.write('張春来')
        st.write('東京海洋大学大学院　サプライチェーン最適化　数理最適化　')
        st.write('email: anlian0482@gmail.com')
    else:
        st.subheader("Home")
        html_temp = """
        <div style="background-color:royalblue;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">Multi runway aircraft-Landing-Scheduling</h1>
        </div>
        """
        
        components.html(html_temp)
        

      
       
        uploaded_file = st.file_uploader('1. ファイルをアップロードする。', type='txt')
        
        check = st.checkbox('サンプルデータを使う', value=False)
        
        if uploaded_file is not None:
            
            if 'push1' not in st.session_state:
                st.session_state.push1 = False
                
            button1 = st.button(' ファイル読み込み')
            
            if button1:
                st.session_state.push1 = True
        if (uploaded_file is not None and st.session_state.push1) or check:
            
            if uploaded_file is not None and st.session_state.push1:
                df = pd.read_csv(uploaded_file)
                if button1:
                    st.write(df)
                df.to_csv('fname.txt', sep='\t',index=False)
                fn = "fname.txt"
                date=open(fn,"r",)
                lines = date.readlines()
                num_planes=int(lines[0].split()[0])
                freeze_time=int(lines[0].split()[1])
                flight_details=np.empty([num_planes,6],dtype=float)
                sep_time=np.empty([num_planes,num_planes],dtype=int)
                st.write('飛行機数：')
                if button1:
                    st.write(num_planes)
                s=''
                for line in lines[1:]:
                    s=s+line
                s=s.split()
                flag=0
                count=0
                for items in [s[x:x+6+num_planes] for x in range(0,len(s),num_planes+6)]:
                    flight_details[count]=[float(x) for x in items[:6]]
                    sep_time[count]=[int(x) for x in items[6:]]
                    count=count+1
                taisuu = st.selectbox('2. ルート数を選択してください',('１','2'))
                runways = int(taisuu)
                model=Model(" Schedule")
                M=999999
                ai={}
                for i in np.arange(1,num_planes+1):
                    ai[i]=flight_details[i-1,5]
                bi={}
                for i in np.arange(1,num_planes+1):
                    bi[i]=flight_details[i-1,4]
                x={}
                for i in np.arange(1,num_planes+1):
                    x[i]=0
                del_={}
                for i in np.arange(1,num_planes+1):
                    for j in np.arange(1,num_planes+1):
                        del_[i,j]=0
                q_={}
                for i in np.arange(1,num_planes+1):
                    for j in np.arange(1,num_planes+1):
                        q_[i,j]=0
                y_={}
                for i in np.arange(1,num_planes+1):
                    for r in np.arange(1,runways+1):
                        y_[i,r]=0
                z_p=model.addVars(ai.keys(),lb=0,ub=GRB.INFINITY,obj=ai,vtype=GRB.CONTINUOUS,name="z_p")
                # landing after the target time
                z_n=model.addVars(bi.keys(),lb=0,ub=GRB.INFINITY,obj=bi,vtype=GRB.CONTINUOUS,name="z_n")
                #Real landing time
                x=model.addVars(x.keys(),lb=0,ub=GRB.INFINITY,obj=x,vtype=GRB.CONTINUOUS,name="x") 
                
                d=model.addVars(del_.keys(),lb=0,ub=1,obj=del_,vtype=GRB.BINARY,name="d")

                y=model.addVars(y_.keys(),lb=0,ub=1,obj=y_,vtype=GRB.BINARY,name="y")
                
                model.addConstrs((d[i,j]+d[j,i]>=y[i,r]+y[j,r]-1 for r in np.arange(1,runways+1)for i in np.arange(1,num_planes+1)                   for j in np.arange(1,num_planes+1) if j!=i),name="~")
                #the time difference between Ti and xi
                model.addConstrs((z_n[i]>=x[i]-flight_details[i-1,2] for i in np.arange(1,num_planes+1)),name="+")
                model.addConstrs((z_p[i]>=flight_details[i-1,2]-x[i] for i in np.arange(1,num_planes+1)),name="-")
                #each plane lands within its time window
                model.addConstrs((x[i]>=flight_details[i-1,1] for i in np.arange(1,num_planes+1)),name="after earliest  time")
                model.addConstrs((x[i]<=flight_details[i-1,3] for i in np.arange(1,num_planes+1)),name=" before latest time")
                model.addConstrs((x[j]>=x[i]+sep_time[i-1,j-1]- M*(1-d[i,j]) for i in np.arange(1,num_planes+1) for j in np.arange(1,num_planes+1) if j!=i),name="Clearance")

                #model.addConstrs((q[i,j]==q[j,i] for i in np.arange(1,num_planes +1) for j in np.arange(1,num_planes+1) if j!=i),name="$")

                model.addConstrs((quicksum(y[i,r] for r in np.arange(1,runways+1))==1 for i in np.arange(1,num_planes+1)),name="Land at only 1 runway")

                #model.addConstrs((q[i,j]>=y[i,r]+y[j,r]-1 for r in np.arange(1,runways+1) for j in np.arange(1,num_planes+1) for i in np.arange(1,num_planes+1) if j!=i),name="enforcing constraint")
        
                model.optimize()
                button2 = st.button('最適化')
                if button2:
                    for i in np.arange(1,num_planes+1):
                         for r in np.arange(1,runways+1):
                                if model.getVarByName("y["+str(i)+","+str(r)+"]").X==1:
                                     st.write('%s %g %s %g' % (' 飛行機'+str(i)+'着陸時間 '" = ", model.getVarByName("x["+str(i)+"]").X, ' ルート= ',r))
          
            if check:
                df = pd.read_csv ("airland1.txt")

                st.write(df)
            
                fname = "airland1.txt"
                date= open(fname,"r")
                lines = date.readlines()
                num_planes=int(lines[0].split()[0])
                freeze_time=int(lines[0].split()[1])
                flight_details=np.empty([num_planes,6],dtype=float)
                sep_time=np.empty([num_planes,num_planes],dtype=int)
                st.write('飛行機数：')
                st.write(num_planes)
                
                s=''
                for line in lines[1:]:
                    s=s+line
                s=s.split()
                flag=0
                count=0
                for items in [s[x:x+6+num_planes] for x in range(0,len(s),num_planes+6)]:
                    flight_details[count]=[float(x) for x in items[:6]]
                    sep_time[count]=[int(x) for x in items[6:]]
                    count=count+1
       
                taisuu = st.selectbox('2. ルート数を選択してください',('１','2'))
                runways = int(taisuu)
                model=Model(" Schedule")
                M=999999
                ai={}
                for i in np.arange(1,num_planes+1):
                    ai[i]=flight_details[i-1,5]
                bi={}
                for i in np.arange(1,num_planes+1):
                    bi[i]=flight_details[i-1,4]
                x={}
                for i in np.arange(1,num_planes+1):
                    x[i]=0
                del_={}
                for i in np.arange(1,num_planes+1):
                    for j in np.arange(1,num_planes+1):
                        del_[i,j]=0
                q_={}
                for i in np.arange(1,num_planes+1):
                    for j in np.arange(1,num_planes+1):
                        q_[i,j]=0
                y_={}
                for i in np.arange(1,num_planes+1):
                    for r in np.arange(1,runways+1):
                        y_[i,r]=0
                z_p=model.addVars(ai.keys(),lb=0,ub=GRB.INFINITY,obj=ai,vtype=GRB.CONTINUOUS,name="z_p")
                # landing after the target time
                z_n=model.addVars(bi.keys(),lb=0,ub=GRB.INFINITY,obj=bi,vtype=GRB.CONTINUOUS,name="z_n")
                #Real landing time
                x=model.addVars(x.keys(),lb=0,ub=GRB.INFINITY,obj=x,vtype=GRB.CONTINUOUS,name="x") 
                
                d=model.addVars(del_.keys(),lb=0,ub=1,obj=del_,vtype=GRB.BINARY,name="d")

                y=model.addVars(y_.keys(),lb=0,ub=1,obj=y_,vtype=GRB.BINARY,name="y")
                
                model.addConstrs((d[i,j]+d[j,i]>=y[i,r]+y[j,r]-1 for r in np.arange(1,runways+1)for i in np.arange(1,num_planes+1)                   for j in np.arange(1,num_planes+1) if j!=i),name="~")
                #the time difference between Ti and xi
                model.addConstrs((z_n[i]>=x[i]-flight_details[i-1,2] for i in np.arange(1,num_planes+1)),name="+")
                model.addConstrs((z_p[i]>=flight_details[i-1,2]-x[i] for i in np.arange(1,num_planes+1)),name="-")
                #each plane lands within its time window
                model.addConstrs((x[i]>=flight_details[i-1,1] for i in np.arange(1,num_planes+1)),name="after earliest  time")
                model.addConstrs((x[i]<=flight_details[i-1,3] for i in np.arange(1,num_planes+1)),name=" before latest time")
                model.addConstrs((x[j]>=x[i]+sep_time[i-1,j-1]- M*(1-d[i,j]) for i in np.arange(1,num_planes+1) for j in np.arange(1,num_planes+1) if j!=i),name="Clearance")

                #model.addConstrs((q[i,j]==q[j,i] for i in np.arange(1,num_planes +1) for j in np.arange(1,num_planes+1) if j!=i),name="$")

                model.addConstrs((quicksum(y[i,r] for r in np.arange(1,runways+1))==1 for i in np.arange(1,num_planes+1)),name="Land at only 1 runway")

                #model.addConstrs((q[i,j]>=y[i,r]+y[j,r]-1 for r in np.arange(1,runways+1) for j in np.arange(1,num_planes+1) for i in np.arange(1,num_planes+1) if j!=i),name="enforcing constraint")
        
                model.optimize()
                button2 = st.button('最適化')
                if button2:
                    for i in np.arange(1,num_planes+1):
                         for r in np.arange(1,runways+1):
                                if model.getVarByName("y["+str(i)+","+str(r)+"]").X==1:
                                     st.write('%s %g %s %g' % (' 飛行機'+str(i)+'着陸時間 '" = ", model.getVarByName("x["+str(i)+"]").X, ' ルート= ',r))
                

            
      
            
       
                
                
                
        
if __name__ == '__main__':
    main()






