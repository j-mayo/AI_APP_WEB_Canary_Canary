# MLOps server & Deeplearning Code

## [Deeplearning Code link](https://github.com/osamhack2021/AI_APP_WEB_Canary_Canary/tree/main/AI(BE)/deeplearning/kwoledge_distillation_yolov5)

## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API
 **GET /admin**  
 
 *account*
 **POST /account/login**  
 > parameters: {"username": "string", "password": string"}   
 > status: 201   
 > respose: {"message": "string", "token": string}   
 
 *deeplearning*
 **GET /deeplearning/files**  
 > status: 200  
 > response: { "count": 0, "next": "string", "previous": "string", "results": [{"file": "string"}]}   
 
 **POST /deeplearning/files**  
 > parameters: {"file": [FILE]}  
 > status: 200  
 > response: {"file": "string"}  
 
 **GET /deeplearning/log**
 > response {"count": 0, "next": "string", "previous": "string", "results": [{"username": "string", "log": "string", "create_at": "2021-10-14T13:50:37.279Z"}]}  
 
 **POST /deeplearning/log**
 > parameters: {"username": "string", "log": "string", "create_at": "2021-10-14T13:52:33.709Z"}  
 > status: 201  
 > response: {"username": "string", "log": "string", "create_at": "2021-10-14T13:52:33.709Z"}  
 
 **GET /deeplearning/models**  
 > status: 200  
 > response: {"file": "string", "result": "string", "version": 0, "matrix": 0}  
 
 **POST /deeplearning/train**
 > headers: {'Authorization': 'Bearer [TOKEN]'}  
 > status: 201  
 > response: {"file": "string"} 

## Architecture
![Architecture](https://user-images.githubusercontent.com/40621030/136700081-b195dfa6-1c21-4983-a4cd-463f7e584091.PNG)

## Screen Shot
### Admin Page
<p align='center'><img src='https://user-images.githubusercontent.com/40621030/136724519-9a6b4318-bfc3-4591-91ad-6c92d8d59563.PNG' width=800></p>
<p align='center'><img src='https://user-images.githubusercontent.com/40621030/136724521-82aeca91-224a-4ce7-bcdc-1176f71e556d.PNG' width=800></p>

### Registered Model
<p align='center'><img src='https://user-images.githubusercontent.com/40621030/136724526-e2f2a054-2405-4e23-8f5f-b25a570ff838.PNG' width=800></p>

### Registered Data
<p align='center'><img src='https://user-images.githubusercontent.com/40621030/136724529-a3e0d81b-94d9-4088-8a0a-730773718a0c.PNG' width=800></p>

### Train Authorization
<p align='center'><img src='https://user-images.githubusercontent.com/40621030/136724532-46603bc3-c0e0-497b-904d-3359610f8079.PNG' width=800></p>
