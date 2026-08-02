import streamlit as st
import sympy as sp

from modules.binomial_basic import (
    QUESTION_GENERATORS,
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
# Session State
# ==================================================

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "question" not in st.session_state:
    st.session_state.question = None


def clear_answers():
    """
    清除各題型輸入框中的舊答案。
    """

    for i in range(5):

        key = f"answer_{i}"

        if key in st.session_state:
            del st.session_state[key]


def new_question():
    """
    依目前題型產生新題目。
    """

    generator = QUESTION_GENERATORS[
        st.session_state.question_index
    ]

    st.session_state.question = generator()


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

st.selectbox(
    "主題",
    [
        "二項式定理－基本練習",
    ],
)


# ==================================================
# 題型
# ==================================================

question_names = [
    "1｜二項式完整展開",
    "2｜含分式的二項式展開",
    "3｜求 xᵏyᵗ 的係數",
    "4｜求 xᵏ 的係數",
    "5｜含正負次方的係數",
]


selected_question = st.radio(
    "選擇題型",
    range(5),
    format_func=lambda i: question_names[i],
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
    f"answer_{selected_question}"
)


if question["type"] == "expression":

    student_answer = st.text_input(
        "你的答案",
        placeholder=(
            "例如：x^2 + 2xy + y^2"
        ),
        key=answer_key,
    )

else:

    student_answer = st.text_input(
        "你的答案",
        placeholder="請輸入整數",
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

        if (
            question["type"]
            == "expression"
        ):

            correct, error = (
                check_expression(
                    student_answer,
                    question["answer"],
                )
            )

        else:

            correct, error = (
                check_integer(
                    student_answer,
                    question["answer"],
                )
            )

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
                question["type"]
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