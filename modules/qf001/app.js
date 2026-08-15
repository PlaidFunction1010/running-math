const conditionsDiv = document.getElementById("conditions");
const optionsDiv = document.getElementById("options");

conditionsDiv.innerHTML = `
a > 0<br>
b < 0<br>
c = 0
`;

const labels = ["A", "B", "C", "D", "E"];

for (let i = 0; i < labels.length; i++) {

    const card = document.createElement("div");

    card.className = "option-card";

    card.innerHTML = `
        <div class="option-title">${labels[i]}</div>

        <canvas
            id="canvas${i}"
            width="220"
            height="180">
        </canvas>
    `;

    optionsDiv.appendChild(card);
}

drawDemoGraph();

function drawDemoGraph() {

    const canvas = document.getElementById("canvas0");

    const ctx = canvas.getContext("2d");

    const width = canvas.width;
    const height = canvas.height;

    ctx.clearRect(0, 0, width, height);

    // x軸
    ctx.beginPath();
    ctx.moveTo(0, height / 2);
    ctx.lineTo(width, height / 2);
    ctx.stroke();

    // y軸
    ctx.beginPath();
    ctx.moveTo(width / 2, 0);
    ctx.lineTo(width / 2, height);
    ctx.stroke();

    // 畫 y = x² - 2x

    ctx.beginPath();

    let firstPoint = true;

    for (let px = 0; px <= width; px++) {

        const x = (px - width / 2) / 20;

        const y = x * x - 2 * x;

        const py = height / 2 - y * 20;

        if (firstPoint) {
            ctx.moveTo(px, py);
            firstPoint = false;
        } else {
            ctx.lineTo(px, py);
        }
    }

    ctx.lineWidth = 3;
    ctx.stroke();
}

document.getElementById("result").innerHTML =
"第一條拋物線測試";
