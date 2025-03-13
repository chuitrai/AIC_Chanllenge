import streamlit as st
from PIL import Image
from utils import MyFaiss, submit_tool 
import os
import pandas as pd

st.set_page_config(layout="wide")
st.title("Query Tools")

######################################
if 'cosine_faiss_vit32' not in st.session_state:
    bin_file = 'faiss_cosine.bin'
    json_path = 'database/keyframes_id.json'
    st.session_state['cosine_faiss_vit32'] = MyFaiss('B32' ,'', 'faiss_cosine_B32.bin', json_path)


csv_file_path = 'temp.csv' 
######################################
st.sidebar.header("Query Inputs")
query = st.sidebar.text_input("Nhập query:")
id = st.sidebar.text_input("Nhập id query:")
neighbor = st.sidebar.text_input("Nhập id neighbor:")
check_timer = st.sidebar.text_input("Nhập ảnh cần tra timer")
submit_image = st.sidebar.text_input("Nhập ảnh cần nộp")

######################################
query_button_vit32 = st.sidebar.button('Search VIT32')
id_button = st.sidebar.button('Search by ID Query')
neighbor_button = st.sidebar.button('Search neighbor')
save_ans = st.sidebar.button('check_timer')
qa_submit = st.sidebar.button('Q&A submit')
kis_submit = st.sidebar.button('KIS submit')
######################################
num_cols = 4
cols = st.columns(num_cols)

def display_images(image_paths, ids, scores=None):
    for i, image_path in enumerate(image_paths):
        img = Image.open(image_path)
        with cols[i % num_cols]:
            image_label = image_path.split("\\")[:-3:-1][-1::-1]
            image_label = '-'.join(image_label)
            st.image(img, caption=f"{image_label} - id: {ids[i]}", use_column_width=True)

cosine_faiss32= st.session_state['cosine_faiss_vit32']


if query and query_button_vit32:  
  scores, id_queries, infos_query, image_paths = cosine_faiss32.text_search(query, k=200)
  st.subheader("Results for Text Query")
  video_ans = [i.split('\\')[-2] for i in image_paths]
  keyframe_ans = [i.split('\\')[-1].split('.')[-2] for i in image_paths]
  df = pd.DataFrame({'video_ans': video_ans, 'keyframe_ans' : keyframe_ans})
  df.to_csv(csv_file_path, index=False, header=False)
  display_images(image_paths, id_queries, scores)

elif id and id_button:
  i_scores, id_queries, infos_query, image_paths = cosine_faiss32.image_search(id_query=int(id), k=100)
  st.subheader("Results for ID Query")
  video_ans = [i.split('\\')[-2] for i in image_paths]
  keyframe_ans = [i.split('\\')[-1].split('.')[-2] for i in image_paths]
  df = pd.DataFrame({'video_ans': video_ans, 'keyframe_ans' : keyframe_ans})
  df.to_csv(csv_file_path, index=False, header=False)
  display_images(image_paths, id_queries, i_scores)

elif neighbor and neighbor_button:
    image_paths, id_queries = cosine_faiss32.takeNeighbor(int(neighbor), k = 40)
    st.subheader("Results for neighbor")
    video_ans = [i.split('\\')[-2] for i in image_paths]
    keyframe_ans = [i.split('\\')[-1].split('.')[-2] for i in image_paths]
    df = pd.DataFrame({'video_ans': video_ans, 'keyframe_ans' : keyframe_ans})
    df.to_csv(csv_file_path, index=False, header=False)
    display_images(image_paths, id_queries)

elif save_ans and check_timer:
    file_timer = check_timer.split('-')[0]
    df = pd.read_csv('map-keyframes/' + f'{file_timer}.csv')
    fps = df['fps'][0]
    frame_idx_check = int(check_timer.split('-')[1].split('.')[0])
    result_timer = (frame_idx_check / fps) * 1000
    st.write(f'{check_timer}     :     {result_timer} ms')

elif submit_image and qa_submit:
  submit_json = submit_tool(image_path=submit_image, type='qa')
  st.write(submit_json)
elif submit_image and kis_submit:
  submit_json = submit_tool(image_path=submit_image, type='kis')
  st.write(submit_json)