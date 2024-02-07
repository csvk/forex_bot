console.log("Hello");

var num;
console.log('num: ' + num);

let num2;
console.log('num2: ' + num2);

var abool = true;
var anull = null;
var anumber = 45.5;
var astring = "I am a string";

console.log("abool:", typeof abool);
console.log("anull:", typeof anull);
console.log("anumber:", typeof anumber);
console.log("astring:", typeof astring);
console.log("num:", typeof num);


if(anumber === 45.5) {
    console.log("anumber === 45.5");
}


if(anumber !== 40.5) {
    console.log("anumber !== 40.5");
}

if("22" == 22) {
    console.log("'22' == 22");
}


if(!anull) {
    console.log("!anull");
}

if(!num) {
    console.log("!num");
}

if(num === null) {
    console.log("num === null");
}
if(num === undefined) {
    console.log("num === undefined");
}

if(abool) {
    console.log("abool:", abool);
}

if (num) {
    console.log("num undefined");
} else if(num2 === null) {
    console.log("num2 undefined");
} else {
    console.log("blah");
}


if(!num) {
    console.log("!num");
    var s = 56;
    let t = 76;
    console.log("inner s:", s);
    console.log("inner t:", t);
} else {
    console.log("num is ok!");
}
console.log("s:", s);


var n1 = 34;
var n2 = "34";


console.log("n1:", n1);
n1 += 10;
console.log("n1:", n1);

console.log("n2:", n2);
n2 += 10;
console.log("n2:", n2);







