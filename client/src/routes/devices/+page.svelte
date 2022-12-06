<script>
	import { page } from '$app/stores';
	import Device from '$lib/devices/Device.svelte';
	export let data;

	let currentUser = $page.data.user;
	let errors = data.errors;
	let devices = data.devices;
</script>

<main class="h-100">
  <div class="m-3 container-fluid">
    <h2>Devices</h2>
    <p>Hello {currentUser.username}!</p>
    <p>
    	Here are all the devices that are currently logged in with your Bubbles account. You can log out
    	of each one individually or all other devices.
    </p>
    <p>
    	If you see an entry you do not recognize, log out of that device and change your Bubbles account
    	password immediately.
    </p>

    {#if errors}
      <p class="text-danger">{errors}</p>
    {/if}
    {#each devices as device}
      <Device {device} current_device_id={currentUser.device_id} />
    {/each}
  </div> 
</main>