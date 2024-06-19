<script setup>
import { provide, ref, watch, computed } from 'vue';
import { onLaunch } from '@dcloudio/uni-app';

const s = ref('');

const mymajors = ref([]);

const mymust = ref([]);
const myrank = ref(null);
const mydisabled = ref(0);

const majors = {
	add: function (id) {
		if (mymajors.value.length >= 200) {
			uni.showToast({
				title: '最多收藏200个',
				icon: 'error',
				duration: 2000
			});
		} else {
			mymajors.value.push(id);
			this.update();
		}
	},
	remove: function (id) {
		mymajors.value = mymajors.value.filter((item) => item != id);
		this.update();
	},
	has: function (id) {
		return mymajors.value.includes(id);
	},
	get: function () {
		return mymajors.value;
	},
	clean: function () {
		mymajors.value = [];
	},
	update: function () {
		uni.setStorageSync('myuniv_my_majors', mymajors.value);
	},
	fetch: function () {
		mymajors.value = uni.getStorageSync('myuniv_my_majors') || [];
	},
	length: computed(() => mymajors.value.length)
};

const infos = {
	setMust: function (musts) {
		mymust.value = musts;
		this.update();
	},
	setRank: function (rank) {
		myrank.value = rank;
		this.update();
	},
	setDisabled: function (disabled) {
		mydisabled.value = disabled;
		this.update();
	},
	getMust: function () {
		return mymust.value;
	},
	getRank: function () {
		return myrank.value;
	},
	getDisabled: function () {
		return mydisabled.value;
	},
	isSetted: function () {
		return mydisabled.value || mymust.value.length > 0 || myrank.value > 0;
	},
	update: function () {
		uni.setStorageSync('myuniv_my_infos', {
			mymust: mymust.value,
			myrank: myrank.value,
			mydisabled: mydisabled.value
		});
	},
	fetch: function () {
		let info = uni.getStorageSync('myuniv_my_infos');
		if (!info) return;
		mymust.value = info.mymust;
		myrank.value = info.myrank;
		mydisabled.value = info.mydisabled;
	}
};

provide('s', s);
provide('majors', majors);
provide('infos', infos);

onLaunch(() => {
	infos.fetch();
	majors.fetch();
});
</script>

<style lang="scss">
@import './styles/generate.scss';
@import './styles/expand.scss';

page {
	background-color: #fafafa;
}

.uni-section {
	background-color: rgba(255, 255, 255, 0) !important;
}

.uni-popup__wrapper {
	border-radius: 15px;
}

.main-content {
	margin: 20px 15px;
	padding: 10px 16px;
	border-radius: 20px;
	background-color: #fff;
}

button[type='info']:hover {
	background-color: #005cc5;
}

button[type='info'] {
	color: #fff;
	background-color: #0075ff;
}

.floatButton .uni-fab__circle {
	width: 40px !important;
	height: 40px !important;
}

.floatButton .uni-fab__circle .uni-icons {
	font-size: 24px !important;
}
</style>
