#Title: SketchYourself
#Developer: Vishwas Puri
#Purpose: A program that uses your live webcam to process your image with different filters like cartoon, edges, coloured and more...

#This program is made using python supported by streamlit.

import streamlit as st
import cv2
from streamlit_webrtc import (
    AudioProcessorBase,
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)
st.set_page_config(layout="wide")
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
import av

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.write("Press start to turn on camera and select the type of filter from the dropdown!")
def sketchYourself():
    class OpenCVVideoProcessor(VideoProcessorBase):
        type: Literal["null", "Cartoon", "Edges"]

        def __init__(self) -> None:
            self.type = "mask"

        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")

            if self.type == "null":
                pass

            elif self.type == "Cartoon":
                #converting image to cartoon using multiple filters
                img_color = cv2.pyrDown(cv2.pyrDown(img))
                for _ in range(6):
                    img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
                img_color = cv2.pyrUp(cv2.pyrUp(img_color))

                img_edges = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                img_edges = cv2.adaptiveThreshold(
                    cv2.medianBlur(img_edges, 7),
                    255,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY,
                    9,
                    2,
                )
                img_edges = cv2.cvtColor(img_edges, cv2.COLOR_GRAY2RGB)

                # combine color and edges
                img = cv2.bitwise_and(img_color, img_edges)
            elif self.type == "Edges":
                # perform edge detection
                img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            elif self.type == "Green-Effect":
                #converting image to HLS Filter
                img = cv2.cvtColor(img,cv2.COLOR_BGR2HLS)

            elif self.type == "Blue-Effect":
                #converting image to LAB Filter
                img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

            elif self.type == "Red-Effect":
                #converting image to HSV Filter
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            elif self.type == "Blurred":
                #blurring image
                img = cv2.blur(img, (20,20))

            elif self.type == "Light":
                #converting image to XYZ Filter
                img = cv2.cvtColor(img, cv2.COLOR_BGR2XYZ)

            elif self.type == "Pencil Sketch":
                #convert image to a colered pencil sketch filter
                sk_gray, img = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)

            elif self.type == "Dark":
                #converting to no-bits image
                img = cv2.bitwise_not(img)

            return av.VideoFrame.from_ndarray(img, format="bgr24")

    # setting up streamlit camera configuration
    webrtc_ctx = webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=OpenCVVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        video_html_attrs={
            "style": {"margin": "0 auto", "border": "5px yellow solid"},
            "controls": False,
            "autoPlay": True,
        },
    )

    #dropdown of options of filters
    if webrtc_ctx.video_processor:
        webrtc_ctx.video_processor.type = st.selectbox(
            "", ("Select Sketch Type", "Cartoon", "Edges","Green-Effect","Blue-Effect", "Red-Effect", "Blurred", "Pencil Sketch", "Dark","Light")
        )

    # Info Block
    st.write("If camera doesn't turn on, please ensure that your camera permissions are on!")
    with st.expander("Steps to enable permission"):
        st.write("1. Click the lock button at the top left of the page")
        st.write("2. Slide the camera slider to on")
        st.write("3. Reload your page!")


if __name__ == "__main__":
   sketchYourself()
