# Django API Documentation

### Account Management

Login: /api/users/auth/login/
* Body: { email, password }

Register: /api/users/auth/register/
* Body: { email, password1, password2 }

Logout: /api/users/auth/logout/
* Body: { Token <token> }


### Document Management

Add Doc: /api/docs/add/
* POST
* Body: { filename, file, mode, language, trans_language }
  * trans_language can be left blank when in definition mode
* Headers
  * Authorization: Token <token>
    
Get Docs: /api/docs/list/
* GET
* Headers
  * Authorization: Token <token>

Delete Doc: /api/docs/delete/<id>
* DELETE
* Headers
  * Authorization: Token <token>
    
Update Doc: /api/docs/update/<id>
* POST
* Body: { filename }
* Headers
  * Authorization: Token <token>


### Vocabulary Management

Get all Study Sets: /api/vocab/sets/
* GET
* Headers
  * Authorization: Token <token>
    
Get words by Study Set ID: /api/vocab/sets/<id>/words
* GET
* Headers
  * Authorization: Token <token>
    
Get Study Set by Document ID: /api/vocab/sets/fromDoc/<id>
* GET
* Headers
  * Authorization: Token <token>
    
Get all words: /api/vocab//allWords
* GET
* Headers
  * Authorization: Token <token>