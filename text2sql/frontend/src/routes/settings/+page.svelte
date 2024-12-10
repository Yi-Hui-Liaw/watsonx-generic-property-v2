<script lang="ts">
	import {
		Button,
		Column,
		DataTable,
		Grid,
		Loading,
		Row,
		FileUploaderDropContainer,
		FileUploaderItem
	} from 'carbon-components-svelte';
	import { ArrowRight } from 'carbon-icons-svelte';
	import Restart from 'carbon-icons-svelte/lib/Restart.svelte';
	import { onMount } from 'svelte';

	let fileName: string;
	let uploadStatus = '';
	let visibility = 'invisible';
	let sampleData: any[] = [];

	let data: any[];
	$: data = [];

	onMount(async () => {
		const response = await fetch('/api/database');
		data = await response.json();
		console.log(data);
	});

	const onClick = async () => {
		visibility = 'visible';
		await new Promise((f) => setTimeout(f, 3000));
		visibility = 'invisible';
	};

	const onUpload = async (e: CustomEvent) => {
		try {
			uploadStatus = 'uploading';
			fileName = e.detail[0].name;
			const formData = new FormData();
			// formData.append('uid', uuidv4());
			formData.append('file', e.detail[0]);
			const response = await fetch('/api/upload', {
				method: 'POST',
				body: formData
			});
			if (!response.ok) {
				throw new Error(`${response.status} ${response.statusText}`);
			}
			await new Promise((f) => setTimeout(f, 1000));
			uploadStatus = 'uploaded';

			const data = (await response.json()).data;

			console.log(data);
		} catch (error) {
			uploadStatus = 'error';
			console.log(error);
		}
	};
</script>

<Grid fullWidth class="h-full" style="padding-bottom: 20px">
	<Row class="h-full">
		<Column class="h-full">
			<Grid class="h-full flex flex-col">
				<Row>
					<Column>
						<h3 class="my-6">Upload</h3>
					</Column>
				</Row>
				<Row class="my-4">
					<Column class="flex items-center justify-between">
						{#if uploadStatus === 'uploaded'}
							<FileUploaderItem name={fileName} status="complete" />
							
							<Loading withOverlay={false} small class="ml-4 {visibility}" />
							
						{:else if uploadStatus === 'uploading'}
							<FileUploaderItem name={fileName} status="uploading" class="mr-8" />
						{:else if uploadStatus === 'error'}
							<FileUploaderItem
								invalid
								name={fileName}
								errorSubject="Unable to process file."
								errorBody="Please select a new file."
								status="edit"
								on:delete={() => {
									uploadStatus = '';
								}}
								class="mr-8"
							/>
						{:else}
							<div class="w-full mr-8">
								<div class="mb-4">
									<p class="mb-4">This is a simplified demo to update a simulated database in the backend. After uploading the Excel file, the backend will be updated so that new questions will be queried against the updated backend.</p>
									<p>The uploaded file should be in Excel (.xlsx) with the following columns.</p>
								</div>
								<DataTable
									headers={[
										{ key: 'Property_Name', value: 'Property Name' },
										{ key: 'Layout', value: 'Layout' },
										{ key: 'Status', value: 'Status' },
										{ key: 'Block', value: 'Block' },
										{ key: 'Price', value: 'Price' }
									]}
									rows={[
										{
											Property_Name: 'A-09-01',
											Layout: 'TYPE A',
											Status: 'Signed',
											Block: 'BLOCK A',
											Price: 343888,
											id: 0
										},
										{
											Property_Name: 'A-09-02',
											Layout: 'TYPE C',
											Status: 'Signed',
											Block: 'BLOCK A',
											Price: 335888,
											id: 1
										},
										{
											Property_Name: 'A-09-03',
											Layout: 'TYPE D',
											Status: 'Signed',
											Block: 'BLOCK A',
											Price: 338888,
											id: 2
										},
										{
											Property_Name: 'A-09-03A',
											Layout: 'TYPE D',
											Status: 'Signed',
											Block: 'BLOCK A',
											Price: 338888,
											id: 3
										},
										{
											Property_Name: 'A-09-05',
											Layout: 'TYPE A1',
											Status: 'Signed',
											Block: 'BLOCK A',
											Price: 335888,
											id: 4
										}
									]}
								/>
							</div>
						{/if}
					</Column>
				</Row>
				<Row class="flex-auto">
					<Column>
						<div class="pr-8">
							<FileUploaderDropContainer
								labelText="Drag and drop files here or click to upload"
								on:change={onUpload}
								validateFiles={(files) => files.filter((x) => x.size < 1_048_576)}
							/>
							{#if sampleData.length > 0}
								<DataTable
									headers={[
										{ key: 'question', value: 'Question', width: '33.3%' },
										{ key: 'answer', value: 'Answer', width: '33.3%' },
										{ key: 'generated', value: 'Generated' }
									]}
									rows={sampleData}
								>
									<div slot="description" class="text-sm">
										Displaying top 5 row from uploaded data
									</div>
								</DataTable>
							{/if}
						</div>
					</Column>
				</Row>
			</Grid>
		</Column>
		<Column class="h-full">
			<Grid class="h-full flex flex-col">
				<Row>
					<Column>
						<h3 class="my-6">Database</h3>
					</Column>
				</Row>
				<Row class="flex-auto">
					<Column>
						{#each data as table}
							<DataTable
								class="mb-4"
								title={table.name}
								headers={[
									{ key: 'Property_Name', value: 'Property Name' },
									{ key: 'Layout', value: 'Layout' },
									{ key: 'Status', value: 'Status' },
									{ key: 'Block', value: 'Block' },
									{ key: 'Price', value: 'Price' }
								]}
								rows={table.data}
							/>
						{/each}
					</Column>
				</Row>
			</Grid>
		</Column>
	</Row>
</Grid>

<style lang="scss">
	@use '@carbon/styles/scss/type';

	.intro {
		@include type.type-style('body-02');
	}

	.result-heading {
		@include type.type-style('heading-02');
	}

	.result-score {
		@include type.type-style('heading-06');
	}

	.result-description {
		@include type.type-style('body-compact-02');
	}

	:global(.bx--data-table-container) {
		padding: 0;
	}

	:global(.bx--data-table td) {
		padding: 1rem;
	}

	:global(.bx--data-table-header) {
		padding-top: 0.5rem;
		padding-bottom: 0.5rem;
	}

	:global(.bx--btn--sm) {
		height: 2.5rem;
	}

	:global(.bx--file__selected-file) {
		min-height: 2.5rem;
		margin-bottom: 0;
	}

	:global(.bx--file__selected-file, .bx--file-browse-btn) {
		max-width: 100%;
		width: 100%;
	}
</style>
