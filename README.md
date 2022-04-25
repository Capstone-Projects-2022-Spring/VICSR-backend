# VICSR Backend

VICSR's backend was built using Django for the server, PostgresSQL V13 for the database. VICSR backend also requires accounts with Amazon S3 Bucket for persistant file storage, Google Translate API, and Wikipedia API. All database tables are built from Django's models. The VICSR Server has the follow apps:
* AccountManagement
* DocumentManagement
* DocumentProcessing
* VocabularyManagement              
                          
Each VICSR server app has associated API calls for the frontend to utilize. 

## Deploying // Running for dev

### Development/Local Setup
1) Clone or unzip VICSR Backend repository
2) Install all libraries in requirements.txt

#### Database Setup
The VICSR Database is implemented with PostgreSQL V13. For local development, follow instructions for your OS [here](https://www.postgresqltutorial.com/postgresql-getting-started/).  Once PostGresSQL is installed create a local database, and complete the following steps:
1) Update settings.py with database user and password
2) Run command ```python manage.py``` from project directory
3) Run command ```makemigrations``` to initialize all Django models
4) Run command ```migrate``` to build tables in local database

#### Server Setup
The VICSR Server is implemented with Django. To run VICSR's Django Server locally, run the following command:                    
```python manage.py runserver```

#### S3 Bucket, Google API, Wikipedia API
Sign up for an S3 account and follow Amazon's directions for getting and AWS Access Key ID and Key. Also follow directions give from Google and Wikipedia to access their APIs. Include all related details in a conig file(s). 

### Deploying on Heroku
##### Initital setup:
1) Add a Postgres database to the Heroku project
2) Add the following buildpacks:           
   * heroku/python            
   * https://github.com/k16shikano/heroku-buildpack-poppler   
   * https://github.com/pathwaysmedical/heroku-buildpack-tesseract              
   * https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack.git
3) Add the following Config Vars:       
   * ALLOWED_HOSTS | vicsr-api.herokuapp.com  
   * AWS_ACCESS_KEY_ID | *Your AWS Access Key ID*
   * AWS_SECRET_ACCESS_KEY | *Your AWS Secret Access Key*
   * GOOGLE_APPLICATION_CREDENTIALS | google-credentials.json 
   * GOOGLE_CLIENT_ID | *Your Google client ID*
   * GOOGLE_CREDENTIALS | *Your Google credentials*
   * GOOGLE_KEY | *Your Google Key*
   * GOOGLE_KEY_ID | *Your Google Key ID*
   * GOOGLE_PROJECT_ID | *Your Google project ID*
   * S3_BUCKET_NAME | *Your S3 bucket name*
   * WEB_CONCURRENCY | 2+  *(depending on Heroku tier)*

##### Deployment:
1) Make sure you have Heroku CLI installed              
2) ```heroku login```                   
3) Make sure to add heroku remote origin with this command:        
 ```heroku git:remote -a vicsr-api```
4) ```git add .```
5) ```git commit -am "message"```
6)  ```git push heroku main```

## Current Features
- User authentication/management
- Document Upload:
     * Split PDF into multiple images
     * Each image cleaned up and straightened for OCR
     * Each image resized to frontend canvas size
     * OCR implemented and any already highlighted words extracted
     * Associated study set auto-generated
- Document Management(rename, delete)
- Live highlight to translation/definition 
- Custom study set creation
- Study set words ordered by user feedback

## Known Bugs
- OCR misses some words, therefore cannot be found in query from frontend highlight.
- OCR processing upon upload is slow.  To fix this OCR should be implemented as a background process.
- Some definitions returned from the Wikipedia API are not ideal/the best choice for the word.
- Sapced repition algorithm not implememnted, only take user's feedback. 
