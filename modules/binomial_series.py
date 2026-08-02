import random
import math


# ==================================================
# 共用工具
# ==================================================

def binom(n, k):
    return rf"\binom{{{n}}}{{{k}}}"


def power_latex(base, exponent):
    """
    次方 LaTeX。
    負底數強制保留括號。
    """

    if base < 0:
        return rf"({base})^{{{exponent}}}"

    return rf"{base}^{{{exponent}}}"


def verify_sum(n, indices, signs=None):
    """
    實際利用 math.comb 驗證組合級數。
    """

    if signs is None:
        signs = [1] * len(indices)

    return sum(
        sign * math.comb(n, k)
        for k, sign in zip(indices, signs)
    )


# ==================================================
# 子題 1
# 基本組合級數求和
# ==================================================

def generate_question_1():

    n = random.choice([
        5, 6, 7, 8, 9, 10
    ])

    series_type = random.randint(1, 4)

    # ----------------------------------------------
    # 類型 1
    # C(n,0)+...+C(n,n)
    # ----------------------------------------------

    if series_type == 1:

        indices = list(range(n + 1))

        actual_answer = verify_sum(
            n,
            indices,
        )

        expected_answer = 2 ** n

        assert actual_answer == expected_answer

        series = (
            rf"{binom(n, 0)}"
            rf"+{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"+\cdots"
            rf"+{binom(n, n)}"
        )

        solution = rf"""
### 解析

由二項式定理：

$$
(1+x)^{{{n}}}
=
\sum_{{k=0}}^{{{n}}}
\binom{{{n}}}{{k}}x^k
$$

令 $x=1$：

$$
{binom(n, 0)}
+{binom(n, 1)}
+\cdots
+{binom(n, n)}
=
(1+1)^{{{n}}}
$$

所以

$$
\boxed{{2^{{{n}}}}}
$$

其值為

$$
\boxed{{{expected_answer}}}
$$
"""

    # ----------------------------------------------
    # 類型 2
    # 從下標 1 開始
    # ----------------------------------------------

    elif series_type == 2:

        indices = list(range(1, n + 1))

        actual_answer = verify_sum(
            n,
            indices,
        )

        expected_answer = (
            2 ** n - 1
        )

        assert actual_answer == expected_answer

        series = (
            rf"{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"+{binom(n, 3)}"
            rf"+\cdots"
            rf"+{binom(n, n)}"
        )

        solution = rf"""
### 解析

完整的組合數級數為：

$$
{binom(n, 0)}
+{binom(n, 1)}
+\cdots
+{binom(n, n)}
=
(1+1)^{{{n}}}
=
2^{{{n}}}
$$

但本題少了

$$
{binom(n, 0)}=1
$$

因此原式為

$$
2^{{{n}}}-1
$$

所以答案：

$$
\boxed{{2^{{{n}}}-1}}
=
\boxed{{{expected_answer}}}
$$
"""

    # ----------------------------------------------
    # 類型 3
    # 完整正負相間
    # ----------------------------------------------

    elif series_type == 3:

        indices = list(range(n + 1))

        signs = [
            (-1) ** k
            for k in indices
        ]

        actual_answer = verify_sum(
            n,
            indices,
            signs,
        )

        expected_answer = 0

        assert actual_answer == expected_answer

        series = (
            rf"{binom(n, 0)}"
            rf"-{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"-{binom(n, 3)}"
            rf"+\cdots"
            rf"+(-1)^{{{n}}}{binom(n, n)}"
        )

        solution = rf"""
### 解析

由二項式定理：

$$
(1+x)^{{{n}}}
=
\sum_{{k=0}}^{{{n}}}
\binom{{{n}}}{{k}}x^k
$$

令 $x=-1$：

$$
{binom(n, 0)}
-{binom(n, 1)}
+{binom(n, 2)}
-\cdots
+(-1)^{{{n}}}{binom(n, n)}
=
(1-1)^{{{n}}}
$$

因此

$$
\boxed{{0}}
$$
"""

    # ----------------------------------------------
    # 類型 4
    # 正負相間且從 1 開始
    # ----------------------------------------------

    else:

        indices = list(
            range(1, n + 1)
        )

        signs = [
            (-1) ** k
            for k in indices
        ]

        actual_answer = verify_sum(
            n,
            indices,
            signs,
        )

        expected_answer = -1

        assert actual_answer == expected_answer

        series = (
            rf"-{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"-{binom(n, 3)}"
            rf"+\cdots"
            rf"+(-1)^{{{n}}}{binom(n, n)}"
        )

        solution = rf"""
### 解析

完整的正負相間級數為：

$$
{binom(n, 0)}
-{binom(n, 1)}
+{binom(n, 2)}
-\cdots
+(-1)^{{{n}}}{binom(n, n)}
=
(1-1)^{{{n}}}
=
0
$$

而

$$
{binom(n, 0)}=1
$$

本題少了這一項，因此

$$
-\binom{{{n}}}{{1}}
+\binom{{{n}}}{{2}}
-\cdots
+(-1)^{{{n}}}\binom{{{n}}}{{{n}}}
=
-1
$$

所以

$$
\boxed{{-1}}
$$
"""

    question = rf"""
求下列式子之值：

$$
{series}
$$
"""

    return {
        "type": "numeric_expression",
        "question": question,
        "answer": expected_answer,
        "solution": solution,
    }


