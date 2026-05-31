import discord
import asyncio
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True

client = discord.Client(intents=intents)

voice_client = None


async def connect_voice():
    global voice_client

    await client.wait_until_ready()

    channel = client.get_channel(CHANNEL_ID)

    if not channel:
        print("❌ Channel not found")
        return

    # إذا موجود اتصال قديم افصله
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()

    try:
        voice_client = await channel.connect(self_deaf=True, self_mute=True)
        print(f"🔊 Joined {channel.name}")
    except Exception as e:
        print("⚠️ Error connecting:", e)


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    await connect_voice()

    # مراقبة مستمرة
    while True:
        await asyncio.sleep(20)

        if not voice_client or not voice_client.is_connected():
            print("♻️ Reconnecting...")
            await connect_voice()


@client.event
async def on_voice_state_update(member, before, after):
    global voice_client

    if member.id == client.user.id:
        if after.channel is None:
            await asyncio.sleep(2)
            await connect_voice()


client.run(TOKEN)
