<script setup>
import { NConfigProvider } from "naive-ui";
import { zhCN, dateZhCN } from "naive-ui";
import { useOsTheme, darkTheme } from "naive-ui";
import { computed, provide } from "vue";

const osThemeRef = useOsTheme();
const theme = computed(() => (osThemeRef.value === "dark" ? darkTheme : null));

/**
 * @type import('naive-ui').GlobalThemeOverrides
 */
const themeOverrides = {
	common: {
		fontFamily: "Inter, Noto Sans SC",
		primaryColor: "#2080f0FF",
		primaryColorHover: "#4098fcFF",
		primaryColorPressed: "#1060c9FF",
		primaryColorSuppl: "#4098fcFF",
	},
};

const collapsed = ref(window.innerWidth <= 768);
window.addEventListener("resize", () => {
	collapsed.value = window.innerWidth <= 768;
});
provide("darkTheme", osThemeRef.value === "dark");
provide("collapsed", collapsed);

const loadFontPromise = fetch(
	"https://fonts.googleapis.com/css?family=Inter:500,800%7CNoto+Sans+SC:500,800&display=swap",
).then(async (res) => {
	const style = document.createElement("style");
	style.innerHTML = await res.text();
	document.head.appendChild(style);
});
</script>

<template>
	<n-config-provider
		class="h-full"
		:locale="zhCN"
		:date-locale="dateZhCN"
		:theme="theme"
		:theme-overrides="themeOverrides"
	>
		<n-global-style />
		<n-dialog-provider>
			<router-view></router-view>
		</n-dialog-provider>
	</n-config-provider>
</template>

<style>
html,
body,
#app {
	height: 100%;
}
</style>
