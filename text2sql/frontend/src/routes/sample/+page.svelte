<!-- <script lang="ts">
	import Zig from '$lib/assets/img/zig.png';
	import { currentPage } from '$lib/store';
	import { onMount } from 'svelte';
	
	onMount(async () => {
		$currentPage = 'residensi-zig';
	});
</script>

<img src={Zig} alt="" class="object-cover h-full w-full" /> -->

<script lang="ts">
	// Importing necessary resources
	import { onMount } from 'svelte';
	import { currentPage } from '$lib/store'; // Assuming $lib/store is a Svelte store
	import villa from '$lib/assets/img/villa.jpg'; // Image import

	// This will run when the component is mounted
	onMount(async () => {
		// Set the current page when the component mounts
		$currentPage = 'beach_house';
	});

	// Define the properties (instead of using useState and useEffect in React)
	let property = {
		name: 'Luxury Villa',
		location: 'Los Angeles, CA',
		price: '$1,200,000',
		image: villa
	};
</script>

<!-- HTML Section for Property Details -->
<div class="property-detail">
	<img src={property.image} alt={property.name} class="property-detail-image" />
	<div>
		<div class="property-details">
			<h2>{property.name}</h2>
			<p>{property.location}</p>
			<p>{property.price}</p>
		</div>
		<button class="reserve-button">Reserve Now</button>
	</div>
</div>

<!-- Styles can go here if needed -->
<style scoped>
	.property-detail {
		padding: 20px;
		font-size: 1.5 em;
		display: flex;
		justify-content: flex-start;
		font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode',
			Geneva, Verdana, sans-serif;
	}

	.property-detail-image {
		width: 900px;
		height: 500px;
		object-fit: cover;
		margin-right: 20px;
	}

	.property-details {
		flex: 2;
	}

	.reserve-button {
		background-color: #e6c270;
		/* Green background */
		color: black;
		/* White text */
		padding: 10px 20px;
		/* Vertical and horizontal padding */
		font-size: 16px;
		/* Larger font size */
		transition: background-color 0.3s ease;
		/* Smooth color transition */
		width: 200px;
		height: 50px;
		border: none;
		font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode',
			Geneva, Verdana, sans-serif;
	}

	.reserve-button:hover {
		background-color: #c1a35e;
		/* Darker green when hovered */
		cursor: pointer;
		/* Pointer cursor */
	}

	.features {
		background-color: #e6c270;
		padding: 0px 20px;
		font-size: 2em;
		font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode',
			Geneva, Verdana, sans-serif;
	}
</style>
