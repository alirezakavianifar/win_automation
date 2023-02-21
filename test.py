from helpers import connect_to_sql
from fastapi import FastAPI
import json
import moviepy.editor as mp

video_path = r'E:\Tutorials\self-adaptive\resiliance talk\Resilience Talk 3 - Uncertainty in self-adaptive systems... Danny Weyns, KU Leuven.mp4'
video = mp.VideoFileClip(video_path)

audio = video.audio
audio.write_audiofile(video_path + 'my_audio.mp3')


app = FastAPI()

sql_query = 'SELECT * FROM tblTgju'
data = connect_to_sql(sql_query=sql_query, connect_type='none',
                      read_from_sql=True, return_df=True)
out = data.to_json(orient="records")
parsed = json.loads(out)
print('stop')


@app.get("/")
def read_root():
    return parsed
