# Architecutre

## Cloud Architecture
![image info](C:\Users\Anak\Pictures\FAUCovidCrawler\fau_covid_crawler_cloud_architecture.png) 


## Local Architecture
![image info](C:\Users\Anak\Pictures\FAUCovidCrawler\fau_covid_crawler_local_architecutre.png) 

# Todo list 
- [ ] create CDK for servless 
  - requirement:
    - create new resources for all the stack comonents. 
- [ ] here> stream reddit data
  - system requirement:
    - create new lambda reddit_firhose.txt
- [ ] create path with string query to sample data given ranges.
- [ ] create path for kinesis stream
  
# Things to do

## about the architecture 

### api gateway 

- [ ] create path with string query to sample data given ranges. 
- [ ] create path for kinesis stream


### kinesis
- [ ] figure out why data is encrypting when I access it via apigateway

## about streaming 

### reddit 
- [ ] here> stream reddit data
  - system requirement:
    - create new lambda reddit_firhose.txt

### twitter  
- [ ] figure out why I get 420 error when running C:\Users\Anak\PycharmProjects\cdkworkshop\FAUCovidCrawler\AWSKinesisAndFirehose\twitter_firehose.py

## about Testing 
- [ ] figure out how to test with Moto.
  - do the following:
    - [ ] moto with lambda
    - [ ] moto with kinesis
    - [ ] moto with s3
    - [ ] moto with dynamoDB
    
## about features 

- [ ] implement airflow to shedule + orchestrate the architecutre.
- [ ] send email to awannaphasch2016@fau.edu whenever program failed to run.
  
### api gateway 
- [ ] create path for s3 

### migrate to local
- [ ] s3 to MinIO
- [ ] dynamoDB to MongoDB
- [ ] apigateway to apistar
