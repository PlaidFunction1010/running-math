const conditionsDiv = document.getElementById("conditions");
const optionsDiv = document.getElementById("options");

generateQuestion();

function generateQuestion() {

    optionsDiv.innerHTML = "";

    const aSign = Math.random() < 0.5 ? 1 : -1;

    const bStates = ["positive", "zero", "negative"];
    const cStates = ["positive", "zero", "negative"];

    const bState =
        bStates[Math.floor(Math.random() * 3)];

    const cState =
        cStates[Math.floor(Math.random() * 3)];

    conditionsDiv.innerHTML = `
        ${aSign > 0 ? "a > 0" : "a < 0"}<br>
        ${stateToText("b", bState)}<br>
        ${stateToText("c", cState)}
    `;

    const correctGraph =
        createGraph(
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
        aSign > 0 ? 1 : -1;

    let b = 0;

    if (bState === "positive") {
        b = 2;
    }

    if (bState === "negative") {
        b = -2;
    }

    let c = 0;

    if (cState === "positive") {
        c = 2;
    }

    if (cState === "negative") {
        c = -2;
    }

    return {
        a,
        b,
        c
    };
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

    const xMin = -5;
    const xMax = 5;

    const yMin = -5;
    const yMax = 5;

    const zeroX =
        ((0 - xMin) / (xMax - xMin))
        * width;

    const zeroY =
        height -
        ((0 - yMin) / (yMax - yMin))
        * height;

    ctx.strokeStyle = "#999";
    ctx.lineWidth = 1;

    ctx.beginPath();
    ctx.moveTo(0, zeroY);
    ctx.lineTo(width, zeroY);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(zeroX, 0);
    ctx.lineTo(zeroX, height);
    ctx.stroke();

    ctx.beginPath();

    let firstPoint = true;

    for (
        let px = 0;
        px <= width;
        px++
    ) {

        const x =
            xMin +
            (px / width)
            * (xMax - xMin);

        const y =
            a * x * x +
            b * x +
            c;

        const py =
            height -
            ((y - yMin) / (yMax - yMin))
            * height;

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

    if (state === "positive") {
        return "negative";
    }

    if (state === "negative") {
        return "positive";
    }

    return "positive";
}

function stateToText(name, state) {

    if (state === "positive") {
        return `${name} > 0`;
    }

    if (state === "negative") {
        return `${name} < 0`;
    }

    return `${name} = 0`;
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
        ] = [
            array[j],
            array[i]
        ];
    }
}
