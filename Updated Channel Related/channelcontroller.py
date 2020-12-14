from fastapi import FastAPI,HTTPException
from channelmodel import Channel,db
from bson import ObjectId

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
    return {'channels_list': channels_list}


@app.post('/channels_list')
async def create_channel(channel: Channel):
    if hasattr(channel, 'id'):
        delattr(channel, 'id')
    ret = db.channels_list.insert_one(channel.dict(by_alias=True))
    channel.id = ret.inserted_id
    return {'channel': channel}

class Error(Exception):
    """Base class for other exceptions"""
    pass

class RandomError(Error):
    """Raised when the channel is not found"""
    pass

@app.delete("/channels/{id}", response_description="Delete channel")
async def delete_channel(id: str):
    try:
        #print(id)
        x=db.channels_list.delete_one({"_id":ObjectId(id)})
        print(x.deleted_count)
        if x.deleted_count==0:
            raise  RandomError
        else:
            return("successfully deleted")

    except RandomError:
        print("Channel not found")
        return "Channel not found"
    