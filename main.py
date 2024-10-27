import os
import discord
import pytz
from discord.ext import commands
from datetime import datetime
from myserver import server_on


intents = discord.Intents.default()
intents.guilds = True  # เปิด intents สำหรับเหตุการณ์ในห้องเสียง
intents.voice_states = True  # เปิด intents สำหรับเหตุการณ์ในห้องเสียง

bot = commands.Bot(command_prefix="-", intents=intents)

# Dictionary เก็บเวลาการเข้าและออกของผู้ใช้
voice_log = {}

# ID ของช่องข้อความที่คุณต้องการให้บอทส่งข้อความ
TEXT_CHANNEL_ID = 1300116422105501787  # แทนที่ด้วย ID ของช่องข้อความ

@bot.event
async def on_voice_state_update(member, before, after):
    user_id = member.id
    current_time = datetime.now(pytz.timezone('Asia/Bangkok'))
    channel = bot.get_channel(TEXT_CHANNEL_ID)  # รับช่องข้อความที่กำหนด

    # แยกวันที่และเวลา
    date_str = current_time.strftime("%d-%m-%Y")
    time_str = current_time.strftime("%H:%M:%S")

    if before.channel is None and after.channel is not None:  # เข้าห้องเสียง
        voice_log[user_id] = {'join_time': current_time}
        message = f"{member} เข้าห้อง {after.channel.name} วันที่ {date_str} เวลา {time_str}"
        print(message)
        await channel.send(message)  # ส่งข้อความไปยังช่องข้อความ

    elif before.channel is not None and after.channel is None:  # ออกจากห้องเสียง
        leave_time = datetime.now(pytz.timezone('Asia/Bangkok'))
        leave_date_str = leave_time.strftime("%d-%m-%Y")
        leave_time_str = leave_time.strftime("%H:%M:%S")
        
        join_time = voice_log.get(user_id, {}).get('join_time')
        
        if join_time:
            duration = leave_time - join_time
            duration_seconds = duration.total_seconds()
            hours = int(duration_seconds // 3600)
            minutes = int((duration_seconds % 3600) // 60)
            seconds = int(duration_seconds % 60)
            message = (f"{member} ออกจากห้อง {before.channel.name} เวลา {leave_date_str} เวลา {leave_time_str} "
                       f"อยู่ในห้อง {hours} ชั่วโมง {minutes} นาที {seconds} วินาที")
            print(message)
            await channel.send(message)  # ส่งข้อความไปยังช่องข้อความ
            # ลบข้อมูลที่เก็บไว้หลังออกจากห้องเสียง
            del voice_log[user_id]

    elif before.channel is not None and after.channel is not None and before.channel != after.channel:  # ย้ายห้องเสียง
        message = f"{member} ย้ายจากห้อง {before.channel.name} ไปยังห้อง {after.channel.name}"
        print(message)
        await channel.send(message)  # ส่งข้อความไปยังช่องข้อความ

server_on()
bot.run(os.getenv('TOKEN'))