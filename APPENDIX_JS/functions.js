function frodo(num) {
    console.log("frodo:", num);
}

const bilbo = function(num) {
    console.log("bilbo:", num);
}

const gimli = (num) => {
    console.log("gimli:", num);
}

const legolas = (num) => console.log("legolas:", num);


frodo(45);
bilbo(45);
gimli(45);
legolas(45);


const elrond = (num) => {
    return `elrond ${num}`; 
}

const sam = (num) => `sam ${num}`;

console.log(elrond(54));
console.log(sam(54));















