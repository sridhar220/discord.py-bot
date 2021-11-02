import discord
from discord.ext import commands

import json
with open("C:/Users/<ENTER-USER-NAME>/Desktop/<ENTER-FOLDER-NAME>/config/config.json")     as g: config     = json.load(g)
with open("C:/Users/<ENTER-USER-NAME>/Desktop/<ENTER-FOLDER-NAME>/config/thumbnails.json") as h: thumbnails = json.load(h)

import datetime, random, requests

client = commands.Bot(command_prefix = config['PREFIX'])

THEME = int(config['THEME'], 16)

@client.event
async def on_ready():
    activity = discord.Game(name = config['PREFIX'] + 'cmdlist', type = 3)
    await client.change_presence(activity = activity)
    print(client.user.display_name + ' has connected to Discord!')

@client.event
async def on_command_error(ctx, error):
    if not isinstance(error, commands.CheckFailure):
        await ctx.message.add_reaction('❌')
        await ctx.reply('Either an error occured, or the command does not exist. Please try again!')

@client.command()
async def test(ctx):
    if str(ctx.author.id) == config['CREATOR']['ID']:
        await ctx.reply('Test was successful!')
    else:
        await ctx.reply('You do not have access to this command!')

@client.command()
async def cmdlist(ctx):
    cmdListEmbed = discord.Embed(color = THEME)
    cmdListEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
    cmdListEmbed.set_thumbnail(url = thumbnails['CMDLIST'])
    cmdListEmbed.add_field(name = 'General Commands', value = '`profilepic` `serverinfo` `weather`'       , inline = False)
    cmdListEmbed.add_field(name = 'Fun Commands'    , value = '`geekmeter` `ppmeter` `dadjoke` `gif`'     , inline = False)
    cmdListEmbed.add_field(name = 'Anime Commands'  , value = '`waifu` `anipic` `aniquote` `animesearch`' , inline = False)

    await ctx.send(embed = cmdListEmbed)

@client.command()
async def profilepic(ctx, member: discord.Member = None):
    target = member or ctx.author
    imageLink = target.avatar_url
    profileEmbed = discord.Embed(url = imageLink, title = target.name + '\'s Profile Picture', color = THEME)
    profileEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
    profileEmbed.set_image(url = imageLink)

    await ctx.send(embed = profileEmbed)

@client.command()
async def serverinfo(ctx):
    guildOwnerID     = str(ctx.guild.owner_id)
    guildName        = ctx.guild.name
    guildDescription = ctx.guild.description
    memberCount      = str(ctx.guild.member_count)
    guildIcon        = ctx.guild.icon_url
    textChannels     = str(len(ctx.guild.text_channels))
    voiceChannels    = str(len(ctx.guild.voice_channels))

    guildEmbed = discord.Embed(description = '**Server Information**', color = THEME)
    guildEmbed.add_field(name = 'Server Name'       , value = guildName)
    guildEmbed.add_field(name = 'Server Owner'      , value = '<@' + guildOwnerID + '>')
    guildEmbed.add_field(name = 'Server Description', value = guildDescription)
    guildEmbed.add_field(name = 'Member Count'      , value = memberCount)
    guildEmbed.add_field(name = 'Text Channel(s)'   , value = textChannels)
    guildEmbed.add_field(name = 'Voice Channel(s)'  , value = voiceChannels)

    if guildIcon:
        guildEmbed.set_thumbnail(url = guildIcon)

    await ctx.send(embed = guildEmbed)

