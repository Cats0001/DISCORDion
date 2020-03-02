import discord
import string

activeSessions = {
    #  userid:{data}
}

resources = {  # sentiment:{resource:{contact method: info}}}
    'sad': {
        'Anxiety and Depression Association of America': {
            'url': 'https://adaa.org/understanding-anxiety/depression',
            'helpline': None
        },
        'Substance Abuse and Mental Health Services Helpline': {
            'url': 'https://www.samhsa.gov/',
            'helpline': '1-800-662-HELP (4337)'
        },
        'American Academy of Child and Adolescent Psychiatry': {
            'url': 'https://www.aacap.org/',
            'helpline': None
        },
        'National Suicide Prevention Lifeline': {
            'url': 'https://suicidepreventionlifeline.org',
            'helpline': '1-800-273-TALK (8255)'
        },
        'Crisis Text Line': {
            'url': 'https://www.crisistextline.org/get-help/depression',
            'helpline': 'text HOME to 741741'
        }

    },
    'bully': {
        'National Suicide Prevention Lifeline': {
            'url': 'https://suicidepreventionlifeline.org',
            'helpline': '1-800-273-TALK (8255)'
        },
        'Crisis Text Line': {
            'url': 'https://www.crisistextline.org/get-help/bullying',
            'helpline': 'text HOME to 741741'
        },
        'StopBullying': {
            'url': 'https://stopbullying.gov',
            'helpline': None
        },
        'Stomp Out Bullying': {
            'url': 'https://www.stompoutbullying.org/get-help/helpchat-line',
            'helpline': 'See Website'
        },
        'LGBT National Help Center': {
            'url': 'https://www.glbthotline.org/',
            'helpline': '888-843-4564 for Adults, 800-246-7743 for for young adults, 888-234-7243 for ages 50+'
        },
        'Substance Abuse and Mental Health Services Helpline': {
            'url': 'https://www.samhsa.gov/',
            'helpline': '1-800-662-HELP (4337)'
        }
    },
    'overwhelmed': {
        'National Suicide Prevention Lifeline': {
            'url': 'https://suicidepreventionlifeline.org',
            'helpline': '1-800-273-TALK (8255)'
        },
        'Crisis Text Line': {
            'url': 'https://www.crisistextline.org/get-help/anxiety',
            'helpline': 'text HOME to 741741'
        },
        'Substance Abuse and Mental Health Services Helpline': {
            'url': 'https://www.samhsa.gov/',
            'helpline': '1-800-662-HELP (4337)'
        },
        'Anxiety and Depression Association of America': {
            'url': 'https://adaa.org/understanding-anxiety',
            'helpline': None
        }
    }
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
                        activeSessions[message.author.id]["sentiment"] = sentiment
                        positive = False  # In case this isn't set later, assume sentiment is not positive
                        if sentiment == 'happy':
                            positive = True
                            await message.author.create_dm()
                            await message.author.dm_channel.send(
                                f'Hi {message.author.name}, I am really glad to hear that! You should keep it up!'
                                f' Stay around supportive friends and family, so you can stay happy! :smile:'
                            )
                        if sentiment == 'sad':
                            await message.author.create_dm()
                            await message.author.dm_channel.send(
                                f'Hi {message.author.name}, That\'s alright. We all have our off days. '
                                f'There is always someone to talk to. Never be afraid to reach out to a loved one.'
                                f' You can also call (877) 870-4673. You are an amazing person!')

                        if sentiment == 'bully':
                            await message.author.create_dm()
                            await message.author.dm_channel.send(
                                f'Hi {message.author.name}, Please reach out to an adult. You are an amazing person'
                                f' who deserves kindness. You can also call 1-800-273-8255 if you feel really down.')

                        if sentiment == 'overwhelmed':
                            await message.author.create_dm()
                            await message.author.dm_channel.send(
                                f'Hi {message.author.name}, consider taking a break from your school or work. You can'
                                f' also set specific hours for your work, and make sure you relax when not during'
                                f' designated work hours.')
                        if not positive:
                            await message.author.dm_channel.send(
                                f'Would you like additional resources to help deal with how you are feeling? Please '
                                f'respond yes or no.')

                            activeSessions[message.author.id]["step"] = 2
                        else:
                            activeSessions.pop(message.author.id, None)  # Delete session, dm bot for new one

                    elif activeSessions[message.author.id]['step'] == 2:
                        give_resources = False
                        await message.author.create_dm()
                        yes_set = {'yes', 'y', 'yeah', 'sure', 'of course', 'please'}
                        for item in yes_set:
                            if item in message.content:
                                give_resources = True
                                break

                        if give_resources:
                            help_centers = ''
                            for index, item in enumerate(resources[activeSessions[message.author.id]["sentiment"]]):
                                help_centers = help_centers + f'{index+1}: {item} \n'
                            await message.author.dm_channel.send('Please select an option from the following:')
                            await message.author.dm_channel.send(help_centers)
                            activeSessions[message.author.id]['numberOptions'] = \
                                range(1, len(resources[activeSessions[message.author.id]["sentiment"]])+1)
                            activeSessions[message.author.id]['step'] = 3
                            activeSessions[message.author.id]['resources'] = help_centers

                        else:
                            await message.author.dm_channel.send("OK. Feel free to message me again if you change"
                                                                 " your mind :smile:")
                            activeSessions.pop(message.author.id, None)  # Delete session, dm bot for new one

                    elif activeSessions[message.author.id]['step'] == 3:
                        await message.author.create_dm()
                        try:
                            print(message.content)
                            message_number = int(message.content)
                            if message_number in activeSessions[message.author.id]['numberOptions']:
                                selected_option = list(resources[activeSessions[message.author.id]["sentiment"]].keys())\
                                    [message_number-1]
                                print(selected_option)
                                if resources[activeSessions[message.author.id]["sentiment"]][selected_option]['helpline']:
                                    message_to_send = f'You can reach the {selected_option} here: \n Website: ' \
                                        f'{resources[activeSessions[message.author.id]["sentiment"]][selected_option]["url"]} \n ' \
                                        f'Phone: {resources[activeSessions[message.author.id]["sentiment"]][selected_option]["helpline"]}'

                                    await message.author.dm_channel.send(message_to_send)
                                else:
                                    message_to_send = f'You can reach the {selected_option} here: \n Website: ' \
                                        f'{resources[activeSessions[message.author.id]["sentiment"]][selected_option]["url"]}'
                                    await message.author.dm_channel.send(message_to_send)
                                await message.author.dm_channel.send("Would you like the contact information for "
                                                                     "another organization? Please enter yes/no")
                                activeSessions[message.author.id]['step'] = 4

                            else:
                                await message.author.dm_channel.send(f"Please enter a number within the supplied range")

                        except Exception as e:
                            print(e)
                            await message.author.dm_channel.send("Sorry, but that doesn't appear to be a number."
                                                                 " Please re-enter the corresponding number for your"
                                                                 " chosen site :slight_frown:")

                    elif activeSessions[message.author.id]['step'] == 4:
                        repeat_resources = False
                        await message.author.create_dm()
                        yes_set = {'yes', 'y', 'yeah', 'sure', 'of course', 'please'}
                        for item in yes_set:
                            if item in message.content:
                                repeat_resources = True
                                break
                        if repeat_resources:
                            await message.author.dm_channel.send('Please select an option from the following:')
                            await message.author.dm_channel.send(activeSessions[message.author.id]["resources"])
                            activeSessions[message.author.id]['step'] = 3
                        else:
                            await message.author.dm_channel.send("OK. Feel free to message me again if you change"
                                                                 " your mind :smile:")
                            activeSessions.pop(message.author.id, None)  # Delete session, dm bot for new one


    def check_sentiment(self, tokens):
        happy_set = {'happy', 'excited', 'amazed', 'energized', 'joyful', 'joy', 'great'}
        sad_set = {'sad', 'upset', 'depressed', 'disappointed', 'unhappy', 'sorrowful'}
        overwhelmed_set = {'overwhelmed', 'busy', 'stressed', 'out of control'}
        bully_set = {'bully', 'bullied', 'abused'}
        sentiments = {'happy': 0, 'sad': 0, 'scared': 0, 'bully': 0, 'overwhelmed': 0}
        sentiment = 0
        for token in tokens:
            token = token.translate(str.maketrans('', '', string.punctuation))  # What is this meant to do?

        for token in tokens:
            if token in sad_set:
                sentiments['sad'] += 1
            if token in happy_set:
                sentiments['happy'] += 1
            if token in bully_set:
                sentiments['bully'] += 1
            if token in overwhelmed_set:
                sentiments['overwhelmed'] += 1

        return max(sentiments, key=sentiments.get)  # return sentiment with max mentions


client = MyClient()
client.run('NTc0Njk2NDExNTA2MTQ3MzM4.XlyOzg.WyJbmcnXu_Y0RcUGFYP-52225I8')

