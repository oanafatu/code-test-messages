# code-test-messages

### Requirements
- Pyhton3

### To run the application:
- Create the virtual environment by running `make virtualenv`
- to activate the venv, run in terminal: `source venv/bin/activate`

- run `make install`
- `python run.py`

The data is in csv files:
- messages.csv
- users.csv


To submit a message to a user, use curl:
 curl -X POST --data '{"text": `{text}} --header "Content-Type:application/json" http://localhost:5000/messages/`{username}`/submit-message
For example: `curl -X POST --data '{"text": "I did it again!"}' --header "Content-Type:application/json" http://localhost:5000/messages/user1/submit-message`

