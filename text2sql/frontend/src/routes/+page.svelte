<script lang="ts">
	import { Column, ClickableTile, Grid, Row, Tag } from 'carbon-components-svelte';
	import { USE_CASES } from '$lib/data/use_cases';
	import uem_sunrise_logo from '$lib/assets/img/uem-sunrise-logo.webp';

	import { currentPage } from '$lib/store';
	$currentPage = null;
</script>

<Grid fullWidth class="h-full" style="padding-left: 0">
	<Row class="h-full">
		<Column class="h-full bg-white" sm={{ span: 1, offset: 0 }}>
			<Grid class="h-full flex flex-col">
				<Row class="h-full">
					<Column class="prose lg:prose-xl flex flex-col justify-between h-full">
						<div class="pt-4">
							<div class="watsonx my-4">Building Communities of the Future</div>
							<img src={uem_sunrise_logo} alt="uem-sunrise-logo" class="w-40" />
							<p>
								UEM Sunrise brings together the talented and skilled, the imaginative and the
								courageous. We create sustainable environments loved by homeowners, acclaimed by
								investors and recognised by the industry. We believe in thinking big and acting
								quickly to unlock potential; to thrive in a changing world.
							</p>
						</div>
						<div class="pb-8 ibm-ce">Developed by IBM Client Engineering Malaysia</div>
					</Column>
				</Row>
			</Grid>
		</Column>
		<Column class="h-full">
			<Grid class="h-full flex flex-col">
				<Row>
					<Column>
						<div class="mt-8 grid grid-cols-3 gap-10">
							{#each USE_CASES as x}
								<ClickableTile href={x.url} class="rounded-lg shadow-lg">
									<img
										src={x.img}
										alt=""
										class="object-cover h-48 w-full rounded-lg shadow-lg mb-4"
									/>
									<div class="flex flex-col prose prose-stone">
										<div class="flex items-center">
											<div class="title">
												{x.title}
											</div>
										</div>
										<p class="py-2 flex-auto description" style="height: 100px;">
											{x.description}
										</p>
									</div>
								</ClickableTile>
							{/each}
						</div>
					</Column>
				</Row>
			</Grid>
		</Column>
	</Row>
</Grid>

<style lang="scss">
	@use '@carbon/styles/scss/type';

	:global(.bx--tag:first-child) {
		margin-left: 0;
	}
	.ibm-ce {
		@include type.type-style('body-01');
	}

	.watsonx {
		@include type.type-style('heading-05');
		// font-family: 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif;
		font-weight: 400;
	}

	.title {
		@include type.type-style('heading-03');
	}

	.description {
		@include type.type-style('body-01');
	}
</style>
