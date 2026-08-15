const optionsDiv = document.getElementById("options");
const resultDiv = document.getElementById("result");

let selectedIndex = null;
let correctIndex = null;

generateQuestion();

document
.getElementById("submitBtn")
.addEventListener("click", submitAnswer);

document
.getElementById("nextBtn")
.addEventListener("click", generateQuestion);

function generateQuestion(){

    resultDiv.innerHTML = "";

    selectedIndex = null;

    optionsDiv.innerHTML = "";

    let data;

    do{
        data = buildQuestion();
    }
    while(!data.valid);

    document.getElementById("questionText").innerHTML =
        `${data.expression} ${data.sign} 0`;

    const choices = [];

    choices.push({
        text:data.correctAnswer,
        correct:true
    });

    data.distractors.forEach(d=>{
        choices.push({
            text:d,
            correct:false
        });
    });

    shuffle(choices);

    correctIndex =
        choices.findIndex(
            c=>c.correct
        );

    const labels =
        ["A","B","C","D"];

    choices.forEach((choice,index)=>{

        const card =
            document.createElement("div");

        card.className =
            "option-card";

        card.dataset.index =
            index;

        card.innerHTML = `
            <div class="option-title">
                ${labels[index]}
            </div>

            <div class="option-text">
                ${choice.text}
            </div>
        `;

        card.addEventListener(
            "click",
            ()=>selectOption(index)
        );

        optionsDiv.appendChild(card);
    });
}

function buildQuestion(){

    const a =
        randomInt(-20,20,true);

    const r1 =
        randomInt(-10,10,false);

    let r2 =
        randomInt(-10,10,false);

    if(r1===r2){
        return {valid:false};
    }

    const b =
        -a*(r1+r2);

    const c =
        a*r1*r2;

    if(
        b<-20 || b>20 ||
        c<-20 || c>20
    ){
        return {valid:false};
    }

    const D =
        b*b-4*a*c;

    if(D<=0){
        return {valid:false};
    }

    if(D>900){
        return {valid:false};
    }

    const sqrtD =
        Math.sqrt(D);

    if(!Number.isInteger(sqrtD)){
        return {valid:false};
    }

    const signList =
        [">","<","≥","≤"];

    const sign =
        signList[
            Math.floor(
                Math.random()*4
            )
        ];

    const x1 =
        Math.min(r1,r2);

    const x2 =
        Math.max(r1,r2);

    const correctAnswer =
        buildAnswer(
            a,
            sign,
            x1,
            x2
        );

    const distractors =
        buildDistractors(
            a,
            sign,
            x1,
            x2,
            correctAnswer
        );

    return{
        valid:true,
        expression:
            formatExpression(
                a,b,c
            ),
        sign,
        correctAnswer,
        distractors
    };
}

function buildAnswer(
    a,
    sign,
    x1,
    x2
){

    const up = a>0;

    if(up){

        if(sign===">"){
            return outside(x1,x2,false);
        }

        if(sign==="<"){
            return inside(x1,x2,false);
        }

        if(sign==="≥"){
            return outside(x1,x2,true);
        }

        return inside(x1,x2,true);
    }

    if(sign===">"){
        return inside(x1,x2,false);
    }

    if(sign==="<"){
        return outside(x1,x2,false);
    }

    if(sign==="≥"){
        return inside(x1,x2,true);
    }

    return outside(x1,x2,true);
}

function buildDistractors(
    a,
    sign,
    x1,
    x2,
    correct
){

    const set =
        new Set();

    const insideWrong =
        inside(x1,x2,false);

    const outsideWrong =
        outside(x1,x2,false);

    const insideEqual =
        inside(x1,x2,true);

    const outsideEqual =
        outside(x1,x2,true);

    [
        insideWrong,
        outsideWrong,
        insideEqual,
        outsideEqual,

        inside(-x2,-x1,false),
        outside(-x2,-x1,false),

        inside(-x2,-x1,true),
        outside(-x2,-x1,true)

    ].forEach(item=>{

        if(item!==correct){
            set.add(item);
        }

    });

    return [...set].slice(0,3);
}

function inside(
    x1,
    x2,
    include
){

    const l =
        include ? "[" : "(";

    const r =
        include ? "]" : ")";

    return `${l}${x1}, ${x2}${r}`;
}

function outside(
    x1,
    x2,
    include
){

    const l =
        include ? "[" : "(";

    const r =
        include ? "]" : ")";

    return `(-∞, ${x1}${r} ∪ ${l}${x2}, +∞)`;
}

function formatExpression(
    a,b,c
){

    let text = "";

    if(a===1){
        text += "x²";
    }
    else if(a===-1){
        text += "-x²";
    }
    else{
        text += `${a}x²`;
    }

    if(b>0){
        text += `+${b}x`;
    }

    if(b<0){
        text += `${b}x`;
    }

    if(c>0){
        text += `+${c}`;
    }

    if(c<0){
        text += `${c}`;
    }

    return text;
}

function selectOption(index){

    document
    .querySelectorAll(".option-card")
    .forEach(card=>{
        card.classList.remove("selected");
    });

    document
    .querySelector(
        `[data-index="${index}"]`
    )
    .classList.add("selected");

    selectedIndex = index;
}

function submitAnswer(){

    if(selectedIndex===null){

        resultDiv.innerHTML =
            '<span class="wrong">請先選擇答案</span>';

        return;
    }

    if(selectedIndex===correctIndex){

        resultDiv.innerHTML =
            '<span class="correct">🎉 答對！</span>';

    }else{

        resultDiv.innerHTML =
            '<span class="wrong">😢 答錯，再試一次。</span>';
    }
}

function randomInt(
    min,
    max,
    excludeZero
){

    let n;

    do{

        n =
            Math.floor(
                Math.random()
                *(max-min+1)
            )+min;

    }while(
        excludeZero &&
        n===0
    );

    return n;
}

function shuffle(array){

    for(
        let i=array.length-1;
        i>0;
        i--
    ){

        const j =
            Math.floor(
                Math.random()
                *(i+1)
            );

        [array[i],array[j]]
        =
        [array[j],array[i]];
    }
}
