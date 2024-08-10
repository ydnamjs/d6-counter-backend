# D6 Counter Backend

API made with FastAPI that receives images of six sided dice and runs them through an AI model for detection and classification

# Live Front End Site
Check out the React.js App that this API was made for at: https://ydnamjs.github.io/d6-counter-frontend/

# Technologies Used
- Amazon Web Services (AWS)
- Python
- FastAPI
- Nginx
- PyTorch
- Torchvision
- openCV
- Python Image Library (PIL)

# AWS Deployment On An EC2 Ubuntu Instance

## Setting Up The Instance

In AWS under all services under Computer select EC2

![image](https://github.com/user-attachments/assets/bd6405b1-6156-4d64-9c2e-3d8237a7ade7)

In the EC2 dashboard select "Launch Instance"

![image](https://github.com/user-attachments/assets/c188532d-8738-46e0-833d-f5fa417bc498)

In the "Application and OS Images (Amazon Machine Image)" section select Ubuntu and Ubuntu Server 24.04 LTS

![image](https://github.com/user-attachments/assets/8899baec-c618-48e3-a06a-f7b4e1f666ea)

In "Network Settings" turn on "Allow HTTP traffic from the internet"

![image](https://github.com/user-attachments/assets/096fd678-510d-463f-a9ce-f3fbad13765a)

Launch and connect to the instance

Run
```
sudo apt-get update
```

Run
```
sudo apt-get upgrade
```

## NGINX Setup

Run
```
sudo apt install nginx
```

Run
```
sudo vim /etc/nginx/sites-enabled/d6_counter_api
```

Enter this in the file making sure to put your EC2 instance's Public IPv4 address in the server_name field
```
server {
        listen 80;
        server_name *PUT_YOUR_EC2_IP_HERE*;
        location / {
                proxy_pass http://127.0.0.1:8000;
        }
}
```

Restart the nginx service
```
sudo service nginx restart
```

## Deploying The API

Install python virtual environment
```
sudo apt install python3.12-venv
```

Clone the repository
```
git clone https://github.com/ydnamjs/d6-counter-backend.git
```

Move into the repository 
```
cd d6-counter-backend
```

Create a python virtual environment
```
python3 -m venv python-environment
```

Install general dependencies
```
python-environment/bin/pip3 install -r requirements/general.txt
```

Install torch dependencies
```
python-environment/bin/pip3 install -r requirements/torch.txt
```

Move into src
```
cd src/
```

Run the app
```
../python-environment/bin/python3 -m uvicorn main:app
```

Run the app detached from the console
```
nohup ../python-environment/bin/python3 -m uvicorn main:app &
```
