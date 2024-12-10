<script lang="ts">
	import '../app.scss';
	import { browser } from '$app/environment';
	import {
		Content,
		Header,
		HeaderNav,
		HeaderNavItem,
		HeaderUtilities
	} from 'carbon-components-svelte';
	import { register } from 'swiper/element/bundle';
	import WatsonAssistant from '$lib/components/WatsonAssistant.svelte';
	import 'carbon-components-svelte/css/all.css';
	import SettingsAdjust from 'carbon-icons-svelte/lib/SettingsAdjust.svelte';
	let theme = 'g10'; // "white" | "g10" | "g80" | "g90" | "g100"
	$: {
		if (browser) {
			document.documentElement.setAttribute('theme', theme);
		}
	}
	register();
</script>

<svelte:head>
	<title>watsonx Demo | IBM Client Engineering</title>
</svelte:head>

<div class="box">
	<div class="header">
		<Header company="IBM" href="/">
			<svelte:fragment slot="platform">
				<div>watson<span style="color: #0f62fe;">x</span> Demo</div>
			</svelte:fragment>
			<HeaderNav>
				<HeaderNavItem href="/the-connaught-one" text="The Connaught One" />
				<HeaderNavItem href="/the-minh" text="The MINH" />
				<HeaderNavItem href="/residensi-zig" text="Residensi ZIG" />
			</HeaderNav>
			<HeaderUtilities>
				<HeaderNav>
					<HeaderNavItem href="/settings">
						<SettingsAdjust size={20} fill="white" />
					</HeaderNavItem>
				</HeaderNav>
			</HeaderUtilities>
		</Header>
	</div>
	<div class="content">
		<Content style="height: 100%; padding: 0;">
			<slot />
		</Content>
	</div>
</div>

<WatsonAssistant />

<style>
	:global(header.bx--header) {
		position: relative;
	}

	:global(.bx--header__global button > svg) {
		display: inline-block;
		vertical-align: middle;
	}
</style>
