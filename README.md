# AWS Deployment

Create an EC2 ubuntu instance and ssh in

Run
```
sudo apt-get update
```

Run
```
sudo apt-get upgrade
```

Run
```
sudo apt install nginx
```

Run
```
sudo apt install python3.12-venv
```

## NGINX Setup

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

## APP Setup

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

Run the app until killed
```
nohup ../python-environment/bin/python3 -m uvicorn main:app &
```
