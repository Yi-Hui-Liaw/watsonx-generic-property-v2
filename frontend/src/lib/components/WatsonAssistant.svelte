<script lang="ts">
	import { onMount } from 'svelte';
	import { currentPage } from '$lib/store';
	import Carousel from './Carousel.svelte';

	let webChatInstance: any;

	const preSendHandler = (event: any) => {
		if (event.data.context.skills['actions skill'].skill_variables) {
			event.data.context.skills['actions skill'].skill_variables.CurrentPage = $currentPage;
		}
	};

	const chatReadyHandler = () => {
		webChatInstance.updateHomeScreenConfig({
			is_on: true,
			starters: {
				is_on: true
			}
		});
	};

	const preRestartHandler = (event: any) => {
		webChatInstance.updateHomeScreenConfig({
			is_on: false
		});
	};

	const customResponseHandler = (event: any, instance: any) => {
		const { element } = event.data;
		console.log("event.data fetch:", element)
		const customResponse = event.data.message.user_defined;
		console.log("event.data.message.user_defined fetch", customResponse)
		// if (customResponse && customResponse.images)
		// 	element.innerHTML = `<img class="customer-response-image" src="/img/the-connaught-one/${customResponse.image}" alt="" />`;
		if (customResponse && customResponse.images) {
			element.innerHTML = '<div id="carousel"></div>';
			// console.log(element.querySelector('#carousel'));
			new Carousel({
				target: element.querySelector('#carousel')!,
				props: {
					images: customResponse.images.map((x: string) => /img/ + x)
				}
			});
		}
	};

	onMount(async () => {
		const onLoad = async (instance: any) => {
			webChatInstance = instance;
			instance.on({ type: 'pre:send', handler: preSendHandler });
			instance.on({ type: 'chat:ready', handler: chatReadyHandler });
			instance.on({ type: 'pre:restartConversation', handler: preRestartHandler });
			instance.on({ type: 'customResponse', handler: customResponseHandler });
			instance.updateHomeScreenConfig({
				is_on: false
			});
			await instance.render();
		};

		(window as any).watsonAssistantChatOptions = {
			integrationID: '701ee0c7-178c-4cd1-be97-b4985f9b21b1', // The ID of this integration.
			region: 'us-south', // The region your integration is hosted in.
			serviceInstanceID: '2b12c818-752c-4824-9327-6dd46a9c78b0', // The ID of your service instance.
			onLoad: onLoad,
			showRestartButton: true,
			openChatByDefault: false,
			showLauncher: true
		};
		setTimeout(function () {
			const t = document.createElement('script');
			t.src =
				'https://web-chat.global.assistant.watson.appdomain.cloud/versions/latest/WatsonAssistantChatEntry.js';
			document.head.appendChild(t);
		});
	});
</script>
