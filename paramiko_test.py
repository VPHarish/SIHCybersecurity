import paramiko
import streamlit as st
import pandas as pd
import numpy as np


ssh_client =paramiko.SSHClient()
st.set_page_config(page_title="CIS Benchmark-CentOS", layout="wide")


def color_fail(value):
    return f"background-color: red;" if value in "  Fail  " else None

def exec_cis_script(ip_addr, port, user, password):
    
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_addr,port=port,username=user,password=password)
    stdin,stdout,stderr=ssh_client.exec_command("python /home/vp/cis-benchmarks-audit/cis_audit.py")
    st.write("Output: ")
    for i in stdout.readlines():
        st.write(i)
        print(i)
        if not len([x for x in i.split(" ") if x]) <= 5:
            df2 = pd.DataFrame([[x for x in i.split("  ") if x]], columns=("ID", "Desc", "Level", "Result", "Time"))
            my_table.add_rows(df2)
    st.write("Error: ")
    st.write(stderr.readlines())

st.title("CIS Benchmark - CentOS")

st.markdown(f'''This page allows you to execute our automated CIS benchmark, customised for CentOS. 
        For more information on CIS Benchmark for CentOS, visit: 
            <a href="https://www.cisecurity.org/benchmark/centos_linux">CentOS</a>''',
        unsafe_allow_html=True)

with st.form(key='my_form'):
    ip_addr = st.text_input(label="Enter IP address: ")
    port = st.text_input(label="Enter port: ")
    username = st.text_input(label="Enter username: ")
    password = st.text_input(label="Enter password: " ,type="password")
    submit_button = st.form_submit_button(label='Submit')

df1 = pd.DataFrame(
    [["ID", "Desc", "Level", "Result", "Time"]], columns=("ID", "Desc", "Level", "Result", "Time")
)

my_table = st.dataframe(df1, width=1600, hide_index=True)


if submit_button:
    print("Submited")
    exec_cis_script(ip_addr, port, username, password)