@client.command()
async def weather(ctx, *args):
    searchLocation = ' '.join(args)
    if not searchLocation:
        return await ctx.reply('Please mention a location!')
    
    weatherData = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=' + config['APIKEYS']['WEATHER'] + '&q=' + searchLocation).json()

    if weatherData['cod'] != 200:
        return await ctx.reply('Could not find the location.')

    forecastTitle       = '**' + 'Weather forecast for ' + weatherData['name'] + ', ' + weatherData['sys']['country'] + '**'
    forecastTimeZone    = 'UTC ' + str(weatherData['timezone'] / 3600)
    forecastTemperature = str(round(weatherData['main']['temp'] - 273.15)) + '°'
    forecastWindSpeed   = str(round(weatherData['wind']['speed'] * 3.6)) + ' km/h'
    forecastHumidity    = str(round(weatherData['main']['humidity'])) + '%'
    forecastPressure    = str(round(weatherData['main']['pressure'])) + ' hPa'

    weatherEmbed = discord.Embed(description = forecastTitle, color = THEME, timestamp = datetime.datetime.utcnow())
    weatherEmbed.set_thumbnail(url = thumbnails['WEATHER'])
    weatherEmbed.add_field(name = 'TimeZone'   , value = forecastTimeZone)
    weatherEmbed.add_field(name = 'Temperature', value = forecastTemperature)
    weatherEmbed.add_field(name = 'Degree Type', value = 'Celcius')
    weatherEmbed.add_field(name = 'Wind Speed' , value = forecastWindSpeed)
    weatherEmbed.add_field(name = 'Humidity'   , value = forecastHumidity)
    weatherEmbed.add_field(name = 'Pressure'   , value = forecastPressure)

    await ctx.send(embed = weatherEmbed)

@client.command()
async def geekmeter(ctx, member: discord.Member = None):
    target = member or ctx.author
    if target.bot:
        return await ctx.reply('Bots are not geeks!')
        
    percent   = str(random.randint(0,100))
    geekEmbed = discord.Embed(title = 'GeekMeter', description = target.name + '\'s Reading: ' + '`' + percent + '%`', color = THEME)
    geekEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
    await ctx.send(embed = geekEmbed)

@client.command()
async def ppmeter(ctx, member: discord.Member = None):
    pp = '8'
    number = random.randint(0,9)
    for i in range(number + 1): pp += '='
    pp += 'D'

    target = member or ctx.author
    if target.bot: return await ctx.reply('Bots do not have a pp!')
    if str(target.id) == config['CREATOR']['ID']: return await ctx.reply('Too huge!') 

    ppEmbed = discord.Embed(title = 'PP Meter', description = target.name + '\'s Reading: `' + pp + '`', color = THEME)
    await ctx.send(embed = ppEmbed)

@client.command()
async def dadjoke(ctx):
    jokeData = requests.get('https://icanhazdadjoke.com/slack').json()
    joke = jokeData['attachments'][0]['text']
    jokeEmbed = discord.Embed(title = 'Here\'s your dad joke!', description = joke, color = THEME)
    jokeEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
    jokeEmbed.set_thumbnail(url = thumbnails['DADJOKE'])

    await ctx.send(embed = jokeEmbed)

@client.command()
async def gif(ctx, *args):
    searchQuery = ' '.join(args)
    if not searchQuery:
        gifData   = requests.get('https://api.giphy.com/v1/gifs/random?api_key=' + config['APIKEYS']['GIPHY']).json()
        imageLink = gifData['data']['images']['original']['url']
        gifEmbed  = discord.Embed(url = imageLink, title = 'Here\'s your gif!', color = THEME)
        gifEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
        gifEmbed.set_image(url = imageLink)

    else:
        gifData = requests.get('https://api.giphy.com/v1/gifs/search?api_key=' + config['APIKEYS']['GIPHY'] + '&q=' + searchQuery + '&limit=50').json()
        searchResults = gifData['pagination']['total_count']
        searchCount   = gifData['pagination']['count']

        if (not searchResults) or (not searchCount):
           return await ctx.reply('Unfortunately, no results were found.')

        number    = random.randint(0,49)
        imageLink = gifData['data'][number]['images']['original']['url']
        gifEmbed  = discord.Embed(url = imageLink, title = 'Here\'s your gif!', color = THEME)
        gifEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
        gifEmbed.set_image(url = imageLink)
    
    await ctx.send(embed = gifEmbed)

