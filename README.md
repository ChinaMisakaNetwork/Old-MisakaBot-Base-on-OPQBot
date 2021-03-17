# CLIENT
This is the branch for the client of Misaka Network<br>
# Requirement
Windows: libmysql.dll<br>
Linux & MacOS: mysql installed within $PATH<br>
# Language
Programming Language: Pascal<br>
User Interface Language: English<br>
# Notes
The program connect to MySQL Server to get data<br>
The user data should be store in WebAdmin<br>
Details: <br>

| QQ | Priv | Pass |
|---------------------|----------------------------|--------------------------|
| Username in integer | Privilege in short/integer | SHA256(SHA256(Password)) |

# Privilege
The Privilege is present as a number between 0 to 7
and it can be split into 3 bit

| 4 | 2 | 1 |
|----------------|---------------------|----------------------|
| Admin Settings | Bot Log (Within QQ) | Bot Log (Without QQ) |
