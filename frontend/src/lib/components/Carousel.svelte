<script lang="ts">
	import { onMount } from 'svelte';

	import type { SwiperContainer } from 'swiper/element';

	let swiperEl: SwiperContainer | undefined;

	export let images: string[];

	onMount(() => {
		const swiperParams = {
			navigation: true,
			pagination: true,
			slidesPerView: 1,
			// loop: true
		};
		Object.assign(swiperEl!, swiperParams);
		swiperEl!.initialize();
	});
</script>

<div class="swiper">
	<swiper-container init="false" bind:this={swiperEl} style="--swiper-navigation-size: 20px;">
		{#each images as img}
			<swiper-slide>
				<img class="carousel-image" src={img} alt="" />
			</swiper-slide>
		{/each}
	</swiper-container>
</div>
