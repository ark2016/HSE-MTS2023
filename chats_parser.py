from telethon.sync import TelegramClient
from parser_info import api_id,api_hash,phone
import pandas as pd
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetHistoryRequest

emotions=[""]
table = pd.DataFrame()

api_id = api_id
api_hash = api_hash
phone = phone

client = TelegramClient(phone, api_id, api_hash)

client.start()

chats = []
last_date = None
size_chats = 200
groups=[]

result = client(GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=size_chats,
            hash = 0
        ))

chats.extend(result.chats)


for chat in chats:
   try:
       if chat.megagroup==True:
           groups.append(chat)
   except:
       continue


print('Выберите номер группы из перечня:')
i=0

neeed_group_name='Матч! Чат'
g_index=0

for g in groups:
   print(str(i) + '- ' + g.title)
   if g.title==neeed_group_name:
       g_index = i
   i += 1

g_index = input("Введите нужную цифру: ")

target_group=groups[int(g_index)]


print(target_group)
print(target_group.title)


all_messages = []
messages_posts=[]
offset_id = 0
limit = 200
total_messages = 0
total_count_limit = 0

table = pd.DataFrame()
emotions = ['👍','❤️','✌️','👎','👌','👏','💅','🖕','😆','😁','😊','🥰','🤩','🤔','🤬','💀','🔥']

while(True):
    history = client(GetHistoryRequest(
           peer=target_group,
           offset_id=offset_id,
           offset_date=None,
           add_offset=0,
           limit=limit,
           max_id=0,
           min_id=0,
           hash=0
       ))
    if not history.messages:
        break

    messages = history.messages

    for message in messages:
        total_messages+=1
        try:
            if message.from_id.channel_id:
                print("Это сообщение с канала")
                all_messages.append(message.message)
                messages_posts.append(message.message)
        except:
            continue
        id = message.id
        text = message.message
        replies = message.replies
        views = message.views
        if views==None:
            continue
        forward = message.forwards
        user_id = message.from_id
        reaction = message.reactions
        replies_massiv = []
        dataline = {"from_id": message.from_id, "text": text, "views": message.views, "reposts": message.forwards}
        emcount = [0] * len(emotions)

        if reaction != None:
            for k in message.reactions.results:
                try:
                    emcount[emotions.index(k.reaction.emoticon)] = k.count
                except:
                    continue

        for i, val in enumerate(emotions):
            dataline[val] = emcount[i]

        if replies != None and replies.replies > 0:
            print("  ")
            print(message)
            for k in messages:
                if k.reply_to != None:
                    reply = k.reply_to
                    if reply.reply_to_msg_id == id and k.message != '':
                        replies_massiv.append(k.message)
                        print("вот коментЖ " + k.message)
        dataline["comments"] = replies_massiv
        row = pd.DataFrame([dataline])
        table = pd.concat([table, row], ignore_index=True)
    print(total_messages)
    offset_id = messages[len(messages) - 1].id
    if total_count_limit != 0 and total_messages >= total_count_limit:
        break
    table.to_csv("comments_base.csv", sep='\t')
