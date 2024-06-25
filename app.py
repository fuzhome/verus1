import streamlit as st
import subprocess
import os

def download_and_extract_nheqminer():
    if not os.path.exists('./nheqminer'):
        download_command = "wget https://github.com/VerusCoin/nheqminer/releases/download/v0.8.2/nheqminer-Linux-v0.8.2.tgz"
        extract_command = "tar -xzvf nheqminer-Linux-v0.8.2.tgz && rm nheqminer-Linux-v0.8.2.tgz && tar -xzvf nheqminer-Linux-v0.8.2.tar.gz"
        
        st.info("Downloading nheqminer...")
        subprocess.run(download_command, shell=True)
        st.info("Extracting nheqminer...")
        subprocess.run(extract_command, shell=True)
        st.success("nheqminer downloaded and extracted successfully!")
    else:
        st.warning("nheqminer is already downloaded and extracted.")

def start_mining():
    command = "./nheqminer/nheqminer -v -l stratum+tcp://na.luckpool.net:3956 -u RWmpwxvJkhchBxTc6hzkxNDLiK1VmGnvKz.hard_worker2 -p x -t 16"
    st.info(f"Running command: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

st.title("nheqminer GUI")

if st.button("Download and Extract nheqminer"):
    download_and_extract_nheqminer()

if st.button("Start Mining"):
    process = start_mining()
    st.success("Mining started!")

if 'process' in locals() and process.poll() is None:
    st.text("Miner Output:")
    for line in iter(process.stdout.readline, ''):
        st.text(line.strip())
