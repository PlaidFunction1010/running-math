import streamlit as st
import sympy as sp

from decimal import (
    Decimal,
    InvalidOperation,
)

from pathlib import Path


from modules.binomial_basic import (
    QUESTION_GENERATORS as BINOMIAL_BASIC_GENERATORS,
)

from modules.binomial_last_digits import (
    QUESTION_GENERATORS as BINOMIAL_LAST_DIGITS_GENERATORS,
)

from modules.binomial_series import (
    QUESTION_GENERATORS as BINOMIAL_SERIES_GENERATORS,
)

from utils.answer_checker import (
    check_expression,
    check_integer,
)


# ==================================================
# 網站設定
# ==================================================

st.set_page_config(
    page_title="Running Math",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ==================================================
# CSS
# ==================================================

def load_css():

    css_path = (
        Path(__file__).parent
        / "styles"
        / "main.css"
    )

    if css_path.exists():

        with open(
            css_path,
            "r",
            encoding="utf-8",
        ) as file:

            css = file.read()

        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )


load_css()


# ==================================================
# 題庫設定
# ==================================================

TOPICS = {

    "二項式定理－基本練習": {

        "unit": "排列組合",

        "generators":
            BINOMIAL_BASIC_GENERATORS,

        "question_names": [
            "1｜二項式完整展開",
            "2｜含分式的二項式展開",
            "3｜求 xᵏyᵗ 的係數",
            "4｜求 xᵏ 的係數",
            "5｜含正負次方的係數",
        ],
    },

    "二項式定理－末位數練習": {

        "unit": "排列組合",

        "generators":
            BINOMIAL_LAST_DIGITS_GENERATORS,

        "question_names": [
            "1｜整數冪末位數",
            "2｜接近 1 的小數冪",
        ],
    },

    "二項式定理－級數": {

        "unit": "排列組合",

        "generators":
            BINOMIAL_SERIES_GENERATORS,

        "question_names": [
            "1｜基本組合級數求和",
            "2｜對稱性求部分偶數項和",
            "3｜奇數／偶數下標係數和",
            "4｜帶等比權重的二項式級數",
        ],
    },

}


# ==================================================
# Session State
# ==================================================

if "font_size" not in st.session_state:
    st.session_state.font_size = "中"

if "topic" not in st.session_state:
    st.session_state.topic = (
        "二項式定理－基本練習"
    )

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "question" not in st.session_state:
    st.session_state.question = None


# ==================================================
# 共用函式
# ==================================================

def clear_answers():

    keys_to_delete = [
        key
        for key in st.session_state.keys()
        if (
            key.startswith("answer_")
            or key.startswith("choice_")
        )
    ]

    for key in keys_to_delete:
        del st.session_state[key]


def new_question():

    topic_data = TOPICS[
        st.session_state.topic
    ]

    generator = topic_data[
        "generators"
    ][
        st.session_state.question_index
    ]

    st.session_state.question = (
        generator()
    )


# ==================================================
# 特殊答案判定
# ==================================================

def check_last_digits(
    student_answer,
    correct_answer,
):

    try:

        text = str(
            student_answer
        ).strip()

        if not text:
            return False, "請輸入答案"

        if not text.isdigit():
            return (
                False,
                "請輸入非負整數",
            )

        return (
            int(text)
            == int(correct_answer),
            None,
        )

    except Exception:

        return (
            False,
            "無法辨識答案",
        )


def check_decimal_3(
    student_answer,
    correct_answer,
):

    try:

        text = str(
            student_answer
        ).strip()

        if not text:
            return False, "請輸入答案"

        student_value = Decimal(
            text
        )

        return (
            student_value
            == correct_answer,
            None,
        )

    except (
        InvalidOperation,
        ValueError,
    ):

        return (
            False,
            "請輸入有效的小數",
        )


def check_numeric_expression(
    student_answer,
    correct_answer,
):
    """
    級數題答案判定。

    接受：
    2^8-1
    2**8-1
    255

    並用 SymPy 做等價判定。
    """

    try:

        text = str(
            student_answer
        ).strip()

        if not text:
            return False, "請輸入答案"

        text = text.replace(
            "^",
            "**",
        )

        student_expr = sp.sympify(
            text
        )

        difference = sp.simplify(
            student_expr
            - sp.Integer(correct_answer)
        )

        return (
            difference == 0,
            None,
        )

    except Exception:

        return (
            False,
            "無法辨識你輸入的答案",
        )


