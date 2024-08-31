import paramiko
import streamlit as st
import pandas as pd
import numpy as np


ssh_client =paramiko.SSHClient()
st.set_page_config(page_title="CIS Benchmark-CentOS", layout="wide")


def color_fail(value):
    return f"background-color: red;" if value in "  Fail  " else None


def send_audit_script(ip_addr, port, user, password):
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_addr,port=port,username=user,password=password)
    sftp = ssh_client.open_sftp()
    sftp.put('E:\Projects\SIH 24\CIS Benchmark\Code\SIHCybersecurity\scripts\centos.zip', '/tmp/centos.zip')
    ssh_client.exec_command("unzip -d /tmp /tmp/centos.zip")
    # stdin,stdout,stderr=ssh_client.exec_command("")


def exec_cis_script():
    
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ip_addr,port=port,username=username,password=password)
    stdin,stdout,stderr=ssh_client.exec_command("python /tmp/cis-benchmarks-audit-main/cis_audit.py")
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
    save_button = st.form_submit_button(label='Save')
    send_button = st.form_submit_button(label='Send Audit Script')
    run_button = st.form_submit_button(label="Run Audit Script")


# actions_container = st.container(border=True)

# with actions_container:
#     st.header("Step 1: Send audit script for evaluation")
#     st.button(label='Send Audit Script', type='primary')
#     st.markdown("#")
#     st.header("Step 2: Run audit script on target machine")
#     st.button(label='Run Audit Script', type='primary', on_click=send_audit_script)


logs_container = st.container(border=True)

logs_container.header("Logs:")


df1 = pd.DataFrame(
    [["ID", "Desc", "Level", "Result", "Time"]], columns=("ID", "Desc", "Level", "Result", "Time")
)

my_table = st.dataframe(df1, width=1600, hide_index=True)


if run_button:
    print("Submited")
    exec_cis_script()

if send_button:
    send_audit_script(ip_addr, port, username, password)