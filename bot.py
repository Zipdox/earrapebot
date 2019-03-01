import discord
import asyncio


client = discord.Client()
started = 0

settings_file = open('words.txt', 'r').read().replace('\n', '').strip()
exec(settings_file)





@client.event
async def on_ready():
    global started
    if started == 0:
        print('\n')
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        await client.change_presence(game=discord.Game(name='with eardrums'))
        print('\n')
        started = 1

@client.event
async def on_message(message):
    global wordlist

    def done():
        print('Done\n')

    sendertype = str(type(message.author))


    if 'Member' in sendertype and message.author.voice.voice_channel != None and client.user != message.author and message.author.id not in exceptions:
        voice_limit = message.author.voice.voice_channel.user_limit
        users_in_channel = len(message.author.voice.voice_channel.voice_members)
        if voice_limit == 0:
            proceed = 1
        elif voice_limit - users_in_channel > 0:
            proceed = 1
        else:
            proceed = 0
    else:
        proceed = 0



    if proceed == 1:

        voice_channel = message.author.voice.voice_channel

        def print_cli(warning):
            if len(warning) > 4:
                print('\n' + message.author.name + ' in ' + str(message.author.voice.voice_channel) + warning + '#' + str(message.channel))

        def get_reply(warning):
            return message.author.mention + warning + message.channel.mention


        for triggers in wordlist:
            for word in triggers[0]:
                if word in message.content.lower():
                    warning = triggers[1]
                    print_cli(warning)
                    try:
                        vc = await client.join_voice_channel(voice_channel)
                    except:
                        print('Error: Can\'t join channel.\n')
                    else:
                        try:
                            await client.send_message(message.channel, get_reply(warning))
                        except:
                            print('Can\'t send message.')
                        player = vc.create_ffmpeg_player('audio/' + triggers[2])
                        # player.volume = float(2)
                        player.start()
                        while not player.is_done():
                            await asyncio.sleep(1)
                        player.stop()
                        done()
                        await vc.disconnect()
                        break
            else:
                continue
            break


client.run('TOKEN')
