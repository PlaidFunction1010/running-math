import random
from decimal import Decimal, ROUND_HALF_UP
from math import comb


# ==================================================
# 共用工具
# ==================================================

def signed_integer(value):
    """
    將整數轉成自然的 +k / -k 顯示。
    """
    if value > 0:
        return f"+{value}"
    return str(value)


def signed_decimal(value):
    """
    Decimal 轉成自然的 +0.02 / -0.02 顯示。
    """
    if value > 0:
        return f"+{value}"
    return str(value)


def latex_integer_sum(terms):
    """
    將整數項組合成自然的 LaTeX 加減式，
    避免 +- 或 --。
    """
    result = ""

    for term in terms:

        if term == 0:
            continue

        if not result:
            result = str(term)
        elif term > 0:
            result += f"+{term}"
        else:
            result += str(term)

    return result or "0"


# ==================================================
# 子題 1
# 整數冪末位數
# ==================================================

def generate_question_1():

    # ----------------------------------------------
    # 隨機決定基準類型
    # ----------------------------------------------

    base_type = random.choice([
        "tens",
        "hundreds",
        "thousands",
    ])

    if base_type == "tens":

        A = random.choice([
            10, 20, 30, 40, 50,
            60, 70, 80, 90,
        ])

        m = 2
        type_name = "整十數"

    elif base_type == "hundreds":

        A = random.choice([
            100, 200, 300, 400, 500,
            600, 700, 800, 900,
        ])

        m = 3
        type_name = "整百數"

    else:

        A = 1000
        m = 4
        type_name = "整千數"

    k = random.choice([
        -2, -1, 1, 2,
    ])

    n = random.choice([
        3, 4, 5, 6,
    ])

    N = A + k

    modulus = 10 ** m

    # ----------------------------------------------
    # 正確答案
    # ----------------------------------------------

    answer_number = pow(
        N,
        n,
        modulus,
    )

    answer_display = str(
        answer_number
    ).zfill(m)

    # ----------------------------------------------
    # 二項式各項
    # ----------------------------------------------

    terms = []

    for r in range(n + 1):

        value = (
            comb(n, r)
            * (A ** (n - r))
            * (k ** r)
        )

        terms.append(value)

    # ----------------------------------------------
    # 找出模 10^m 下真正有影響的項
    # ----------------------------------------------

    relevant_terms = []
    irrelevant_terms = []

    for r, value in enumerate(terms):

        if value % modulus == 0:
            irrelevant_terms.append((r, value))
        else:
            relevant_terms.append((r, value))

    relevant_values = [
        value
        for _, value in relevant_terms
    ]

    relevant_sum = sum(
        relevant_values
    )

    # ----------------------------------------------
    # LaTeX
    # ----------------------------------------------

    k_latex = signed_integer(k)

    rewritten = (
        f"({A}{k_latex})^{{{n}}}"
    )

    expansion_terms = []

    for r in range(n + 1):

        coefficient = comb(n, r)

        a_power = n - r
        k_power = r

        parts = []

        if coefficient != 1:
            parts.append(str(coefficient))

        if a_power > 0:

            if a_power == 1:
                parts.append(str(A))
            else:
                parts.append(
                    f"{A}^{{{a_power}}}"
                )

        if k_power > 0:

            if k < 0:
                k_part = f"({k})"
            else:
                k_part = str(k)

            if k_power == 1:
                parts.append(k_part)
            else:
                parts.append(
                    f"{k_part}^{{{k_power}}}"
                )

        if not parts:
            parts.append("1")

        expansion_terms.append(
            r"\cdot ".join(parts)
        )

    expansion_latex = (
        " + ".join(expansion_terms)
    )

    # 修正 + 負數的視覺問題
    expansion_latex = expansion_latex.replace(
        "+ -",
        "- ",
    )

    relevant_latex = latex_integer_sum(
        relevant_values
    )

    # ----------------------------------------------
    # 不影響末位數說明
    # ----------------------------------------------

    if irrelevant_terms:

        ignored_r = [
            str(r)
            for r, _ in irrelevant_terms
        ]

        ignored_text = (
            "其中 "
            + "、".join(
                f"$r={r}$"
                for r in ignored_r
            )
            + f" 的項都是 ${modulus}$ 的倍數，"
              f"因此不影響末 {m} 位數。"
        )

    else:

        ignored_text = (
            f"本題各項在模 ${modulus}$ 下皆需保留。"
        )

    # ----------------------------------------------
    # 解析
    # ----------------------------------------------

    solution = f"""
### 解析

因為 ${N}$ 接近{type_name} ${A}$，所以先改寫：

$$
{N}={A}{k_latex}
$$

因此

$$
{N}^{{{n}}}
=
{rewritten}
$$

利用二項式定理：

$$
(A+k)^n
=
\\sum_{{r=0}}^n
\\binom{{n}}{{r}}
A^{{n-r}}k^r
$$

代入本題：

$$
{rewritten}
=
{expansion_latex}
$$

我們只要求末 **{m} 位數**，因此只需要考慮除以

$$
10^{m}={modulus}
$$

後的餘數。

{ignored_text}

所以只需計算會影響末 {m} 位數的部分：

$$
{relevant_latex}
$$

在模 ${modulus}$ 下，

$$
{N}^{{{n}}}
\\equiv
{answer_number}
\\pmod{{{modulus}}}
$$

因此末 {m} 位數為

$$
\\boxed{{\\text{{{answer_display}}}}}
$$
"""

    # ----------------------------------------------
    # 題目
    # ----------------------------------------------

    question = f"""
試利用二項式定理，求

$$
{N}^{{{n}}}
$$

的末 **{m} 位數**。
"""

    return {
        "type": "last_digits",
        "question": question,
        "answer": answer_number,
        "answer_display": answer_display,
        "solution": solution,
    }


