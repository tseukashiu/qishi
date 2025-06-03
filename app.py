import streamlit as st
from zhipuai import ZhipuAI

# 初始化 Zhipu 客户端（建议用环境变量方式处理 key）
#原来是client_zp =  ZhipuAI(api_key="your API key")
client_zp = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])

# 分析函数
def get_discrimination_level(text):
    completion = client_zp.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": "### 定位：语义歧视分析专家\n ### 任务：请对用户输入的句子进行歧视性分析，并用 1 到 5 之间的数字表示其歧视程度。1 表示没有歧视，5 表示极为歧视。\n ###输出 ：只输出数字，不需要额外解释。"},
            {"role": "user", "content": f"{text}"}
        ]
    )
    return completion.choices[0].message.content

def tiaozheng(text):
    completion = client_zp.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": "### 定位：语言表述专家\n ### 任务：将具有歧视倾向或敏感表达的语句，转化为一种更抽象、隐晦的调侃方式，使其不再直接指向具体群体，从而弱化其中的攻击性与严肃性，让整体话语呈现出一种讽刺而非冒犯的语气。\n ###输出 ：只输出调整后的句子，不需要额外解释。"},
            {"role": "user", "content": text}
      ]
    )

    return completion.choices[0].message.content


# Streamlit 页面设置
st.set_page_config(page_title="语义歧视分析器", layout="centered")
st.title("🧠 语义歧视分析小工具")

# 用户输入句子
user_input = st.text_area("请输入要分析的句子：", height=100)



# 当用户点击按钮时进行分析
if st.button("开始分析"):
    if user_input.strip() == "":
        st.warning("请输入一句话再分析哦。")
    else:
        with st.spinner("正在分析中...",  show_time=True):
            try:
                score = get_discrimination_level(user_input)
                st.success(f"🧾 歧视程度评分：**{score}**（1~5）")

                if score != "1":
                    try:
                        result = tiaozheng(user_input)
                        st.success(f"调整语气后的句子：{result}")
                    except Exception as e:
                        st.error("出错了，请稍后再试😂")

            except Exception as e:
                st.error("出错了，请稍后再试😂")
