__DOCUMENTATION__


To ensure that the project is easily modifiable(in confirmation with the OOPS concept), I went with a layered abstraction approach.

The system has 2 major components:

1)INIT.py ~ Contains the SkypeBot class which implements various hooks to obtain data from payload

2)INTERNAL.py ~ Contains the end point functionality of the system.


__DOCUMENTATION OF INIT__


It is the main component of Skype.py, the SkypeHandler inherits the SkypeBot class present here.

It takes 2 inputs, skype bot's id and skype bot's secret.


__Functions:__


sendTextMessage(StringMessage) ~ Sends a simple text message as response.

sendMessage(Message) ~ Sends a complex message/payload as response.

createMessage(StringMessage) ~ Creates a simple complex message(the return value is to be stored to use the message).

addButton() ~ Adds a button to a message.

addImage() ~ Adds an image to a message.

addMedia() ~ Adds a video/file to a message.

addCard() ~ Adds a card to a message.


__JSON Hooks:__


getService() ~ Gets the URL to send the message to.

getSender() ~ Gets the sender of the message.

getUserId() ~ Gets the sender ID for a specific chat thread.

getUserStore() ~ Gets a concatenated string of user's name and user's id.

getType() ~ Gets the type of the communication.

getText() ~ Gets the text in the message/data/payload.

getBotId() ~ Gets the bot's Id.

setData() ~ Sets data to be used by the object.

getData() ~ Gets data being used by the object.


__DOCUMENTATION OF internal.py__


It is the main component of SkypeBot class. It is the lowest level of abstraction of the system.

It contains bottomline functions that will be used for transmission.

All data must be pre extracted to use this, which is handled by SkypeBot.


Functions:

CreateBasicPayload() ~ Creates and returns a basic json message/payload.

Send() ~ Sends any message to the specified destinations.

SendTextMessage() ~ Used for sending a basic text message.

AddButton() ~ Adds a button to a message.

AddImage() ~ Adds an image to a message.

AddCardDetails() ~ Adds a card to a message.

AddMedia() ~ Adds media to a message.

