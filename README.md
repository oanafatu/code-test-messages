# code-test-messages

### Requirements
- Pyhton3

### To run the application:
- Create the virtual environment by running `make virtualenv`
- to activate the venv run `source venv/bin/activate`

- run `make install` 
- to start the server, run `python run.py`

The data is stored and manipulated in csv files. To work with csv I use pandas. You can find the files under the folder database:
- messages.csv
- users.csv

### How to interact with the application:

#### To fetch all messages, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/
- curl http://localhost:5000/api/v1/messages/

#### To fetch all messages that were not previously fetched, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/?include-previously-fetched=no
- curl http://localhost:5000/api/v1/messages/?include-previously-fetched=no

#### To fetch ordered by time messages between index range, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/order/start-index={int}&stop-index={int} --> for example: `http://localhost:5000/api/v1/messages/order/start-index=1&stop-index=3`
- curl http://localhost:5000/api/v1/messages/order/start-index={int}&stop-index={int} --> for example: `curl http://localhost:5000/api/v1/messages/order/start-index=1&stop-index=3`

#### To fetch one message by id, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/{message_id} --> for example: `http://localhost:5000/api/v1/messages/834ca4f1-0650-48a5-abb8-0236cc871e39`
- curl http://localhost:5000/api/v1/messages/{message_id} --> for example: `curl http://localhost:5000/api/v1/messages/834ca4f1-0650-48a5-abb8-0236cc871e39`

#### To submit a message to a user, use curl:
- curl -X POST --data '{"text": {text}} --header "Content-Type:application/json" http://localhost:5000/api/v1/messages/user/{username}/submit-message
For example: `curl -X POST --data '{"text": "I did it!"}' --header "Content-Type:application/json" http://localhost:5000/messages/api/v1/user/user1/submit-message`

#### To delete one or more messages, use curl:
-  curl -X POST --data '{"ids": [{message_id}, {message_id}]}' --header "Content-Type:application/json" http://localhost:5000/messages/api/v1/delete-messages
For example: `curl -X POST --data '{"ids": ["fa3af6c1-94b8-46f0-b5fa-cef15810f855"]}' --header "Content-Type:application/json" http://localhost:5000/messages/api/v1/delete-messages`

#### To fetch all users, use one of the options below:
- navigate to: http://localhost:5000/api/v1/users/
- curl http://localhost:5000/api/v1/users/

#### To fetch all messages for one user, use one of the options below:
- navigate to: http://localhost:5000/api/v1/messages/user/{username} --> for example: `http://localhost:5000/api/v1/messages/user/ana`
- curl http://localhost:5000/api/v1/messages/user/{username} --> for example: `curl http://localhost:5000/messages/api/v1/user/ana`



