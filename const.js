const provinces = {
    11: "北京",
    12: "天津",
    13: "河北",
    14: "山西",
    15: "内蒙古",
    21: "辽宁",
    22: "吉林",
    23: "黑龙江",
    31: "上海",
    32: "江苏",
    33: "浙江",
    34: "安徽",
    35: "福建",
    36: "江西",
    37: "山东",
    41: "河南",
    42: "湖北",
    43: "湖南",
    44: "广东",
    45: "广西",
    46: "海南",
    50: "重庆",
    51: "四川",
    52: "贵州",
    53: "云南",
    54: "西藏",
    61: "陕西",
    62: "甘肃",
    63: "青海",
    64: "宁夏",
    65: "新疆",
    81: "香港",
    100: "军校",
    0: "未知",
};

const majors = [
    "不提科目要求",
    "物理",
    "化学",
    "生物",
    "地理",
    "历史",
    "思想政治",
    "技术",
];

const majors_short = ["无", "物", "化", "生", "地", "史", "政", "技"];

const recommends = [
    { label: "冗余", tag: "default", color: "#D3D3D3" },
    { label: "保底", tag: "primary", color: "#4098FC" },
    { label: "稳妥", tag: "success", color: "#36AD6A" },
    { label: "冲刺", tag: "warning", color: "#FCB040" },
    { label: "困难", tag: "error", color: "#DE576D" },
];

const batches = {
    0: "全部",
    1: "本科",
    2: "专科",
};

export { provinces, majors, majors_short, recommends, batches };
