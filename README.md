
# Association Game based TF-IDF Algorithem[MVP version]

This system will generate Phrase and will give you
4 stories that were ran up in the TF-IDF search Algorithem.
The user will get the score based on the answer precantage it 
got in the IDF-TF.

## Use case
![App Screenshot](https://i.ibb.co/wBVMc7m/UseCase.jpg)

## UML
![App Screenshot](https://i.ibb.co/54jM8PY/UML.png)

## Features

- The algo of TF-IDF is Disterbuted on zookeeper
- Based Flask
- Cross platform


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
