import streamlit as st
from streamlit_javascript import st_javascript

def run_javascript():
    js_code = """
    {function initTimer(periodInSeconds) {
        var end = Date.now() + periodInSeconds * 1000;
        var x = window.setInterval(function() {
            var timeLeft = Math.floor((end - Date.now()) / 1000);
            if(timeLeft < 0) { clearInterval(x); return; }
            document.getElementById('timer').innerHTML = '00:' + (timeLeft < 10 ? '0' + timeLeft : timeLeft);
        }, 200);
    }
    initTimer(10);
    return 'Timer started';}
    """
    result = st_javascript(js_code)
    st.write(result)

if st.button('Start Timer'):
    run_javascript()

st.markdown('<div id="timer"></div>', unsafe_allow_html=True)