# ==================================================
# 子題 2
# 對稱性求部分偶數項和
# ==================================================

def generate_question_2():

    # n ≡ 2 (mod 4)
    # 中央下標為奇數，不會落入偶數項集合
    n = random.choice([
        6, 10, 14, 18
    ])

    half_limit = n // 2

    indices = list(
        range(
            0,
            half_limit,
            2,
        )
    )

    # ----------------------------------------------
    # 防呆驗證
    # ----------------------------------------------

    assert n % 4 == 2

    assert all(
        k % 2 == 0
        for k in indices
    )

    assert n // 2 not in indices

    symmetric_indices = [
        n - k
        for k in indices
    ]

    assert len(
        set(symmetric_indices)
    ) == len(indices)

    assert not (
        set(indices)
        & set(symmetric_indices)
    )

    complete_even_indices = set(
        range(0, n + 1, 2)
    )

    assert (
        set(indices)
        | set(symmetric_indices)
    ) == complete_even_indices

    # ----------------------------------------------
    # 實際計算驗證
    # ----------------------------------------------

    actual_answer = verify_sum(
        n,
        indices,
    )

    expected_answer = (
        2 ** (n - 2)
    )

    assert actual_answer == expected_answer

    # ----------------------------------------------
    # 題目顯示
    # ----------------------------------------------

    series = "+".join(
        binom(n, k)
        for k in indices
    )

    # ----------------------------------------------
    # 對稱配對文字
    # ----------------------------------------------

    pair_lines = []

    for k in indices:

        pair_lines.append(
            rf"{binom(n, k)}"
            rf"="
            rf"{binom(n, n-k)}"
        )

    pairs_latex = r"\qquad ".join(
        pair_lines
    )

    complete_even_series = (
        rf"{binom(n, 0)}"
        rf"+{binom(n, 2)}"
        rf"+\cdots"
        rf"+{binom(n, n)}"
    )

    question = rf"""
求下列式子之值：

$$
{series}
$$
"""

    solution = rf"""
### 解析

利用組合數的對稱性：

$$
\binom{{n}}{{k}}
=
\binom{{n}}{{n-k}}
$$

本題可配對為：

$$
{pairs_latex}
$$

因此題目中的每一項，都能和另一半的偶數下標項完全配對。

設原式為 $S$，則

$$
2S
=
{complete_even_series}
$$

完整的偶數下標係數和為

$$
2^{{{n}-1}}
$$

所以

$$
2S=2^{{{n}-1}}
$$

因此

$$
S=2^{{{n}-2}}
$$

所以答案為

$$
\boxed{{2^{{{n-2}}}}}
=
\boxed{{{expected_answer}}}
$$
"""

    return {
        "type": "numeric_expression",
        "question": question,
        "answer": expected_answer,
        "solution": solution,
    }


# ==================================================
# 子題 3
# 完整奇數／偶數下標係數和
# ==================================================

def generate_question_3():

    n = random.choice([
        5, 6, 7, 8,
        9, 10, 11, 12,
    ])

    parity = random.choice([
        "even",
        "odd",
    ])

    if parity == "even":

        indices = list(
            range(0, n + 1, 2)
        )

        label = "偶數"

    else:

        indices = list(
            range(1, n + 1, 2)
        )

        label = "奇數"

    actual_answer = verify_sum(
        n,
        indices,
    )

    expected_answer = (
        2 ** (n - 1)
    )

    assert actual_answer == expected_answer

    # 顯示完整級數。
    # 項數不多，直接完整顯示可避免省略號歧義。
    series = "+".join(
        binom(n, k)
        for k in indices
    )

    question = rf"""
求下列式子之值：

$$
{series}
$$
"""

    solution = rf"""
### 解析

設偶數下標係數和為 $E$，奇數下標係數和為 $O$。

由

$$
(1+1)^{{{n}}}=2^{{{n}}}
$$

可得

$$
E+O=2^{{{n}}}
$$

再由

$$
(1-1)^{{{n}}}=0
$$

可得

$$
E-O=0
$$

因此

$$
E=O
$$

所以

$$
E=O=2^{{{n}-1}}
$$

本題要求的是完整的{label}下標係數和，因此答案為

$$
\boxed{{2^{{{n-1}}}}}
=
\boxed{{{expected_answer}}}
$$
"""

    return {
        "type": "numeric_expression",
        "question": question,
        "answer": expected_answer,
        "solution": solution,
    }


# ==================================================
# 子題 4
# 帶等比權重的二項式級數
# 四選一
# ==================================================

