import json

frame = {'timestamp':0.015,'movement':'type_2'}
with open('frames.jsonlines', 'a', encoding='utf-8') as file:
    json.dump(frame, file)
    file.write('\n')