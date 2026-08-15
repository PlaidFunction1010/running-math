const conditionsDiv = document.getElementById("conditions");

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

document.getElementById("result").innerHTML =
"題目生成成功";
