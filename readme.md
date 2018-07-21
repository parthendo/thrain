# Secure Text Transfer Using Diffie-Hellman Key Exchange Based On Cloud

Security on cloud has been a hot topic. Even the tech giants like google and amazon spend hefty capital to strengthen their security. We, here have implemented a secure text transfer using diffie-hellman key exchange algorithm.

## Diffie-Hellman Key Exchange

One of the brute approaches for secure transfer can be that *user A* can encrypt the using a key and later the key could be shared with *user B*. This approach can work up to an extent but it always has a risk of **third-party eavesdroppping**. We needed a system in which two users, without knowing the secret key, can independently generate same key at both ends. This key could later be used to encrypt and decrypt the text. The diffie-hellman key exchange algorithm comes into picture.</br></br>
Diffie–Hellman key exchange (DH) is a method of securely exchanging cryptographic keys over a
public channel and was one of the first public-key protocols named after Whitfield Diffie and
Martin Hellman. DH is one of the earliest practical examples of public key exchange
implemented within the field of cryptography.</br>
In public key cryptosystem, enciphering and deciphering are governed by distinct keys, E and D,
such that computing D from E is computationally infeasible (e.g., requiring more than 10^100
instructions). The enciphering key E can thus be publicly disclosed without compromising the
deciphering key D. This was the main ideology behind Diffie-Hellman Key Exchange Protocol.
Each user of the network can, therefore, place his enciphering key in a public directory. This
enables any user of the system to send a message to any other user enciphered in such a way that
only the intended receiver can decipher it. As such, a public key cryptosystem is a multiple access
cipher. A private conversation can therefore be held between any two individuals regardless of
whether they have ever communicated before. Each one sends messages to the other enciphered in
the receiver’s public enciphering key and deciphers the messages he receives using his own secret
deciphering key.

### Working example of Diffie-Hellman 

*p* is a prime number </br>
*g* is a primitive root modulo of *p*

* Alice and Bob agree to use a modulus p = 23 and base g = 5
* Alice gets her private key (key which she should not share with anyone) generated as 4.
* Thus, public key generated for Alice shall be 5^4 %23 = 625%23 = 4
* Bob gets his private key (key which he should not share with anyone) generated as 3.
* Thus, public key generated for Bob shall be 5^3 %23 = 125%23 = 10
* Now, Alice gets the public key of Bob and generates a secret key. i.e.
(public key of Bob ^ Private Key of Alice) mod p
=> (10^4 ) % 23 => 10000 % 23 => 18
* On the other side, Bob also uses a similar method to generate a secret key i.e.
(public key of Alice ^ Private Key of Bob) mod p
=> (4^3 ) % 23 => 64 % 23 => 18

##### Dependencies
```
python-flask
hashlib
pycrypto
secretsharing
tkinter
webbrowser
```
## Code Explanation

This implementation can be explained in two parts
* stand-alone-application
* web-application

### stand-alone-application

![stand-alone-application](https://github.com/parthendo/thrain/tree/master/dump/images/GUI.PNG)</br>

* This portion deals with encryption and decryption of file
* The file is encrypted using AES algorithm
* *Menu* option also helps to toggle the menu to upload and download files</br></br>

**src/stand-alone-application/DH.py**:  This file deals with generating keys using diffie-hellman. It generates three keys:</br>
* Private Key
* Public Key
* Secret Key (used for encryption and decryption)
**src/stand-alone-application/ENCDEC.py**: This file is used for encoding and decoding using AES algorithm.</br>
**src/stand-alone-application/thrain.py**: This file acts as a mediator and connect the main program with other code files.</br>
**src/stand-alone-application/main.py**: This file deals with the GUI. It is the main file [yeah, trust me!].</br>

### web-application
![web-application](https://github.com/parthendo/thrain/tree/master/dump/images/home.PNG)</br>

Once file is encrypted it has to be uploaded on an online directory. Another directory is needed where public-key of all the users is stored. Thus, we built an online directory and hosted it on cloud. The unique thing about hosting is that dynamic files are being generated while adding a new user or uploading a text file. Thus, we needed a cloud service which could run the program and incorporate the dynamic files. We tried free services like pivotal and heroku but then amazon AWS came to our rescue.</br>
**src/web-application/app.py** Contains the website in **python-flask** which acts like a directory.

### Hosting on AWS

* fork this repository
* create an amazon EC2 instance.
* Select and create **Amazon Linux AMI 2018.03.0 (HVM), SSD Volume Type**
* While creating the machine, toggle to menu *Configure Security Group* menu.
* Here, enable port SSH, HTTP, RDP and in port, change *Source* to **Anywhere**
* Download and keep the **publicKeyPair file**
* Install *putty* and *puttygen*
* Open 



