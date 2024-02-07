let my_list = [34, 23, "hello"];

console.log(my_list);
console.log(my_list[1]);

const mapget = (item, index) => {
    return `mapped: index:${index} -> ${item}`;
}

let res1 = my_list.map(mapget);
console.log(res1);

let res2 = my_list.map((item, index) => {
    return `mapped: index:${index} -> ${item}`;
});
console.log(res2);

const myob = {
    'firstname': 'fred',
    age: 12
};
console.log("myob:", myob);

const new_ob = {...myob, eyes: "Blue"};
console.log("new_ob:", new_ob);

const { firstname, age } = myob;
console.log("name:", firstname);
console.log("age:", age);

console.log("new_ob.eyes:", new_ob.eyes);
console.log("new_ob.eyes:", new_ob['eyes']);