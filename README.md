# code-test-messages

### Requirements
- Pyhton3

### To run the application:
- Clone the repository: `git clone git@github.com:oanafatu/`code-test-messages`.git` && `cd git@github.com:oanafatu/code-test-messages.git`
- Create a virtual environment by running `make virtualenv`
- to activate the venv run `source venv/bin/activate`

- run `make install` 
- to start the server, run `python run.py`

The data is stored and manipulated in csv files. To work with csv I use pandas. You can find the files under the folder database:
- messages.csv
- users.csv
* If I were to start over I would probably use postgres (and SQL Alchemy) for data. 

### How to interact with the application:

#### To fetch all messages, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/
- curl http://localhost:5000/api/v1/messages/

#### To fetch all messages that were not previously fetched, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/?include-previously-fetched=no
- curl "http://localhost:5000/api/v1/messages/?include-previously-fetched=no"

#### To fetch ordered by time messages between index range, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/order/start-index={int}&stop-index={int} --> for example: `http://localhost:5000/api/v1/messages/order/?start-index=1&stop-index=3`
- curl "http://localhost:5000/api/v1/messages/order/start-index={int}&stop-index={int}" --> for example: `curl "http://localhost:5000/api/v1/messages/order/?start-index=1&stop-index=3"`

#### To fetch one message by id, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/{message_id} --> for example: `http://localhost:5000/api/v1/messages/8c39c437-ec2a-43dc-a94b-cb0041c2bc31`
- curl http://localhost:5000/api/v1/messages/{message_id} --> for example: `curl http://localhost:5000/api/v1/messages/8c39c437-ec2a-43dc-a94b-cb0041c2bc31`

#### To submit a message to a user, use curl:
- curl -X POST --data '{"text": {text}} --header "Content-Type:application/json" http://localhost:5000/api/v1/messages/user/{username}/submit-message
For example: `curl -X POST --data '{"text": "I did it!"}' --header "Content-Type:application/json" http://localhost:5000/api/v1/messages/user/elsa/submit-message`

#### To delete one or more messages, use curl:
-  curl -X POST --data '{"ids": [{message_id}, {message_id}]}' --header "Content-Type:application/json" http://localhost:5000/api/v1/messages/delete-messages
For example: `curl -X POST --data '{"ids": ["775f9d8b-33ba-4734-abd5-759dd3f38251"]}' --header "Content-Type:application/json" http://localhost:5000/api/v1/messages/delete-messages`

#### To fetch all users, use one of the options below:
- navigate to: http://localhost:5000/api/v1/users/
- curl http://localhost:5000/api/v1/users/

#### To fetch all messages for one user, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/user/{username} --> for example: `http://localhost:5000/api/v1/messages/user/elsa`
- curl http://localhost:5000/api/v1/messages/user/{username} --> for example: `curl http://localhost:5000/api/v1/messages/user/elsa`



