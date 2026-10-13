# CS408-Big-Project

## Running it
python3 -m pip install django

python3 manage.py runserver

## Deploy
scp -i ~/keys/mykey.pem -r deploy ubuntu@<PUBLIC-IP>:~
ssh -i ~/keys/mykey.pem ubuntu@<PUBLIC-IP>
sudo bash deploy/setup-ec2.sh

## Deploy the actual code 
./deploy/deploy.sh -h <PUBLIC-IP> -i ~/keys/webdev.pem