@client.command()
async def waifu(ctx):
    waifuData  = requests.get('https://api.waifu.pics/sfw/waifu').json()
    imageLink  = waifuData['url']
    waifuEmbed = discord.Embed(url = imageLink, title = 'Here\'s your waifu' + ctx.author.name + '-kun!', color = THEME)
    waifuEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
    waifuEmbed.set_image(url = imageLink)

    await ctx.send(embed = waifuEmbed)

@client.command()
async def anipic(ctx, *args):
    picQuery = ' '.join(args).lower()
    picList = ['poke','neko','shinobu','megumin','bully','cuddle','cry','hug','awoo','kiss','lick','pat','smug','bonk','yeet','blush','smile','wave','highfive','handhold','nom','bite','glomp','slap','kill','happy','wink','dance','cringe']
    listLength = len(picList)

    async def embed(link):
        picEmbed = discord.Embed(url = link, title = 'Here\'s your anime picture!', color = THEME)
        picEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
        picEmbed.set_image(url = link)
        await ctx.send(embed = picEmbed)

    if not picQuery:
        number = random.randint(0, listLength - 1)
        picData = requests.get('https://api.waifu.pics/sfw/' + picList[number]).json()
        imageLink = picData['url']
        embed(imageLink)

    else:
        category = ''
        for i in range(0, listLength - 1):
            if picList[i] == picQuery:
                category = picList[i]

        if category == '':
            return await ctx.reply('Invalid category!')
        
        picData = requests.get('https://api.waifu.pics/sfw/' + category).json()
        imageLink = picData['url']
        embed(imageLink)

@client.command()
async def aniquote(ctx):
    quoteData = requests.get('https://animechan.vercel.app/api/random/').json()
    quoteTitle = quoteData['anime']
    quote = '*' + quoteData['quote'] + '*' + '\n-***' + quoteData['character'] + '***'

    quoteEmbed = discord.Embed(title = quoteTitle, description = quote, color = THEME)
    quoteEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)

    await ctx.send(embed = quoteEmbed)

@client.command()
async def animesearch(ctx, *args):
    searchQuery = ' '.join(args)
    if not searchQuery:
        return await ctx.reply('Please enter a search query!')

    animeData = requests.get('https://kitsu.io/api/edge/anime?filter[text]=' + searchQuery).json()

    if animeData['meta']['count'] == 0:
        return await ctx.reply('Unfortunately, no results were found.')

    animeId          = animeData['data'][0]['id']
    animeURL         = 'https://kitsu.io/anime/' + animeId
    animeTitle       = animeData['data'][0]['attributes']['titles']['en_jp']
    animeThumbnail   = animeData['data'][0]['attributes']['posterImage']['large']
    animeDescription = animeData['data'][0]['attributes']['synopsis']
    animeEpisodes    = animeData['data'][0]['attributes']['episodeCount']
    animePopularity  = animeData['data'][0]['attributes']['popularityRank']
    animeRatings     = animeData['data'][0]['attributes']['averageRating']
    animeAirDate     = animeData['data'][0]['attributes']['startDate']
    animeEndDate     = animeData['data'][0]['attributes']['endDate']
    ageRating        = animeData['data'][0]['attributes']['ageRating']

    animeEmbed = discord.Embed(url = animeURL, title = animeTitle, description = animeDescription, color = THEME)
    animeEmbed.set_author(name = ctx.author.name + '#' + ctx.author.discriminator, icon_url = ctx.author.avatar_url)
    animeEmbed.set_thumbnail(url = animeThumbnail)
    animeEmbed.add_field(name = 'Total Episodes'  , value = animeEpisodes)
    animeEmbed.add_field(name = 'Popularity Rank' , value = animePopularity)
    animeEmbed.add_field(name = 'Ratings'         , value = animeRatings)
    animeEmbed.add_field(name = 'Air Date'        , value = animeAirDate)
    animeEmbed.add_field(name = 'End Date'        , value = animeEndDate)
    animeEmbed.add_field(name = 'Age Rating'      , value = ageRating)

    await ctx.send(embed = animeEmbed)
    
client.run(config['TOKEN'])