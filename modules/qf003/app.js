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

    let q;

    do{
        q = buildQuestion();
    }
    while(!q.valid);

    document.getElementById("questionText").innerHTML =
        `${q.expression} ${q.sign} 0`;

    const choices = [];

    choices.push({
        text:q.answer,
        correct:true
    });

    q.distractors.forEach(d=>{
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

    const b =
        randomInt(-20,20,false);

    const c =
        randomInt(-20,20,false);

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

    if(Number.isInteger(sqrtD)){
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

    const root1 =
        formatRoot(
            -b,
            -1,
            D,
            2*a
        );

    const root2 =
        formatRoot(
            -b,
            1,
            D,
            2*a
        );

    const ordered =
        orderRoots(
            a,b,D
        );

    const answer =
        buildAnswer(
            a,
            sign,
            ordered.left,
            ordered.right
        );

    const distractors =
        buildDistractors(
            ordered.left,
            ordered.right,
            answer
        );

    return{
        valid:true,
        expression:
            formatExpression(a,b,c),
        sign,
        answer,
        distractors
    };
}

function orderRoots(a,b,D){

    if(a>0){

        return{
            left:
                formatRoot(
                    -b,
                    -1,
                    D,
                    2*a
                ),
            right:
                formatRoot(
                    -b,
                    1,
                    D,
                    2*a
                )
        };
    }

    return{
        left:
            formatRoot(
                -b,
                1,
                D,
                2*a
            ),
        right:
            formatRoot(
                -b,
                -1,
                D,
                2*a
            )
    };
}

function formatRoot(base,sign,D,den){

    let numerator =
        `${base}`;

    if(sign===1){
        numerator += `+√${D}`;
    }else{
        numerator += `-√${D}`;
    }

    if(den===1){
        return numerator;
    }

    if(den===-1){
        return `-(${numerator})`;
    }

    return `(${numerator})/${den}`;
}

function buildAnswer(
    a,
    sign,
    left,
    right
){

    const up = a>0;

    if(up){

        if(sign===">"){
            return outside(left,right,false);
        }

        if(sign==="<"){
            return inside(left,right,false);
        }

        if(sign==="≥"){
            return outside(left,right,true);
        }

        return inside(left,right,true);
    }

    if(sign===">"){
        return inside(left,right,false);
    }

    if(sign==="<"){
        return outside(left,right,false);
    }

    if(sign==="≥"){
        return inside(left,right,true);
    }

    return outside(left,right,true);
}

function buildDistractors(
    left,
    right,
    correct
){

    const pool = [];

    pool.push(
        inside(left,right,false)
    );

    pool.push(
        outside(left,right,false)
    );

    pool.push(
        inside(left,right,true)
    );

    pool.push(
        outside(left,right,true)
    );

    pool.push(
        inside(right,left,false)
    );

    pool.push(
        outside(right,left,false)
    );

    const result = [];

    pool.forEach(item=>{

        if(
            item!==correct &&
            !result.includes(item)
        ){
            result.push(item);
        }

    });

    return result.slice(0,3);
}

function inside(
    a,
    b,
    include
){

    const l =
        include ? "[" : "(";

    const r =
        include ? "]" : ")";

    return `${l}${a}, ${b}${r}`;
}

function outside(
    a,
    b,
    include
){

    const l =
        include ? "[" : "(";

    const r =
        include ? "]" : ")";

    return `(-∞, ${a}${r} ∪ ${l}${b}, +∞)`;
}

function formatExpression(a,b,c){

    let text="";

    if(a===1){
        text+="x²";
    }
    else if(a===-1){
        text+="-x²";
    }
    else{
        text+=`${a}x²`;
    }

    if(b>0){
        text+=`+${b}x`;
    }

    if(b<0){
        text+=`${b}x`;
    }

    if(c>0){
        text+=`+${c}`;
    }

    if(c<0){
        text+=`${c}`;
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
