from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import avg, sum, col,lit
import streamlit as st
import pandas as pd

st.set_page_config(
     page_title="Environment Data Atlas",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://developers.snowflake.com',
         'About': "This is an *extremely* cool app powered by Snowpark for Python, Streamlit, and Snowflake Data Marketplace"
     }
 )

def create_session_object():
    os.environ["snowpark_account"] = 'keboola' #Dont change
    os.environ["snowpark_user"] = 'SAPI_WORKSPACE_858004958'
    os.environ["snowpark_password"] = 'dfdsfasdfs'
    os.environ["snowpark_warehouse"] = 'KEBOOLA_PROD'
    os.environ["snowpark_database"] = 'SAPI_7322'
    os.environ["snowpark_schema"] = 'WORKSPACE_858004958'

    connection_parameters = {
        "account": os.environ["snowpark_account"],
        "user": os.environ["snowpark_user"],
        "password": os.environ["snowpark_password"],
        "warehouse": os.environ["snowpark_warehouse"],
        "database": os.environ["snowpark_database"],
        "schema": os.environ["snowpark_schema"]
    }    
    session = Session.builder.configs(connection_parameters).create()
    print(session.sql('select current_warehouse(), current_database(), current_schema()').collect())
    return session

def load_data():
    telco_sample = session.table('TELCO_DATASET').sample(n = 20000)
    telco_sample.write.mode('overwrite').saveAsTable('TELCO_TRAINING_DATASET')
    df=telco_sample.to_pandas()

    # Add header and a subheader
    st.header("The Snowpark test")
    st.subheader("Powered by Snowpark for Python | Made with Streamlit")

    # Use columns to display the three dataframes side-by-side along with their headers
    col1, col2 = st.columns(2)
    with st.container():
        with col1:
            st.subheader('Table Telco dataset')
            st.dataframe(df)
        with col2:
            st.subheader('And oncem ore')
            st.dataframe(df)

    # Display an interactive bar chart
    with st.container():
        st.subheader('Random subheader')
        with st.expander(""):
            threshold = st.number_input(label='Threshold',min_value=5000, value=20000, step=5000)
            dfx = telco_sample.filter(col("TOTALCHARGES") > threshold).to_pandas()
            st.bar_chart(data=dfx.set_index('CUSTOMERID'), width=850, height=500, use_container_width=True)

if __name__ == "__main__":
    session = create_session_object()
    load_data(session)
