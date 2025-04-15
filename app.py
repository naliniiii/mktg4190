import streamlit as st
import openai
from datetime import datetime
import pytz
import base64
import requests

st.set_page_config(
    page_title="Universal Fortune Teller",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&display=swap');
    
    .main-title {
        font-family: 'Ma Shan Zheng', cursive;
        color: #D4AF37;
        font-size: 2.8em;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 25px;
    }
    
    h3 {
        font-family: 'Ma Shan Zheng', cursive;
        color: #D4AF37;
        font-size: 1.4em;
        margin-top: 15px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    .stTextInput input, .stDateInput input, .stTimeInput input, .stSelectbox select, .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid #D4AF37;
        border-radius: 5px;
        padding: 8px;
        color: #000;
        font-size: 1em;
    }
    
    .stButton button {
        background-color: #8B0000;
        color: #FFD700;
        font-family: 'Ma Shan Zheng', cursive;
        font-size: 1.1em;
        padding: 10px 30px;
        border: none;
        border-radius: 5px;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #A52A2A;
        border: 2px solid #FFD700;
        transform: translateY(-2px);
    }
    
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("https://wallpaperaccess.com/full/2366958.jpg");
        background-size: cover;
        background-attachment: fixed;
        color: #FFD700;
    }
    
    p, div {
        color: #FFD700;
        font-size: 1em;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes glowingBorder {
        0% { box-shadow: 0 0 5px #D4AF37; }
        50% { box-shadow: 0 0 20px #D4AF37; }
        100% { box-shadow: 0 0 5px #D4AF37; }
    }
    
    .analysis-box {
        background-color: rgba(0, 0, 0, 0.7);
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #D4AF37;
        margin: 20px 0;
        animation: fadeInUp 0.8s ease-out forwards, glowingBorder 2s infinite;
        position: relative;
        overflow: hidden;
        font-size: 1em;
    }
    
    .analysis-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(212,175,55,0.1) 0%, rgba(0,0,0,0) 70%);
        animation: rotate 4s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .input-description {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #D4AF37;
        margin-bottom: 25px;
        font-size: 1em;
    }
</style>
""", unsafe_allow_html=True)

# ... existing code ...

def autoplay_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        audio_tag = f'<audio autoplay loop style="display:none"><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>'
        st.markdown(audio_tag, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error playing audio: {str(e)}")

# Update layout to be more story-like
st.markdown('<h1 class="main-title">🏮 命运之书 The Book of Destiny 🏮</h1>', unsafe_allow_html=True)

# Add mystical intro
st.markdown("""
    <div style='text-align: center; padding: 20px; margin-bottom: 30px; font-style: italic; color: #FFD700;'>
        古老的智慧在召唤着你... 命运的书页正在翻开...
        <br><br>
        Ancient wisdom calls to you... The pages of destiny are turning...
    </div>
""", unsafe_allow_html=True)

autoplay_audio("C:\\Users\\nalin\\Desktop\\University\\Year 4 Term 2\\MKTG4190\\projectx\\whispers.mp3")

# ... rest of the code ...

class LLMInterface:
    def __init__(self, api_key, provider='deepseek'):
        self.api_key = api_key
        self.provider = provider

    def generate_response(self, prompt):
        try:
            if self.provider == 'deepseek':
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'model': 'deepseek-chat',
                    'messages': [{'role': 'user', 'content': prompt}]
                }
                response = requests.post('https://api.deepseek.com/v1/chat/completions', headers=headers, json=data)
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                else:
                    return f"Error: API returned status code {response.status_code}"
            elif self.provider == 'openai':
                openai.api_key = self.api_key
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content
            else:
                return "Provider not supported. Please use 'deepseek' or 'openai'"
        except Exception as e:
            return f"Error generating response: {str(e)}"

st.markdown('<h1 class="main-title">🏮 Universal Fortune Teller 命运占卜 🏮</h1>', unsafe_allow_html=True)

api_key = 'sk-c1ec12e696f844909bb2a9ae05ab8144'
provider = 'deepseek'

col1, col2 = st.columns([2, 1])  # Changed column ratio

with col1:
    st.markdown("### 🌟 探索生命之源 Journey to Your Origins")
    st.markdown("""
        <div class="input-description">
            在东方传统中，每个人降生的时刻都蕴含着独特的天机。让我们一起探索您的命盘...
            <br><br>
            In Eastern tradition, the moment of your birth holds the key to understanding your destiny...
        </div>
    """, unsafe_allow_html=True)
    
    birth_date = st.date_input("🌅 您降临人间的日子 Your Day of Arrival:", 
                              min_value=datetime(1950, 1, 1),
                              max_value=datetime.now())
    birth_time = st.time_input("⏰ 您诞生的时辰 The Hour of Your Birth:")
    timezone = st.selectbox("🌍 您出生地的时区 Your Birth Place Timezone:", pytz.all_timezones)

with col2:
    st.markdown("### 🔮 问道玄机 Seek Your Destiny")
    st.markdown("""
        <div class="input-description">
            八字蕴含无尽天机，您想探索什么样的人生奥秘？
            <br><br>
            Your BaZi chart holds infinite wisdom. What mysteries of life do you wish to uncover?
        </div>
    """, unsafe_allow_html=True)
    user_input = st.text_area('📝 请书写您的问题 Write your question:', height=100)

if st.button('寻求天命 Unveil Your Destiny 🔮'):
    with st.spinner('正在沟通天地玄机 Consulting the cosmic forces...'):
        try:
            birth_datetime = datetime.combine(birth_date, birth_time)
            tz = pytz.timezone(timezone)
            birth_datetime = tz.localize(birth_datetime)
            
            birth_info = f"Birth Date: {birth_date.strftime('%Y-%m-%d')}\nBirth Time: {birth_time.strftime('%H:%M')}\nTimezone: {timezone}"
            
            llm = LLMInterface(api_key, provider)
            bazi_prompt = f"""Based on the following birth information, please provide a detailed analysis in the following format:

1. First, provide the 生辰八字 (Chinese Zodiac and Ba Zi) in Chinese characters along with the English explanation
2. Then, explain in English what each component means:
   - The Year Pillar (年柱)
   - The Month Pillar (月柱)
   - The Day Pillar (日柱)
   - The Hour Pillar (时柱)
3. Finally, provide a brief explanation of what these elements reveal about the person's character and destiny

Birth Information:
{birth_info}"""
            bazi_response = llm.generate_response(bazi_prompt)
            
            st.markdown("### 🎴 八字分析 Your Birth Chart Analysis")
            st.markdown('<div class="analysis-box">' + bazi_response + '</div>', unsafe_allow_html=True)
            
            if user_input:
                st.markdown("### 🎯 天机解读 Your Fortune")
                fortune_prompt = f"""Based on the following birth information and birth chart analysis:
{birth_info}

And the user's question: {user_input}

Please provide a detailed fortune analysis that:
1. Explains how the birth chart elements influence the answer to the specific question
2. Provides practical advice and insights
3. Includes both traditional Chinese wisdom and modern interpretation

Please format the response in a clear, easy-to-understand manner with sections for different aspects of the analysis."""
                fortune_response = llm.generate_response(fortune_prompt)
                st.markdown('<div class="analysis-box">' + fortune_response + '</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")