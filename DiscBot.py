import discord
import random
import string

activeSessions = {
    #userid:{data}
}

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, I am your personal helper. Feel free to reach out if you ever want to talk.'
        )

    async def on_message(self, message):
        if message.guild is None:
            if message.author.id != self.user.id:
                if message.author.id not in activeSessions:
                    await message.channel.send(f'Hi, {message.author.name}, I am here to help.')
                    await message.channel.send('How are you feeling right now?')
                    activeSessions.update({
                        message.author.id: {
                            'user_info': message.author,
                            'step': 1
                        }
                    })

                else:
                    if activeSessions[message.author.id]['step'] == 1:
                        #  Save their response to the initial question here, and check for keywords
                        sentiment = self.check_sentiment(message.content.split())
                        if sentiment == 'happy':
                            await message.author.create_dm()
                            await message.author.dm_channel.send(
                                f'Hi {message.author.name}, I am really glad to hear that! You should keep it up!'
                                f'Stay around supportive friends and family, so you can stay happy! :smile:'
                            )
                        if sentiment == 'sad':
                            await message.author.create_dm()
                            await message.author.dm_channel.send(
                                f'Hi {message.author.name}, That\'s alright. We all have our off days. '
                                f'There is always someone to talk to. Never be afraid to reach out to a loved one.'
                                f'You can also call (877) 870-4673. You are an amazing person!')

                        if sentiment == 'bully':
                            await message.author.create_dm()
                            await message.author.dm_channel.send(
                            f'Hi {message.author.name}, Please reach out to an adult. You are an amazing person'\
                            f'who deserves kindess. You can also call 1-800-273-8255 if you feel really down.'
                        )
    def check_sentiment(self, tokens):
        happy_set = {'happy', 'excited', 'amazed', 'energized', 'joyful', 'joy', 'great'}
        sad_set = {'sad', 'upset', 'depressed', 'disappointed', 'unhappy', 'sorrowful'}
        overwhelmed_set = {'overwhelmed', 'busy', 'stressed'}
        bully_set = {'bully', 'bullied', 'abused'}
        sentiments = {'happy': 0, 'sad': 0, 'scared': 0, 'bully': 0, 'confused': 0}
        sentiment = 0
        for token in tokens:
            token = token.translate(str.maketrans('', '', string.punctuation))
        for token in tokens:
            if token in sad_set:
                sentiments['sad'] += 1
            if token in happy_set:
                sentiments['happy'] += 1
            if token in bully_set:
                sentiments['bully'] += 1
            if token in overwhelmed_set:
                sentiments['overwhelmed'] += 1

        return max(sentiments, key=sentiments.get)

client = MyClient()


client.run('NjgzNDY1MjE1OTgzMjIyODY0.XlsFtA.yPAFR7UT4ZS4NI_9Iw3aycP5fvs')