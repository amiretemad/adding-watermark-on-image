# AmazonS3WithPython
Simple python API end-point to add watermark on the image and upload to AWS-S3 (Simple Storage Service).

## How To run project ? 
After cloning project to your local machine (make sure you have installed Python 3 on your machine),please run this commands in the root directory of project to set Amazon Credentials.

#### Configure Amazon Credentials
```
 $ pip install awscli 
 $ aws configure 
```
#### Run Project
```
python app.py
```

#### Request Example
```
curl --location --request POST 'http://127.0.0.1:5000/upload-image' \
--form 'file=@/directory/Downloads/hello.jpg' \
--form 'text=Watermark text'
```

