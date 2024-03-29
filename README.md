
# Coniunctum
- ### A simple cryptocurrency / blockchain Python project. Based on proof-of-work and public-key cryptography.
Made to open up blockchain technology to newcomers in the developing world.

- #### Whitepaper available here : [Coniunctum.pdf](https://alainmgz.github.io/Coniunctum/Coniunctum.pdf)
- #### Detailed installation and usage instructions [here](https://github.com/AlainMgz/Coniunctum/wiki)
 - ### Build the client with Nix
   - Requirements
     - If your client is going to be a node or a miner, you need a static IP address. Simple wallets don't need a static IP. 
     - If you don't have `nix` installed, install it with `curl -L https://nixos.org/nix/install | sh`
     - Verify the installation with `nix --version`, it should output something like `nix (Nix) 2.3.10`

   - Choose a directory to clone the Coniunctum repo, and clone it using `git clone https://github.com/AlainMgz/Coniunctum.git`
   - Enter the cloned directory with `cd Coniunctum`
   - Modify the `source_data/ip_file.json` file and there put the local IP of your machine (if it's the first time running Coniunctum on your local network) or the IP of an other node running in your local network. (more details in the [wiki](https://github.com/AlainMgz/Coniunctum/wiki))
   - Run `nix-build` to install the client
   - Run `nix-shell` to enter the nix environment
   - Now the `coniunctum` command should be available, run it to start the client

 - ### Build the client from source
   - Requirements : 
     - Install Python 3+ (or make sure you have it, `python3 -V` should output something similar to `Python 3.9.2`, this program is using `python3` and not `python`)
     - Download the latest verison of the client [here](https://github.com/AlainMgz/Coniunctum/releases) 
     - Install the needed pip packages with : `python3 -m pip install -r requirements.txt`
     - If your client is going to be a node or a miner, you need a static IP address. Simple wallets don't need a static IP.
  
   - [ Only for the first client you install : ] For now the client only works on local networks so before installing it for the first time on your network, you need to modify the `source_data/ip_file.json` and put the IP address of your first client. It will generate a genesis block and an installation archive (when you run the client for the first time) customized for your network that you need to install the client on other machines of your network (for which you will not need to modify the `source_data/ip_file.json` file). (more details in the [wiki](https://github.com/AlainMgz/Coniunctum/wiki))
   - Run the client with `python3 coniunctum.py`.
 - If you have trouble, please contact me I will be happy to help. If you find a bug or problem please report it, it helps a lot. And obviously contributions are open :)
- #### Contact : 
  - Email : airwaks98701@protonmail.ch
  - Twitter : @adotmgz

- #### Donations : 
  
  - Bitcoin BTC : bc1qp5yf67fq59cvkj00dsuh94usgvtr7ptte2q893
  - Cardano ADA : addr1qxhcw33f7j9tppxr2dpfpnrz76laddly4pahks5pcpp5yzl7wqt86frzq7ztcupgzwrt5f9w97v3t87v4rl6uxztkjuqwws8e9


                          