# ==================================================
# Header
# ==================================================

st.markdown(
    """
    <div class="rm-header">
        <div class="rm-title">
            📐 Running Math
        </div>
        <div class="rm-subtitle">
            高中數學隨機練習
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 字體大小
# ==================================================

font_col_1, font_col_2 = st.columns(
    [3, 2]
)


with font_col_1:

    st.markdown(
        "**閱讀設定**"
    )


with font_col_2:

    selected_font = st.segmented_control(
        "字體大小",
        options=[
            "小",
            "中",
            "大",
        ],
        default=st.session_state.font_size,
        label_visibility="collapsed",
    )


if selected_font:

    st.session_state.font_size = (
        selected_font
    )


# ==================================================
# 動態字體 CSS
# ==================================================

FONT_SETTINGS = {

    "小": {
        "base": 16,
        "label": 15,
        "input": 16,
        "button": 16,
        "math": 21,
    },

    "中": {
        "base": 20,
        "label": 18,
        "input": 19,
        "button": 18,
        "math": 27,
    },

    "大": {
        "base": 24,
        "label": 21,
        "input": 22,
        "button": 21,
        "math": 34,
    },

}


font = FONT_SETTINGS[
    st.session_state.font_size
]


st.markdown(
    f"""
    <style>

    div[data-testid="stMarkdownContainer"] p {{
        font-size: {font["base"]}px !important;
        line-height: 1.75 !important;
    }}

    div[data-testid="stMarkdownContainer"] li {{
        font-size: {font["base"]}px !important;
        line-height: 1.7 !important;
    }}

    div[data-testid="stMarkdownContainer"] h3 {{
        font-size: {font["base"] + 5}px !important;
    }}

    div[data-testid="stMarkdownContainer"] h4 {{
        font-size: {font["base"] + 3}px !important;
    }}

    div[data-testid="stRadio"] label p {{
        font-size: {font["base"]}px !important;
    }}

    div[data-baseweb="select"] > div {{
        font-size: {font["base"]}px !important;
        min-height: 48px;
    }}

    div[data-testid="stTextInput"] input {{
        font-size: {font["input"]}px !important;
        min-height: 52px !important;
        padding: 10px 14px !important;
    }}

    div[data-testid="stButton"] button {{
        font-size: {font["button"]}px !important;
        min-height: 50px !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stAlert"] p {{
        font-size: {font["base"]}px !important;
    }}

    div[data-testid="stMarkdownContainer"]
    mjx-container[display="true"] {{
        font-size: {font["math"]}px !important;
        overflow-x: auto !important;
        overflow-y: hidden !important;
        padding-top: 8px;
        padding-bottom: 8px;
    }}

    div[data-testid="stLatex"] {{
        font-size: {font["math"]}px !important;
        overflow-x: auto !important;
    }}

    @media (max-width: 640px) {{

        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        div[data-testid="stMarkdownContainer"]
        mjx-container[display="true"] {{
            overflow-x: auto !important;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 單元
# ==================================================

current_unit = TOPICS[
    st.session_state.topic
]["unit"]


st.markdown(
    f"""
    <div class="rm-unit-badge">
        {current_unit}
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# 主題
# ==================================================

st.markdown(
    "### 選擇練習主題"
)


topic_names = list(
    TOPICS.keys()
)


selected_topic = st.selectbox(
    "練習主題",
    topic_names,
    index=topic_names.index(
        st.session_state.topic
    ),
    label_visibility="collapsed",
)


# ==================================================
# 切換主題
# ==================================================

if (
    selected_topic
    != st.session_state.topic
):

    st.session_state.topic = (
        selected_topic
    )

    st.session_state.question_index = 0
    st.session_state.question = None

    clear_answers()

    st.rerun()


topic_data = TOPICS[
    st.session_state.topic
]


st.markdown(
    f"#### {st.session_state.topic}"
)


# ==================================================
# 題型
# ==================================================

question_names = topic_data[
    "question_names"
]


selected_question = st.radio(
    "題型",
    range(
        len(question_names)
    ),
    format_func=lambda i: (
        question_names[i]
    ),
)


# ==================================================
# 切換題型
# ==================================================

if (
    selected_question
    != st.session_state.question_index
):

    st.session_state.question_index = (
        selected_question
    )

    clear_answers()

    new_question()


if st.session_state.question is None:

    new_question()


question = st.session_state.question


# ==================================================
# 題目卡
# ==================================================

st.markdown(
    """
    <div class="rm-question-card">
        <div class="rm-question-label">
            QUESTION
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    question["question"]
)


# ==================================================
# 作答
# ==================================================

answer_key = (
    f"answer_"
    f"{st.session_state.topic}_"
    f"{selected_question}"
)


question_type = question[
    "type"
]


student_answer = None


# ==================================================
# 四選一
# ==================================================

if question_type == "multiple_choice":

    choice_key = (
        f"choice_"
        f"{st.session_state.topic}_"
        f"{selected_question}"
    )

    st.markdown(
        "### 選擇答案"
    )

    student_answer = st.radio(
        "答案選項",
        question["options"],
        index=None,
        key=choice_key,
        format_func=lambda option: (
            f"${option}$"
        ),
        label_visibility="collapsed",
    )


# ==================================================
# 一般輸入
# ==================================================

else:

    if question_type == "expression":

        placeholder = (
            "例如：x^2 + 2xy + y^2"
        )

    elif question_type == "integer":

        placeholder = (
            "請輸入整數"
        )

    elif question_type == "last_digits":

        placeholder = (
            "請輸入末位數，例如：008"
        )

    elif question_type == "decimal_3":

        placeholder = (
            "例如：1.200"
        )

    elif question_type == "numeric_expression":

        placeholder = (
            "例如：2^8-1 或 255"
        )

    else:

        placeholder = (
            "請輸入答案"
        )

    st.markdown(
        "### 你的答案"
    )

    student_answer = st.text_input(
        "你的答案",
        placeholder=placeholder,
        key=answer_key,
        label_visibility="collapsed",
    )


# ==================================================
# 檢查答案
# ==================================================

if st.button(
    "檢查答案",
    type="primary",
    use_container_width=True,
):

    # ----------------------------------------------
    # 空白判定
    # ----------------------------------------------

    if (
        student_answer is None
        or str(student_answer).strip() == ""
    ):

        if question_type == "multiple_choice":

            st.warning(
                "請先選擇答案"
            )

        else:

            st.warning(
                "請先輸入答案"
            )

    else:

        # ------------------------------------------
        # 各答案類型
        # ------------------------------------------

        if question_type == "expression":

            correct, error = (
                check_expression(
                    student_answer,
                    question["answer"],
                )
            )

        elif question_type == "integer":

            correct, error = (
                check_integer(
                    student_answer,
                    question["answer"],
                )
            )

        elif question_type == "last_digits":

            correct, error = (
                check_last_digits(
                    student_answer,
                    question["answer"],
                )
            )

        elif question_type == "decimal_3":

            correct, error = (
                check_decimal_3(
                    student_answer,
                    question["answer"],
                )
            )

        elif question_type == "numeric_expression":

            correct, error = (
                check_numeric_expression(
                    student_answer,
                    question["answer"],
                )
            )

        elif question_type == "multiple_choice":

            correct = (
                student_answer
                == question["answer"]
            )

            error = None

        else:

            correct = False
            error = "未知的答案類型"


        # ==========================================
        # 結果
        # ==========================================

        if error:

            st.error(
                error
            )

        elif correct:

            st.success(
                "答對了！"
            )

        else:

            st.error(
                "答案不正確"
            )

            st.markdown(
                "**正確答案：**"
            )

            if (
                question_type
                == "multiple_choice"
            ):

                st.latex(
                    question["answer"]
                )

            elif (
                "answer_display"
                in question
            ):

                st.latex(
                    str(
                        question[
                            "answer_display"
                        ]
                    )
                )

            elif (
                question_type
                == "expression"
            ):

                st.latex(
                    sp.latex(
                        question["answer"]
                    )
                )

            else:

                st.latex(
                    str(
                        question["answer"]
                    )
                )


        # ==========================================
        # 解析
        # ==========================================

        if (
            not error
            and "solution" in question
        ):

            st.divider()

            st.markdown(
                question["solution"]
            )


# ==================================================
# 再來一題
# ==================================================

st.write("")


if st.button(
    "🔄 再來一題",
    use_container_width=True,
):

    clear_answers()

    new_question()

    st.rerun()