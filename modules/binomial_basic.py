import random
import math
import sympy as sp


x, y = sp.symbols("x y")


# ==================================================
# 共用亂數
# ==================================================

def random_nonzero_integer():
    """
    使用小整數，避免展開後係數過大，
    適合高中生手算。
    """
    return random.choice([
        -3, -2, -1,
        1, 2, 3,
    ])


def generate_ab():
    return (
        random_nonzero_integer(),
        random_nonzero_integer(),
    )


# ==================================================
# LaTeX 顯示工具
# ==================================================

def latex_linear_two_terms(a, first_term, b, second_term=""):
    """
    建立自然的二項式 LaTeX。

    避免：
    3x+-2y
    3x--2y

    產生：
    3x-2y
    """

    first = sp.latex(a * first_term)

    if second_term == "":
        second_expr = sp.Integer(b)
    else:
        second_expr = b * second_term

    second_abs = sp.latex(abs(b) * (
        sp.Integer(1)
        if second_term == ""
        else second_term
    ))

    if b > 0:
        return f"{first}+{second_abs}"

    return f"{first}-{second_abs}"


def latex_ax_by(a, b):
    """ax + by"""
    return latex_linear_two_terms(
        a,
        x,
        b,
        y,
    )


def latex_ax_b(a, b):
    """ax + b"""
    return latex_linear_two_terms(
        a,
        x,
        b,
    )


def latex_ax_b_over_x(a, b):
    """
    ax + b/x
    """

    first = sp.latex(a * x)
    fraction = (
        f"\\frac{{{abs(b)}}}{{x}}"
    )

    if b > 0:
        return f"{first}+{fraction}"

    return f"{first}-{fraction}"


# ==================================================
# 子題 1
# 二項式完整展開
# ==================================================

def generate_question_1():

    a, b = generate_ab()
    n = random.randint(2, 5)

    base = a * x + b * y
    answer = sp.expand(base ** n)

    base_latex = latex_ax_by(a, b)

    question = (
        "請展開下列式子："
        f"$$\\left({base_latex}\\right)^{{{n}}}$$"
    )

    return {
        "type": "expression",
        "question": question,
        "answer": answer,
    }


# ==================================================
# 子題 2
# 含分式的二項式完整展開
# ==================================================

def generate_question_2():

    a, b = generate_ab()
    n = random.randint(2, 5)

    base = a * x + sp.Rational(b, 1) / x
    answer = sp.expand(base ** n)

    base_latex = latex_ax_b_over_x(a, b)

    question = (
        "請展開下列式子："
        f"$$\\left({base_latex}\\right)^{{{n}}}$$"
    )

    return {
        "type": "expression",
        "question": question,
        "answer": answer,
    }


# ==================================================
# 子題 3
# 求指定項 x^k y^t 的係數
# ==================================================

def generate_question_3():

    a, b = generate_ab()
    n = random.randint(2, 5)

    # 約 50% 存在
    # 約 50% 不存在
    exists = random.choice([
        True,
        False,
    ])

    if exists:

        k = random.randint(0, n)
        t = n - k

        answer = (
            math.comb(n, k)
            * (a ** k)
            * (b ** t)
        )

    else:

        while True:

            k = random.randint(0, n + 2)
            t = random.randint(0, n + 2)

            if k + t != n:
                break

        answer = 0

    base_latex = latex_ax_by(a, b)

    question = (
        "求展開式"
        f"$$\\left({base_latex}\\right)^{{{n}}}$$"
        "中，"
        f"$$x^{{{k}}}y^{{{t}}}$$"
        "的係數。"
    )

    return {
        "type": "integer",
        "question": question,
        "answer": answer,
    }


# ==================================================
# 子題 4
# 求 x^k 的係數
# ==================================================

def generate_question_4():

    a, b = generate_ab()
    n = random.randint(2, 5)

    # 題目規定 0 <= k < n
    k = random.randint(0, n - 1)

    answer = (
        math.comb(n, k)
        * (a ** k)
        * (b ** (n - k))
    )

    base_latex = latex_ax_b(a, b)

    question = (
        "求展開式"
        f"$$\\left({base_latex}\\right)^{{{n}}}$$"
        "中，"
        f"$$x^{{{k}}}$$"
        "的係數。"
    )

    return {
        "type": "integer",
        "question": question,
        "answer": answer,
    }


# ==================================================
# 子題 5
# 含正負次方的係數問題
# ==================================================

def generate_question_5():

    a, b = generate_ab()
    n = random.randint(2, 5)

    # 約 50% 指定項存在
    # 約 50% 指定項不存在
    exists = random.choice([
        True,
        False,
    ])

    if exists:

        r = random.randint(0, n)

        k = n - 2 * r

        answer = (
            math.comb(n, r)
            * (a ** (n - r))
            * (b ** r)
        )

    else:

        possible_k = {
            n - 2 * r
            for r in range(n + 1)
        }

        # 同時涵蓋正、0、負整數
        candidates = [
            value
            for value in range(
                -n - 2,
                n + 3,
            )
            if value not in possible_k
        ]

        k = random.choice(candidates)
        answer = 0

    base_latex = latex_ax_b_over_x(a, b)

    question = (
        "求展開式"
        f"$$\\left({base_latex}\\right)^{{{n}}}$$"
        "中，"
        f"$$x^{{{k}}}$$"
        "的係數。"
    )

    return {
        "type": "integer",
        "question": question,
        "answer": answer,
    }


# ==================================================
# 題目生成器
# ==================================================

QUESTION_GENERATORS = [
    generate_question_1,
    generate_question_2,
    generate_question_3,
    generate_question_4,
    generate_question_5,
]