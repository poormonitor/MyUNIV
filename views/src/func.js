import { majors } from "./const";

const getMustString = (must) => {
    if (!must) {
        return majors[0];
    }

    let now = String(must);
    let cnt = now[0];
    let ans = [];
    for (let i = 1; i < now.length; i++) {
        ans.push(majors[Number(now[i])]);
    }
    return ans.join(", ") + " " + `(必选${Number(cnt)}门)`;
};

const fixInteger = (obj, name) => {
    obj[name] = obj[name].map((item) => Number(item));
};

const filterEmptyObject = (obj) => {
    let filteredObj = {};
    for (let key in obj) {
        if (obj[key] !== "") {
            filteredObj[key] = obj[key];
        }
    }
    return filteredObj;
};

function compareObjects(obj1, obj2) {
    if (typeof obj1 !== "object" || typeof obj2 !== "object") {
        return obj1 == obj2;
    }

    const keys1 = Object.keys(obj1);
    const keys2 = Object.keys(obj2);

    if (keys1.length !== keys2.length) {
        return false;
    }

    for (let key of keys1) {
        if (!obj2.hasOwnProperty(key)) {
            return false;
        }

        if (!compareObjects(obj1[key], obj2[key])) {
            return false;
        }
    }

    return true;
}

function findMaxValue(array, n) {
    let max = null;

    for (let i = 0; i < array.length; i++) {
        if (!max || (array[i] <= n && array[i] > max)) {
            max = array[i];
        }
    }

    return max;
}

const base64toBlob = (base64) => {
    let bstr = atob(base64);
    let n = bstr.length;
    let u8arr = new Uint8Array(n);
    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], { type: "application/octet-stream" });
};

export {
    getMustString,
    fixInteger,
    filterEmptyObject,
    compareObjects,
    findMaxValue,
    base64toBlob,
};
