Documentation for skype


You will have to add skype to the channels in the config.json file. 

This channel will take two inputs, cid ~ Skype bot's id, cs ~ Skype bot's secret.

To use complex responses(buttons, cards, videos), the user will have to import class SkypeBot from skype folder. 

For further understanding of the methods of sending and receiving the message, read the readme in the skype folder.


Example of a simple text message: 


SkypeBotInstance.setData(usersMessage) 

SkypeBotInstance.sendTextMessage("Some text message", userMessage)


Example of a complex message: 


SkypeBotInstance.setData(usersMessage) // Only if you want to avoid giving the userMessage/Payload again 

msg = SkypeBotInstance.createMessage() 

SkypeBotInstance.addImage(msg, "http://i.imgur.com/CfSwf.jpg") 

SkypeBotInstance.sendMessage(msg) (or) SkypeBotInstance.sendMessage(msg, usersMessage)
