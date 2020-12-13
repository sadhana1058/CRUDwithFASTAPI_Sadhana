from fastapi import FastAPI
from channelmodel import Channel,db

app = FastAPI()

#this end point gets list of all channel that 
@app.get('/channels')
async def list_channels():
    channels_list = []
    for channel in db.channels_list.find():
        #channels_list.append(Channel(**channel))
        cc=dict(list(Channel(**channel)))
        print(cc,type(cc))
        if (cc['type']=="public"):
            channels_list.append(Channel(**channel))
        #for c in cc:
            # for i,j in c:
            #     if i == 'type' and j=='public':
        #print(c,type(c))
    return {'channels_list': channels_list}

# @app.get('/channels/')
# async def public_channels():
#     public_c = []
#     for channel in db.channels_list.find():
#     #     public_c.append(Channel(**channel))
#     # return {'public_channels': public_c}

@app.post('/channels_list')
async def create_channel(channel: Channel):
    if hasattr(channel, 'id'):
        delattr(channel, 'id')
    ret = db.channels_list.insert_one(channel.dict(by_alias=True))
    channel.id = ret.inserted_id
    return {'channel': channel}


@app.delete("/channels/{id}", response_description="Delete channel")
async def delete_channel(id: str):
    print("id ------->",id)
    for channel in db.channels_list.find():
        dd=dict(list(Channel(**channel)))
        print(dd['id'],type(dd['id']))
        if (dd['id']==id):
            print("deleted it")
            db.channels_list.delete_one(Channel(**channel))
    return "deleted t successfully"
    # if hasattr(channel, 'id'):
    #    delattr(channel, 'id')
    # ret = db.channels_list.insert_one(channel.dict(by_alias=True))
    # channel.id = ret.inserted_id
    # return {'channel': channel}