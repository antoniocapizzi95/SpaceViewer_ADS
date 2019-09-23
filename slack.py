from slacker import Slacker
class Slack:
    token = '' #insert slack bot token
    def sendMessage(self, message):
        sl = Slacker(self.token)
        sl.chat.post_message('#automatic_alerts', message)
