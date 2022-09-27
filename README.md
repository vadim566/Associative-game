
# Association Game based TF-IDF Algorithem[MVP version]

This system will generate Phrase and will give you
4 stories that were ran up in the TF-IDF search Algorithem.
The user will get the score based on the answer precantage it 
got in the IDF-TF.

## Use case/Sequence diagram
1.User will aproach the the front end  and request a Game,
after proccessing the phrase it will return phrase with 4 answers based on idf-tf Algorithem
2.If the main Server was down the zookeeper will create a new leader that will recive all new request
3.The TF part of the IDF-TF is distrebuted between workers by simpale hashing.
![App Screenshot](https://i.ibb.co/wBVMc7m/UseCase.jpg)

## UML
When initlize the flask server it will be elected as a leader or worker,
if it was elected worker it will register its self as a leader in service discovery,
while its mention its ip.
After a get request from front end the request will passed to leader for genrate a phrase and 
it will generate a search based IDF-TF while the TF is distrebuted between all workers,
each worker return the TF result and the leader agrigating it into IDF Score and returning a JSON that 
hold the whole information for fatching the front end
![App Screenshot](https://i.ibb.co/54jM8PY/UML.png)

## Features
MVP
- The algo of TF-IDF is Disterbuted on zookeeper
- Based Flask
- Cross platform
Future Features
-picture that will be attached to each phrase
-cached picture based eachs story that will be searched by terms

## Installation

Install Zookeeper-
https://zookeeper.apache.org/

#### 1. Configure the server to:  localhost:2181
#### 2. Define how many workers will run with the system
#### 3. Under ./book/ create sub folder same number as #workers
#### 4. Recomanded that each folder will have sequential name 
#### 5. Spread Documents between all subfolder, at least one in each folder
#### 6. Create venv Install all python modules into venv
```shell
python -m venv venv
```
```
.\venv\Scripts\activate.bat
```
```
pip install -r requirements.txt
```

## Deployment

#### 1. Make sure that Zookeeper is running , o.w it won't work
#### 2. Run app.py as the number of the subfolder in  differnet cmd/bash instance

```bash
.\venv\Scripts>activate.bat
python .\app.py
```

#### 3. Run FrontGateApp.py as front end server that will create api request to leader at http://127.0.0.1:5000 
!! caution makesure the default ip of FrontGateApp is 127.0.0.10 , its mean that if you have more then 10 subfolder , you will have to run 10 workers and one of them will hold http://127.0.0.10:5000, you will have to change the FrontGateapp ip to other ip that free. 

```bash
.\venv\Scripts>activate.bat
python .\FrontGateApp.py
```
## API Reference

#### Tf-IDF game generator

```http
  GET 127.0.0.1:5000/{phrase}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phrase` | `string` | **Required**. Phrase to run on it IDF-TF |


#### Generate Phrase

```http
  GET 127.0.0.1:5000/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `phrase` | `string` | **Required**. Phrase generator |

#### Make worker run TF on phrase

```http
  GET 127.0.0.{worker_number+1}:5000/{phrase}/{subfolder}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `worker_number+1` | `int` | **Required**. worker index ip |
| `phrase`      | `string` | **Required**. The phrase for TF run |
| `subfolder` | `int` | **Required**. Index of subfolder also matched to number of worker|





## Screenshots

## initial
![App Screenshot](https://i.ibb.co/RzZmT3b/sc1.png)
## Less Signifcant score answer 
![App Screenshot](https://i.ibb.co/3FKchdH/sc2.png)
## Most Signifcant score answer
![App Screenshot](https://i.ibb.co/Xp2tBpq/sc3.png)


