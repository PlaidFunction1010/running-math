import sympy as sp

from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)


x, y = sp.symbols("x y")


TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor,
)


# ==================================================
# 代數式解析
# ==================================================

def parse_math_expression(text):
    """
    將學生輸入轉成 SymPy 代數式。

    支援例如：

    2x
    2*x
    x^2
    x**2
    x^-2
    1/x^2
    3xy
    3*x*y
    (x+1)^2
    """

    text = str(text).strip()

    if not text:
        raise ValueError("答案不能空白")

    return parse_expr(
        text,
        local_dict={
            "x": x,
            "y": y,
        },
        transformations=TRANSFORMATIONS,
        evaluate=True,
    )


# ==================================================
# 代數式等價判定
# ==================================================

def check_expression(
    student_answer,
    correct_answer,
):
    """
    判斷學生答案與標準答案是否數學等價。

    可處理：

    項次不同
    括號不同
    分數
    負次方
    省略乘號
    ^ 與 **
    等價代數表示
    """

    try:

        student_expr = parse_math_expression(
            student_answer
        )

        correct_expr = sp.sympify(
            correct_answer
        )

        difference = (
            student_expr
            - correct_expr
        )

        # cancel 對含負次方／分式特別有效
        difference = sp.cancel(
            difference
        )

        difference = sp.simplify(
            difference
        )

        return (
            difference == 0,
            None,
        )

    except Exception:

        return (
            False,
            "無法辨識你輸入的算式，請檢查括號、次方或運算符號。",
        )


# ==================================================
# 整數判定
# ==================================================

def check_integer(
    student_answer,
    correct_answer,
):
    """
    係數題整數答案判定。
    """

    try:

        text = str(
            student_answer
        ).strip()

        if not text:
            return (
                False,
                "請輸入整數",
            )

        # 使用 SymPy 解析，
        # 避免 int() 過度限制輸入格式
        value = sp.sympify(text)

        if value.is_integer is not True:
            return (
                False,
                "請輸入整數",
            )

        return (
            value == sp.Integer(
                correct_answer
            ),
            None,
        )

    except Exception:

        return (
            False,
            "請輸入整數",
        )