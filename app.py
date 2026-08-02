import streamlit as st
import sympy as sp
from decimal import Decimal, InvalidOperation

from modules.binomial_basic import (
    QUESTION_GENERATORS as BINOMIAL_BASIC_GENERATORS,
)

from modules.binomial_last_digits import (
    QUESTION_GENERATORS as BINOMIAL_LAST_DIGITS_GENERATORS,
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
)


# ==================================================
# 題庫設定
# ==================================================

TOPICS = {

    "二項式定理－基本練習": {
        "generators": BINOMIAL_BASIC_GENERATORS,
        "question_names": [
            "1｜二項式完整展開",
            "2｜含分式的二項式展開",
            "3｜求 xᵏyᵗ 的係數",
            "4｜求 xᵏ 的係數",
            "5｜含正負次方的係數",
        ],
    },

    "二項式定理－末位數練習": {
        "generators": BINOMIAL_LAST_DIGITS_GENERATORS,
        "question_names": [
            "1｜整數冪末位數",
            "2｜接近 1 的小數冪",
        ],
    },

}


# ==================================================
# Session State
# ==================================================

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
        if key.startswith("answer_")
    ]

    for key in keys_to_delete:
        del st.session_state[key]


def new_question():

    topic_data = TOPICS[
        st.session_state.topic
    ]

    generators = topic_data[
        "generators"
    ]

    generator = generators[
        st.session_state.question_index
    ]

    st.session_state.question = (
        generator()
    )


def check_last_digits(
    student_answer,
    correct_answer,
):
    """
    末位數答案判定。

    例如標準答案為 008：
    8、08、008 都接受。
    """

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

        student_value = int(text)

        return (
            student_value
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
    """
    小數點後第三位答案判定。

    使用 Decimal，
    避免 binary floating point 問題。
    """

    try:

        text = str(
            student_answer
        ).strip()

        if not text:
            return False, "請輸入答案"

        student_value = Decimal(text)

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


# ==================================================
# 標題
# ==================================================

st.title("Running Math")

st.caption("高中數學隨機練習")

st.divider()


# ==================================================
# 單元
# ==================================================

st.subheader("排列組合")


# ==================================================
# 主題
# ==================================================

topic_names = list(
    TOPICS.keys()
)


selected_topic = st.selectbox(
    "主題",
    topic_names,
    index=topic_names.index(
        st.session_state.topic
    ),
)


# ==================================================
# 切換主題
# ==================================================

if selected_topic != st.session_state.topic:

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


# ==================================================
# 題型
# ==================================================

question_names = topic_data[
    "question_names"
]


selected_question = st.radio(
    "選擇題型",
    range(len(question_names)),
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


st.divider()


# ==================================================
# 題目
# ==================================================

st.markdown("### 題目")

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


if question_type == "expression":

    placeholder = (
        "例如：x^2 + 2xy + y^2"
    )

elif question_type == "integer":

    placeholder = "請輸入整數"

elif question_type == "last_digits":

    placeholder = (
        "請輸入末位數，例如：008"
    )

elif question_type == "decimal_3":

    placeholder = (
        "例如：1.200"
    )

else:

    placeholder = "請輸入答案"


student_answer = st.text_input(
    "你的答案",
    placeholder=placeholder,
    key=answer_key,
)


# ==================================================
# 檢查答案
# ==================================================

if st.button(
    "檢查答案",
    type="primary",
    use_container_width=True,
):

    if not student_answer.strip():

        st.warning(
            "請先輸入答案"
        )

    else:

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

        else:

            correct = False
            error = "未知的答案類型"

        # ------------------------------------------
        # 顯示結果
        # ------------------------------------------

        if error:

            st.error(error)

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

            elif question_type == "expression":

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

        # ------------------------------------------
        # 有解析的題目才顯示解析
        # ------------------------------------------

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

if st.button(
    "🔄 再來一題",
    use_container_width=True,
):

    clear_answers()

    new_question()

    st.rerun()