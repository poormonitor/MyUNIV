import md5 from "crypto-js/md5";

const GetYearMonth = (timestamp) => {
    let date = new Date(timestamp);
    let year = date.getFullYear();
    let month = date.getMonth() + 1;
    return `${year}年${month}月`;
};

const GetFullTime = (timestamp) => {
    let date = new Date(timestamp);
    return date.toISOString().substring(0, 19).replace("T", " ");
};

const blobToHash = async (blob) => {
    return new Promise((resolve) => {
        let reader = new FileReader();
        reader.readAsBinaryString(blob);
        reader.onloadend = () => {
            let hash = md5(reader.result).toString();
            resolve(hash);
        };
    });
};

export { GetYearMonth, GetFullTime, blobToHash };
