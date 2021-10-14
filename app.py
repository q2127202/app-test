import streamlit as st
import pandas as pd
import codecs
#from pandas_profiling import ProfileReport

import streamlit.components.v1 as components
#from streamlit_pandas_profiling import st_profile_report

#import sweetviz as sv

#def st_display_sweetviz(report_html,width=1000,height=500):
    #report_file = codecs.open(report_html,'r')
    #page = report_file.read()
    #components.html(page,width=width,height=height,scrolling=True)
def  main():
    """a new app with Streamlit"""
    
    menu = ["Home","データ","Sweetviz","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    
    if choice == "データ":
        st.subheader("データを読む")
        date_file =st.file_uploader("Upload TXT",type=['txt'])
        if date_file is not None:
            df = pd.read_csv (date_file)
            st.dataframe(df)
            #profile = ProfileReport(df)
            #st_profile_report(profile)
        
    elif choice == "Sweetviz":
        st.subheader("Automated EDA with Sweetviz")
        #date_file =st.file_uploader("Upload TXT",type=['txt'])
        #if date_file is not None:
          #  df = pd.read_csv (date_file)
           # st.dataframe(df.head())
            
            #report = sv.analyze(df)
            #report.show_html()
            
            
    elif choice == "About":
        st.subheader("About App")
    else:
        st.subheader("Home")
        html_temp = """
        <div style="background-color:royalblue;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">Multi runway aircraft-Landing-Schedule</h1>
        </div>
        """
       # components.html("<p style='color:red;'> Streamlit component is awesome</p>")
       # components.html(html_temp)
        
        components.html("""
                <style>
                body, html {
                  height: 100%;
                  margin: 0;
                  font-family: Arial, Helvetica, sans-serif;
                }

                .hero-image {
                  background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                  url("https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1595181227896&di=f460192ade402f789fff9a4520e05106&imgtype=0&src=http%3A%2F%2Fdpic.tiankong.com%2Fdv%2Flj%2FQJ8315128614.jpg");
                  height: 100%;
                  background-position: center;
                  background-repeat: no-repeat;
                  background-size: cover;
                  position: relative;
                }

                .hero-text {
                  text-align: center;
                  position: absolute;
                  top: 50%;
                  left: 50%;
                  transform: translate(-50%, -50%);
                  color: white;
                }

                .hero-text button {
                  border: none;
                  outline: 0;
                  display: inline-block;
                  padding: 10px 25px;
                  color: black;
                  background-color: #ddd;
                  text-align: center;
                  cursor: pointer;
                }

                .hero-text button:hover {
                  background-color: #555;
                  color: white;
                }
                </style>
                </head>
                <body>

                <div class="hero-image">
                  <div class="hero-text">
                    <h1 style="font-size:30px">Multi runway aircraft-Landing-Schedule</h1>
                  
                    <button>strat</button>
                  </div>
                </div>

                <p>Page Content..</p>
        
               """)
        
        
if __name__ == '__main__':
    main()