def weighted_term_latex(n, a, k):
    """
    產生第 k 項的 LaTeX。
    這裡專門處理負 a 的符號，
    避免出現 +- 等不自然排版。
    """

    combination = binom(n, k)

    if k == 0:
        return combination

    # a > 0
    if a > 0:

        if k == 1:

            if a == 1:
                factor = ""
            else:
                factor = str(a)

        else:

            if a == 1:
                factor = ""
            else:
                factor = rf"{a}^{{{k}}}"

        return factor + combination

    # a < 0
    abs_a = abs(a)

    sign = -1 if k % 2 == 1 else 1

    if k == 1:
        magnitude = str(abs_a)

    else:
        magnitude = rf"{abs_a}^{{{k}}}"

    term = magnitude + combination

    if sign < 0:
        return "-" + term

    return "+" + term


def make_weighted_series(n, a):

    # 顯示前四項 + ... + 最後一項
    # n 最小為 4，因此合法。

    first = binom(n, 0)

    pieces = [first]

    for k in range(1, 4):

        term = weighted_term_latex(
            n,
            a,
            k,
        )

        if a > 0:
            pieces.append(
                "+" + term
            )
        else:
            pieces.append(term)

    pieces.append(r"+\cdots")

    # 最後一項另外處理
    if a > 0:

        last_factor = (
            ""
            if a == 1
            else rf"{a}^{{{n}}}"
        )

        last = (
            "+"
            + last_factor
            + binom(n, n)
        )

    else:

        abs_a = abs(a)

        last_factor = (
            rf"{abs_a}^{{{n}}}"
        )

        if n % 2 == 0:
            last_sign = "+"
        else:
            last_sign = "-"

        last = (
            last_sign
            + last_factor
            + binom(n, n)
        )

    pieces.append(last)

    return "".join(pieces)


def generate_distractor_bases(a):
    """
    根據常見錯誤建立候選底數。

    正解底數 = 1+a
    """

    correct_base = 1 + a

    candidates = [
        a,              # 忘記 1
        1 - a,          # 加減號判斷錯誤
        abs(correct_base),  # 負底數誤變正
        -correct_base,      # 正負號反轉
        a - 1,
        abs(a),
        -abs(a),
        1 + abs(a),
        1 - abs(a),
        correct_base + 1,
        correct_base - 1,
    ]

    # 去除正解與重複
    result = []

    for value in candidates:

        if value == correct_base:
            continue

        if value in result:
            continue

        result.append(value)

    return result


def generate_question_4():

    while True:

        a = random.choice([
            -4, -3, -2,
            1, 2, 3, 4,
        ])

        n = random.choice([
            4, 5, 6, 7,
            8, 9, 10,
        ])

        correct_base = 1 + a

        # a != -1 已由候選值保證
        assert correct_base != 0

        distractor_bases = (
            generate_distractor_bases(a)
        )

        # 數學上 m^n 可能因偶次方造成
        # b^n 與 (-b)^n 相同。
        # 因此不能只檢查字串不同，
        # 要檢查實際數學值不同。

        correct_value = (
            correct_base ** n
        )

        valid_distractors = []

        used_values = {
            correct_value
        }

        for base in distractor_bases:

            value = base ** n

            if value in used_values:
                continue

            used_values.add(value)

            valid_distractors.append(
                base
            )

            if len(valid_distractors) == 3:
                break

        if len(valid_distractors) == 3:
            break

    # ----------------------------------------------
    # 選項
    # ----------------------------------------------

    option_bases = [
        correct_base,
        *valid_distractors,
    ]

    random.shuffle(
        option_bases
    )

    options = []

    correct_option = None

    for base in option_bases:

        label = power_latex(
            base,
            n,
        )

        option = {
            "label": label,
            "base": base,
            "value": base ** n,
        }

        options.append(option)

        if base == correct_base:
            correct_option = label

    assert len(options) == 4

    assert len({
        option["value"]
        for option in options
    }) == 4

    assert sum(
        option["value"]
        == correct_value
        for option in options
    ) == 1

    # ----------------------------------------------
    # 級數
    # ----------------------------------------------

    series = make_weighted_series(
        n,
        a,
    )

    # ----------------------------------------------
    # 解析用 a
    # ----------------------------------------------

    if a > 0:
        binomial = rf"(1+{a})^{{{n}}}"
    else:
        binomial = rf"(1-{abs(a)})^{{{n}}}"

    correct_latex = power_latex(
        correct_base,
        n,
    )

    question = rf"""
下列級數的值可表示成哪一個選項？

$$
{series}
$$
"""

    solution = rf"""
### 解析

二項式定理：

$$
(1+a)^n
=
\binom{{n}}{{0}}
+a\binom{{n}}{{1}}
+a^2\binom{{n}}{{2}}
+\cdots
+a^n\binom{{n}}{{n}}
$$

本題的等比權重為

$$
a={a}
$$

因此原式就是

$$
{binomial}
$$

計算 $1+a$：

$$
1+({a})={correct_base}
$$

所以原式為

$$
\boxed{{{correct_latex}}}
$$
"""

    return {
        "type": "multiple_choice",
        "question": question,
        "answer": correct_option,
        "options": [
            option["label"]
            for option in options
        ],
        "solution": solution,
    }


# ==================================================
# 題目生成器
# ==================================================

QUESTION_GENERATORS = [
    generate_question_1,
    generate_question_2,
    generate_question_3,
    generate_question_4,
]