# ==================================================
# 子題 2
# 接近 1 的小數冪
# ==================================================

def generate_question_2():

    k = random.choice([
        Decimal("-0.02"),
        Decimal("-0.01"),
        Decimal("0.01"),
        Decimal("0.02"),
    ])

    n = random.choice([
        5, 6, 8, 10,
    ])

    one = Decimal("1")

    base = one + k

    # ----------------------------------------------
    # 使用 Decimal 精確計算
    # ----------------------------------------------

    exact_value = base ** n

    rounded_value = exact_value.quantize(
        Decimal("0.001"),
        rounding=ROUND_HALF_UP,
    )

    answer_display = format(
        rounded_value,
        ".3f",
    )

    # ----------------------------------------------
    # 建立二項式展開
    # ----------------------------------------------

    expansion_parts = []

    decimal_terms = []

    for r in range(n + 1):

        coefficient = comb(n, r)

        term = (
            Decimal(coefficient)
            * (k ** r)
        )

        decimal_terms.append(term)

        if r == 0:

            part = "1"

        elif r == 1:

            if coefficient == 1:
                part = f"({k})"
            else:
                part = (
                    f"{coefficient}"
                    f"({k})"
                )

        else:

            if coefficient == 1:
                part = (
                    f"({k})^{{{r}}}"
                )
            else:
                part = (
                    f"{coefficient}"
                    f"({k})^{{{r}}}"
                )

        expansion_parts.append(part)

    expansion_latex = (
        " + ".join(expansion_parts)
    )

    expansion_latex = expansion_latex.replace(
        "+ -",
        "- ",
    )

    # ----------------------------------------------
    # 實際精確值顯示
    # ----------------------------------------------

    exact_text = format(
        exact_value,
        "f",
    )

    # 避免顯示過長且無教學意義
    if len(exact_text) > 18:
        exact_text = exact_text[:18]

    # ----------------------------------------------
    # 正負號顯示
    # ----------------------------------------------

    k_display = str(abs(k))

    if k > 0:

        rewritten_base = (
            f"1+{k_display}"
        )

    else:

        rewritten_base = (
            f"1-{k_display}"
        )

    # ----------------------------------------------
    # 題目
    # ----------------------------------------------

    base_display = format(
        base,
        ".2f",
    )

    question = f"""
試利用二項式定理求

$$
\\left({base_display}\\right)^{{{n}}}
$$

之值，並**四捨五入至小數點後第三位**。
"""

    # ----------------------------------------------
    # 解析
    # ----------------------------------------------

    solution = f"""
### 解析

將底數改寫成接近 $1$ 的形式：

$$
{base_display}
=
{rewritten_base}
$$

所以

$$
\\left({base_display}\\right)^{{{n}}}
=
\\left({rewritten_base}\\right)^{{{n}}}
$$

利用二項式定理：

$$
(1+k)^n
=
\\sum_{{r=0}}^n
\\binom{{n}}{{r}}k^r
$$

代入本題：

$$
\\left({rewritten_base}\\right)^{{{n}}}
=
{expansion_latex}
$$

計算得

$$
\\left({base_display}\\right)^{{{n}}}
=
{exact_value}
$$

四捨五入至小數點後第三位：

$$
\\boxed{{{answer_display}}}
$$
"""

    return {
        "type": "decimal_3",
        "question": question,
        "answer": rounded_value,
        "answer_display": answer_display,
        "solution": solution,
    }


# ==================================================
# 題目生成器
# ==================================================

QUESTION_GENERATORS = [
    generate_question_1,
    generate_question_2,
]