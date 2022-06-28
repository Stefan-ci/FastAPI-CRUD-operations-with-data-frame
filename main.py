import json, pathlib
from models import Track
from typing import Union
from pandas import json_normalize
from fastapi import FastAPI, Response






app = FastAPI()
data = []






@app.on_event('startup')
async def startup_event():
    datapath = pathlib.Path() / 'data' / 'tracks.json'
    with open(datapath, 'r') as f:
        tracks = json.load(f)
        for track in tracks:
            data.append(Track(**track).dict())
        


        


@app.get('/')
def home():
    return {'message':'Home page ....'}






@app.get('/tracks/', response_model=Union[Track, str, dict])
def tracks():
    if len(data) == 0:
        return {'tracks':[]}
    return {'track':data}






@app.get('/tracks/{track_id}/', response_model=Union[Track, str, dict])
def track(track_id: int, response: Response):
    track = None
    for t in data:
        if t['id'] == track_id:
            track = t
            break
    if track is None:
        response.status_code = 404
        return {'message':'Track does not exist'}
    
    return {'track':track}






@app.post('/tracks/', response_model=Union[Track, str, dict], status_code=201)
def create_track(track: Track):
    track_dict = track.dict() 
    track_dict['id'] = max(data, key=lambda x: x['id']).get('id') + 1
    data.append(track_dict)
    return {'track':track_dict}






@app.put('/tracks/{track_id}/', response_model=Union[Track, str, dict])
def track(track_id: int, upadated_track: Track, response: Response):
    track = None
    for t in data:
        if t['id'] == track_id:
            track = t
            break
    if track is None:
        response.status_code = 404
        return {'message':'Track does not exist'}
    
    for key, val in upadated_track.dict().items():
        if key != 'id':
            track[key] = val
    
    return {'track':track}






@app.delete('/tracks/{track_id}/')
def track(track_id: int, response: Response):
    track_index = None
    for idx, t in enumerate(data):
        if t['id'] == track_id:
            track_index = idx
        
    if track_index is None:
        response.status_code = 404
        return {'message':'Track does not exist'}
    
    del data[track_index]
    return {'message':'Track successfully deleted ...'}






# creating a .csv file to store all tracks
df = json_normalize(data)
df.to_csv('tracks.csv')
