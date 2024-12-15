<script lang="ts">
	import Zig from '$lib/assets/img/abc-page.png';
	import { currentPage } from '$lib/store';
	import { onMount } from 'svelte';
	
	onMount(async () => {
		$currentPage = 'abc-residence';
	});
</script>

<img src={Zig} alt="" class="object-cover h-full w-full" />
