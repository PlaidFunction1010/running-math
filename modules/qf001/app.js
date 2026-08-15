const conditionsDiv = document.getElementById("conditions");
const optionsDiv = document.getElementById("options");

const aPositive = Math.random() < 0.5;

const bStates = ["positive", "zero", "negative"];
const cStates = ["positive", "zero", "negative"];

const bState = bStates[Math.floor(Math.random() * 3)];
const cState = cStates[Math.floor(Math.random() * 3)];

const aText = aPositive ? "a > 0" : "a < 0";

const bText =
    bState === "positive"
        ? "b > 0"
        : bState === "negative"
        ? "b < 0"
        : "b = 0";

const cText =
    cState === "positive"
        ? "c > 0"
        : cState === "negative"
        ? "c < 0"
        : "c = 0";

conditionsDiv.innerHTML = `
${aText}<br>
${bText}<br>
${cText}
`;

const labels = ["A", "B", "C", "D", "E"];

for (let i = 0; i < labels.length; i++) {

    const card = document.createElement("div");

    card.className = "option-card";

    card.innerHTML = `
        <div class="option-title">${labels[i]}</div>

        <canvas
            width="220"
            height="180">
        </canvas>
    `;

    optionsDiv.appendChild(card);
}

document.getElementById("result").innerHTML =
"選項建立成功";
