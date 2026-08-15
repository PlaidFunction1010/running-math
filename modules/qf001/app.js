const conditionsDiv = document.getElementById("conditions");

const aSign = Math.random() < 0.5 ? ">" : "<";

const bPool = [">", "=", "<"];
const cPool = [">", "=", "<"];

const bSign = bPool[Math.floor(Math.random() * 3)];
const cSign = cPool[Math.floor(Math.random() * 3)];

conditionsDiv.innerHTML = `
a ${aSign} 0<br>
b ${bSign} 0<br>
c ${cSign} 0
`;

document.getElementById("result").innerHTML =
"題目生成成功";
