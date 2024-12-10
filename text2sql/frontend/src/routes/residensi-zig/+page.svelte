<script lang="ts">
	import Zig from '$lib/assets/img/zig.png';
	import { currentPage } from '$lib/store';
	import { onMount } from 'svelte';
	
	onMount(async () => {
		$currentPage = 'residensi-zig';
	});
</script>

<img src={Zig} alt="" class="object-cover h-full w-full" />
