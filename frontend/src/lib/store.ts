import { writable } from 'svelte/store';
const currentPage = writable('');
export { currentPage };
