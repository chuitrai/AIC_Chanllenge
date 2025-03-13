import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np

def draw_app():
    if st.session_state.show_whiteboard:
        st.sidebar.title("Whiteboard Settings")
        
        # Add additional controls to the new sidebar
        stroke_width = st.sidebar.slider("Stroke width: ", 1, 25, 3)
        stroke_color = st.sidebar.color_picker("Stroke color: ", "#000000")
        bg_color = st.sidebar.color_picker("Background color: ", "#FFFFFF")
        drawing_mode = st.sidebar.radio(
            "Select drawing mode:",
                options=["✏️ Free Draw", "◼️ Rectangle", "🔵 Circle", "📏 Line", "🔄 Transform"],
        )

        drawing_mode_map = {
                "✏️ Free Draw": "freedraw",
                "◼️ Rectangle": "rect",
                "🔵 Circle": "circle",
                "📏 Line": "line",
                "🔄 Transform": "transform"
            }
            
        selected_drawing_mode = drawing_mode_map[drawing_mode]
            
        description = st.text_input("Description: ")

        canvas_result = st_canvas(
            fill_color=bg_color,  # Fixed fill color with some opacity
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color="#ffffff",
            update_streamlit=True,
            height=426,
            width=640,
            drawing_mode=selected_drawing_mode,
            key="canvas",
        )


        submit_button = st.button("Submit")
        if submit_button:
            st.session_state.show_whiteboard = False
            img = Image.fromarray(np.uint8(canvas_result.data))
            st.write(canvas_result.image_data)
            return img, description
            
        