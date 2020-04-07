# code-test-messages

### Requirements
- Pyhton3

### To run the application:
- Create the virtual environment by running `make virtualenv`
- to activate the venv run `source venv/bin/activate`

- run `make install` 
- to start the server, run `python run.py`

The data is stored and manipulated in csv files. To work with csv I use pandas. You can find the files under folder database:
- messages.csv
- users.csv

### How to interact with the application:

#### To submit a message to a user, use curl:
- curl -X POST --data '{"text": {text}} --header "Content-Type:application/json" http://localhost:5000/messages/user/{username}/submit-message
For example: `curl -X POST --data '{"text": "I did it!"}' --header "Content-Type:application/json" http://localhost:5000/messages/user/user1/submit-message`

#### To delete one or more messages, use curl:
-  curl -X POST --data '{"ids": [{message_id}, {message_id}]}' --header "Content-Type:application/json" http://localhost:5000/messages/delete-messages
For example: `curl -X POST --data '{"ids": ["fa3af6c1-94b8-46f0-b5fa-cef15810f855"]}' --header "Content-Type:application/json" http://localhost:5000/messages/delete-messages`

#### To fetch all messages, use one of the options below:
- navigate to: http://localhost:5000/messages/
- curl http://localhost:5000/messages/
``
#### To fetch one message by id, use one of the options below:
- navigate to: http://localhost:5000/messages/{message_id} --> for example: `http://localhost:5000/messages/834ca4f1-0650-48a5-abb8-0236cc871e39`
- curl http://localhost:5000/messages/{message_id} --> for example: `curl http://localhost:5000/messages/834ca4f1-0650-48a5-abb8-0236cc871e39`

#### To fetch all messages for one user, use one of the options below:
- navigate to: http://localhost:5000/messages/user/{username} --> for example: `http://localhost:5000/messages/user2`
- curl http://localhost:5000/messages/user/{username} --> for example: `curl http://localhost:5000/messages/user2`



