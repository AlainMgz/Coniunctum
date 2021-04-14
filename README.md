
# Coniunctum
- A simple cryptocurrency / blockchain Python project. Based on proof-of-work and public-key cryptography.
Made to open up blockchain technology to newcomers in the developing world.

- Whitepaper available here : [Coniunctum.pdf](https://github.com/AlainMgz/Coniunctum/files/6313872/Coniunctum.pdf)
- Detailed installation and usage instructions [here](https://github.com/AlainMgz/Coniunctum/wiki)

- Install Instructions (works on Linux and Windows, should also on Mac but not tested. Also works on Android using Termux) :
  - Requirements : 
    - Install Python 3+ (or make sure you have it, `python3 -V` should output something similar to `Python 3.9.2`, this program is using `python3` and not `python`)
    - Download the latest verison of the client [here](https://github.com/AlainMgz/Coniunctum/releases) 
    - Install the needed pip packages with : `python3 -m pip install -r requirements.txt`
    - If your client is going to be a node or a miner, you need a static IP address. Simple wallets don't need a static IP.
  
  - [ Only for the first client you install : ] For now the client only works on local networks so before installing it for the first time on your network, you need to modify the `source_data/ip_file.json` and put the IP address of your first client. It will generate a genesis block and an installation archive (when you run the client for the first time) customized for your network that you need to install the client on other machines of your network (for which you will not need to modify the `source_data/ip_file.json` file).
  - Run the client with `python3 coniunctum.py`.
  - If you have trouble, please contact me I will be happy to help. If you find a bug or problem please report it, it helps a lot. And obviously contributions are open :)
- Contact : 
  - Email : airwaks98701@protonmail.ch
  - Twitter : @adotmgz

- Donations : 
  
  - Bitcoin BTC : bc1qp5yf67fq59cvkj00dsuh94usgvtr7ptte2q893
  - Cardano ADA : addr1qxhcw33f7j9tppxr2dpfpnrz76laddly4pahks5pcpp5yzl7wqt86frzq7ztcupgzwrt5f9w97v3t87v4rl6uxztkjuqwws8e9


                          

