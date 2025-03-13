import numpy as np
import glob
import json
import os
import re

class File4Faiss:
  def __init__(self, root_database: str):
    self.root_database = root_database

  def re_shot_list(self, shot_list, id, k):
    len_lst = len(shot_list)
    if k>=len_lst or k == 0:
      return shot_list

    shot_list.sort()
    index_a = shot_list.index(id)

    index_get_right = k // 2
    index_get_left = k - index_get_right

    if index_a - index_get_left < 0:
      index_get_left = index_a
      index_get_right = k - index_a
    elif index_a + index_get_right >= len_lst:
      index_get_right = len_lst - index_a - 1
      index_get_left = k - index_get_right

    output = shot_list[index_a - index_get_left: index_a] + shot_list[index_a: index_a + index_get_right + 1]
    return output

  def write_json_file(self, json_path: str, shot_frames_path: str, option='full'):
    count = 0
    self.infos = []
    des_path = os.path.join(json_path, "keyframes_id.json")
    video_paths = sorted(glob.glob(r"C:\Users\ADMIN\Desktop\AIC_2024\KeyFrames\*"))
    
    for video_path in video_paths:
      
        #print(video_path)
      image_paths = sorted(glob.glob(f'{video_path}\\*.jpg'))
      id_keyframes = np.array([int(id.split('\\')[-1].replace('.jpg', '')) for id in image_paths])

      ###### Get scenes from video_path ######
      video_info = video_path.split('\\')[-1]

      # with open(f'{shot_frames_path}/{video_info}.txt', 'r') as f:
      #   lst_range_shotes = f.readlines()
      # lst_range_shotes = np.array([re.sub('\[|\]', '', line).strip().split(' ') for line in lst_range_shotes]).astype(np.uint32)
      lst_range_shotes = np.loadtxt(f'{shot_frames_path}/{video_info}.txt').astype(np.uint32)
      for im_path in image_paths:
        # im_path = 'Database/' + '/'.join(im_path.split('/')[-3:])
        id = int(im_path.split('\\')[-1].replace('.jpg', ''))
        i = 0
        flag = 0
        for range_shot in lst_range_shotes:
          i+=1
          first, end = range_shot

          if first <= id <= end:
            break

          if i == len(lst_range_shotes):
            flag=1

        if flag == 1:
          print(f"Skip: {im_path}")
          print(first, end)
          continue

        ##### Get List Shot ID #####
        lst_shot = id_keyframes[np.where((id_keyframes>=first) & (id_keyframes<=end))]
        lst_shot = self.re_shot_list(list(lst_shot), id, k=6)
        lst_shot = [f"{i:0>6d}" for i in lst_shot]

        ##### Get List Shot Path #####
        lst_shot_path = []
        for id_shot in lst_shot:
          info_shot = {
              "shot_id": id_shot,
              "shot_path": '\\'.join(im_path.split('\\')[:-1]) + f"/{id_shot}.jpg"
          }
          lst_shot_path.append(info_shot)

        ##### Merge All Info #####
        info = {
                "image_path": im_path,
                "list_shot_id": lst_shot,
                "list_shot_path": lst_shot_path
                }

        if option == 'full':
          self.infos.append(info)
        else:
          if id == (end+first)//2:
            self.infos.append(info)

        count += 1

    id2img_fps = dict(enumerate(self.infos))

    with open(des_path, 'w') as f:
      f.write(json.dumps(id2img_fps))

    print(f'Saved {des_path}')
    print(f"Number of Index: {count}")

  def load_json_file(self, json_path: str):
    with open(json_path, 'r') as f:
      js = json.loads(f.read())

    return {int(k):v for k,v in js.items()}

create_file = File4Faiss(r'C:\Users\ADMIN\Desktop\AIC_2024\database')
create_file.write_json_file(json_path=r'C:\Users\ADMIN\Desktop\AIC_2024\database', shot_frames_path="database/scenes_txt")
