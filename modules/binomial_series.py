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
    負底數一定保留括號。
    """

    if base < 0:
        return rf"({base})^{{{exponent}}}"

    return rf"{base}^{{{exponent}}}"


def verify_sum(n, indices, signs=None):
    """
    使用實際組合數驗證級數答案。
    """

    if signs is None:
        signs = [1] * len(indices)

    return sum(
        sign * math.comb(n, k)
        for k, sign in zip(indices, signs)
    )


def make_multiple_choice(correct_label, distractor_labels):
    """
    建立四選一。

    防呆：
    1. 正解一定存在
    2. 固定四個選項
    3. 不重複
    4. 正解位置隨機
    """

    unique_distractors = []

    for label in distractor_labels:

        if label == correct_label:
            continue

        if label in unique_distractors:
            continue

        unique_distractors.append(label)

    if len(unique_distractors) < 3:
        raise ValueError("干擾選項不足")

    selected_distractors = unique_distractors[:3]

    options = [
        correct_label,
        *selected_distractors,
    ]

    assert len(options) == 4
    assert len(set(options)) == 4
    assert options.count(correct_label) == 1

    random.shuffle(options)

    assert correct_label in options

    return options


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
    # 完整相加
    # ----------------------------------------------

    if series_type == 1:

        indices = list(range(n + 1))

        actual_answer = verify_sum(
            n,
            indices,
        )

        expected_value = 2 ** n

        assert actual_answer == expected_value

        series = (
            rf"{binom(n, 0)}"
            rf"+{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"+\cdots"
            rf"+{binom(n, n)}"
        )

        correct_label = (
            rf"2^{{{n}}}"
        )

        distractors = [
            rf"2^{{{n}}}-1",
            rf"2^{{{n-1}}}",
            "0",
            rf"2^{{{n}}}+1",
            "1",
            "-1",
        ]

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

因此

$$
\boxed{{2^{{{n}}}}}
$$
"""

    # ----------------------------------------------
    # 類型 2
    # 從下標 1 開始
    # ----------------------------------------------

    elif series_type == 2:

        indices = list(
            range(1, n + 1)
        )

        actual_answer = verify_sum(
            n,
            indices,
        )

        expected_value = (
            2 ** n - 1
        )

        assert actual_answer == expected_value

        series = (
            rf"{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"+{binom(n, 3)}"
            rf"+\cdots"
            rf"+{binom(n, n)}"
        )

        correct_label = (
            rf"2^{{{n}}}-1"
        )

        distractors = [
            rf"2^{{{n}}}",
            rf"2^{{{n-1}}}",
            rf"2^{{{n}}}+1",
            "0",
            "1",
            "-1",
        ]

        solution = rf"""
### 解析

完整的組合數級數：

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

但本題從下標 $1$ 開始，少了

$$
{binom(n, 0)}=1
$$

因此原式為

$$
\boxed{{2^{{{n}}}-1}}
$$
"""

    # ----------------------------------------------
    # 類型 3
    # 完整正負相間
    # ----------------------------------------------

    elif series_type == 3:

        indices = list(
            range(n + 1)
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

        expected_value = 0

        assert actual_answer == expected_value

        series = (
            rf"{binom(n, 0)}"
            rf"-{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"-{binom(n, 3)}"
            rf"+\cdots"
            rf"+(-1)^{{{n}}}{binom(n, n)}"
        )

        correct_label = "0"

        distractors = [
            "-1",
            "1",
            rf"2^{{{n}}}",
            rf"2^{{{n}}}-1",
            rf"2^{{{n-1}}}",
        ]

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

所以

$$
\boxed{{0}}
$$
"""

    # ----------------------------------------------
    # 類型 4
    # 正負相間，從下標 1 開始
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

        expected_value = -1

        assert actual_answer == expected_value

        series = (
            rf"-{binom(n, 1)}"
            rf"+{binom(n, 2)}"
            rf"-{binom(n, 3)}"
            rf"+\cdots"
            rf"+(-1)^{{{n}}}{binom(n, n)}"
        )

        correct_label = "-1"

        distractors = [
            "0",
            "1",
            rf"2^{{{n}}}",
            rf"2^{{{n}}}-1",
            rf"-2^{{{n}}}",
        ]

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

本題少了這個 $1$，因此

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

    options = make_multiple_choice(
        correct_label,
        distractors,
    )

    question = rf"""
求下列式子之值，請選出正確答案：

$$
{series}
$$
"""

    return {
        "type": "multiple_choice",
        "question": question,
        "answer": correct_label,
        "options": options,
        "solution": solution,
    }


# ==================================================
# 子題 2
# 利用對稱性求部分偶數項和
# ==================================================

def generate_question_2():

    # n ≡ 2 (mod 4)
    # 保證中央下標 n/2 為奇數
    n = random.choice([
        6, 10, 14, 18
    ])

    assert n % 4 == 2

    half_limit = n // 2

    indices = list(
        range(
            0,
            half_limit,
            2,
        )
    )

    # ----------------------------------------------
    # 數學合法性驗證
    # ----------------------------------------------

    assert all(
        k % 2 == 0
        for k in indices
    )

    assert (
        n // 2
        not in indices
    )

    symmetric_indices = [
        n - k
        for k in indices
    ]

    # 每一項的對稱項唯一
    assert (
        len(set(symmetric_indices))
        == len(indices)
    )

    # 題目這一半與另一半不可重疊
    assert not (
        set(indices)
        & set(symmetric_indices)
    )

    complete_even_indices = set(
        range(0, n + 1, 2)
    )

    # 合併後必須剛好是完整偶數下標集合
    assert (
        set(indices)
        | set(symmetric_indices)
    ) == complete_even_indices

    # ----------------------------------------------
    # 實際答案驗證
    # ----------------------------------------------

    actual_answer = verify_sum(
        n,
        indices,
    )

    expected_value = (
        2 ** (n - 2)
    )

    assert (
        actual_answer
        == expected_value
    )

    # ----------------------------------------------
    # 題目
    # ----------------------------------------------

    series = "+".join(
        binom(n, k)
        for k in indices
    )

    correct_label = (
        rf"2^{{{n-2}}}"
    )

    # 常見錯誤：
    # 2^(n-1)：忘記題目只有一半
    # 2^n：直接套完整係數和
    # 2^(n-3)：又多除一次 2
    distractors = [
        rf"2^{{{n-1}}}",
        rf"2^{{{n}}}",
        rf"2^{{{n-3}}}",
    ]

    options = make_multiple_choice(
        correct_label,
        distractors,
    )

    # ----------------------------------------------
    # 配對解析
    # ----------------------------------------------

    pair_lines = []

    for k in indices:

        pair_lines.append(
            rf"{binom(n, k)}"
            rf"="
            rf"{binom(n, n-k)}"
        )

    pairs_latex = (
        r"\qquad ".join(
            pair_lines
        )
    )

    complete_even_series = (
        rf"{binom(n, 0)}"
        rf"+{binom(n, 2)}"
        rf"+\cdots"
        rf"+{binom(n, n)}"
    )

    question = rf"""
求下列式子之值，請選出正確答案：

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

本題中的項可以配對：

$$
{pairs_latex}
$$

因此題目中的每一項，都能與另一半的偶數下標項配對。

設原式為 $S$，則：

$$
2S
=
{complete_even_series}
$$

而完整的偶數下標係數和為：

$$
2^{{{n}-1}}
$$

所以：

$$
2S=2^{{{n}-1}}
$$

兩邊除以 $2$：

$$
S=2^{{{n}-2}}
$$

因此答案為：

$$
\boxed{{2^{{{n-2}}}}}
$$
"""

    return {
        "type": "multiple_choice",
        "question": question,
        "answer": correct_label,
        "options": options,
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

    # ----------------------------------------------
    # 實際驗證
    # ----------------------------------------------

    actual_answer = verify_sum(
        n,
        indices,
    )

    expected_value = (
        2 ** (n - 1)
    )

    assert (
        actual_answer
        == expected_value
    )

    # ----------------------------------------------
    # 題目
    # ----------------------------------------------

    series = "+".join(
        binom(n, k)
        for k in indices
    )

    correct_label = (
        rf"2^{{{n-1}}}"
    )

    # 常見錯誤：
    # 2^n：把所有係數都相加
    # 2^(n-2)：多除一次 2
    # 0：直接把 (1-1)^n 當答案
    distractors = [
        rf"2^{{{n}}}",
        rf"2^{{{n-2}}}",
        "0",
    ]

    options = make_multiple_choice(
        correct_label,
        distractors,
    )

    question = rf"""
求下列式子之值，請選出正確答案：

$$
{series}
$$
"""

    solution = rf"""
### 解析

設偶數下標係數和為 $E$，奇數下標係數和為 $O$。

由：

$$
(1+1)^{{{n}}}=2^{{{n}}}
$$

得到：

$$
E+O=2^{{{n}}}
$$

再由：

$$
(1-1)^{{{n}}}=0
$$

得到：

$$
E-O=0
$$

因此：

$$
E=O
$$

所以：

$$
E=O=2^{{{n}-1}}
$$

本題要求完整的{label}下標係數和，因此答案為：

$$
\boxed{{2^{{{n-1}}}}}
$$
"""

    return {
        "type": "multiple_choice",
        "question": question,
        "answer": correct_label,
        "options": options,
        "solution": solution,
    }


# ==================================================
# 子題 4
# 帶等比權重的二項式級數
# ==================================================

def weighted_term_latex(n, a, k):
    """
    產生級數第 k 項。
    專門處理負權重的正負號。
    """

    combination = binom(
        n,
        k,
    )

    if k == 0:
        return combination

    # ----------------------------------------------
    # 正數 a
    # ----------------------------------------------

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
                factor = (
                    rf"{a}^{{{k}}}"
                )

        return (
            "+"
            + factor
            + combination
        )

    # ----------------------------------------------
    # 負數 a
    # ----------------------------------------------

    abs_a = abs(a)

    if k == 1:

        magnitude = str(
            abs_a
        )

    else:

        magnitude = (
            rf"{abs_a}^{{{k}}}"
        )

    if k % 2 == 1:
        sign = "-"
    else:
        sign = "+"

    return (
        sign
        + magnitude
        + combination
    )


def make_weighted_series(n, a):
    """
    顯示：
    C(n,0) + aC(n,1) + a²C(n,2) + ...
    """

    pieces = [
        binom(n, 0)
    ]

    # 前面顯示 k=1,2,3
    for k in range(1, 4):

        pieces.append(
            weighted_term_latex(
                n,
                a,
                k,
            )
        )

    pieces.append(
        r"+\cdots"
    )

    # 最後一項
    pieces.append(
        weighted_term_latex(
            n,
            a,
            n,
        )
    )

    return "".join(pieces)


def generate_distractor_bases(a):
    """
    子題4常見錯誤。

    正確底數 = 1+a
    """

    correct_base = (
        1 + a
    )

    candidates = [
        a,                  # 忘記 1
        1 - a,              # 1+a 看成 1-a
        abs(correct_base),  # 負底數變正
        -correct_base,      # 正負號反轉
        a - 1,
        abs(a),
        -abs(a),
        1 + abs(a),
        1 - abs(a),
        correct_base + 1,
        correct_base - 1,
    ]

    result = []

    for base in candidates:

        if base == correct_base:
            continue

        if base in result:
            continue

        result.append(base)

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

        correct_base = (
            1 + a
        )

        # a=-1 不會被抽到
        assert correct_base != 0

        correct_value = (
            correct_base ** n
        )

        distractor_bases = (
            generate_distractor_bases(
                a
            )
        )

        valid_distractors = []

        used_values = {
            correct_value
        }

        # ------------------------------------------
        # 防止「看起來不同但數學等價」
        #
        # 例如 n 為偶數時：
        # 2^6 = (-2)^6
        # 不能同時成為兩個選項
        # ------------------------------------------

        for base in distractor_bases:

            value = (
                base ** n
            )

            if value in used_values:
                continue

            used_values.add(
                value
            )

            valid_distractors.append(
                base
            )

            if (
                len(valid_distractors)
                == 3
            ):
                break

        if len(valid_distractors) == 3:
            break

    # ----------------------------------------------
    # 正確答案
    # ----------------------------------------------

    correct_label = (
        power_latex(
            correct_base,
            n,
        )
    )

    # ----------------------------------------------
    # 選項
    # ----------------------------------------------

    option_bases = [
        correct_base,
        *valid_distractors,
    ]

    option_labels = [
        power_latex(
            base,
            n,
        )
        for base in option_bases
    ]

    # 字串不可重複
    assert (
        len(set(option_labels))
        == 4
    )

    # 數學值不可重複
    option_values = [
        base ** n
        for base in option_bases
    ]

    assert (
        len(set(option_values))
        == 4
    )

    options = (
        make_multiple_choice(
            correct_label,
            [
                label
                for label in option_labels
                if label != correct_label
            ],
        )
    )

    # ----------------------------------------------
    # 題目
    # ----------------------------------------------

    series = (
        make_weighted_series(
            n,
            a,
        )
    )

    if a > 0:

        binomial_latex = (
            rf"(1+{a})^{{{n}}}"
        )

    else:

        binomial_latex = (
            rf"(1-{abs(a)})^{{{n}}}"
        )

    question = rf"""
求下列式子之值，請選出正確答案：

$$
{series}
$$
"""

    solution = rf"""
### 解析

由二項式定理：

$$
(1+a)^n
=
\binom{{n}}{{0}}
+a\binom{{n}}{{1}}
+a^2\binom{{n}}{{2}}
+\cdots
+a^n\binom{{n}}{{n}}
$$

觀察本題的等比權重，可得：

$$
a={a}
$$

因此原式就是：

$$
{binomial_latex}
$$

計算括號內：

$$
1+({a})={correct_base}
$$

所以原式為：

$$
\boxed{{{correct_label}}}
$$

不需要將次方展開成巨大整數。
"""

    return {
        "type": "multiple_choice",
        "question": question,
        "answer": correct_label,
        "options": options,
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