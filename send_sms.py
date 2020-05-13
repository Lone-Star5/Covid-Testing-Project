# we import the Twilio client from the dependency we just installed
from twilio.rest import Client

# the following line needs your Twilio Account SID and Auth Token
client = Client("AC4672b67005b1dd29b144f1c0dc287d78", "da66c458d1f6249fe24875c7d2d7259d")

# change the "from_" number to your Twilio number and the "to" number
# to the phone number you signed up for Twilio with, or upgrade your
# account to send SMS to any phone number
client.messages.create(to="+917838101076", 
                       from_="+15703654934", 
                       body="Hello from Python!")