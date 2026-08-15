const conditionsDiv = document.getElementById("conditions");
const optionsDiv = document.getElementById("options");

generateQuestion();

function generateQuestion() {

    optionsDiv.innerHTML = "";

    const aSign = Math.random() < 0.5 ? 1 : -1;

    const bStates = ["positive", "zero", "negative"];
    const cStates = ["positive", "zero", "negative"];

    const bState = bStates[Math.floor(Math.random() * 3)];
    const cState = cStates[Math.floor(Math.random() * 3)];

    conditionsDiv.innerHTML = `
        ${aSign > 0 ? "a > 0" : "a < 0"}<br>
        ${stateToText("b", bState)}<br>
        ${stateToText("c", cState)}
    `;

    const correctGraph = createGraph(
        aSign,
        bState,
        cState
    );

    const graphs = [];

    graphs.push(correctGraph);

    graphs.push(
        createGraph(
            -aSign,
            bState,
            cState
        )
    );

    graphs.push(
        createGraph(
            aSign,
            flipState(bState),
            cState
        )
    );

    graphs.push(
        createGraph(
            aSign,
            bState,
            flipState(cState)
        )
    );

    graphs.push(
        createGraph(
            -aSign,
            flipState(bState),
            flipState(cState)
        )
    );

    shuffle(graphs);

    const labels = ["A", "B", "C", "D", "E"];

    graphs.forEach((graph, index) => {

        const card = document.createElement("div");

        card.className = "option-card";

        card.innerHTML = `
            <div class="option-title">
                ${labels[index]}
            </div>

            <canvas
                id="canvas${index}"
                width="220"
                height="180">
            </canvas>
        `;

        optionsDiv.appendChild(card);

        drawParabola(
            graph.a,
            graph.b,
            graph.c,
            `canvas${index}`
        );
    });

    document.getElementById("result").innerHTML =
        "題目生成成功";
}

function createGraph(aSign, bState, cState) {

    const a =
        aSign > 0
            ? randomInt(1, 4)
            : -randomInt(1, 4);

    let b = 0;

    if (bState === "positive")
        b = randomInt(1, 5);

    if (bState === "negative")
        b = -randomInt(1, 5);

    let c = 0;

    if (cState === "positive")
        c = randomInt(1, 4);

    if (cState === "negative")
        c = -randomInt(1, 4);

    return { a, b, c };
}

function drawParabola(a, b, c, canvasId) {

    const canvas =
        document.getElementById(canvasId);

    const ctx =
        canvas.getContext("2d");

    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(
        0,
        0,
        width,
        height
    );

    ctx.beginPath();
    ctx.moveTo(0, height / 2);
    ctx.lineTo(width, height / 2);
    ctx.strokeStyle = "#888";
    ctx.lineWidth = 1;
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();

    ctx.beginPath();

    let firstPoint = true;

    for (
        let px = 0;
        px <= width;
        px++
    ) {

        const x =
            (px - width / 2) / 20;

        const y =
            a * x * x +
            b * x +
            c;

        const py =
            height / 2 -
            y * 20;

        if (firstPoint) {

            ctx.moveTo(px, py);

            firstPoint = false;

        } else {

            ctx.lineTo(px, py);

        }
    }

    ctx.strokeStyle = "#1976d2";
    ctx.lineWidth = 3;
    ctx.stroke();
}

function flipState(state) {

    if (state === "positive")
        return "negative";

    if (state === "negative")
        return "positive";

    return "positive";
}

function stateToText(name, state) {

    if (state === "positive")
        return `${name} > 0`;

    if (state === "negative")
        return `${name} < 0`;

    return `${name} = 0`;
}

function randomInt(min, max) {

    return Math.floor(
        Math.random() *
        (max - min + 1)
    ) + min;
}

function shuffle(array) {

    for (
        let i = array.length - 1;
        i > 0;
        i--
    ) {

        const j =
            Math.floor(
                Math.random() *
                (i + 1)
            );

        [
            array[i],
            array[j]
        ] =
        [
            array[j],
            array[i]
        ];
    }
}
