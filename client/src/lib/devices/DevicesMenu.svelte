<script>
	import { page } from '$app/stores';
	import Device from '$lib/devices/Device.svelte';
  import { deviceStore } from "$lib/stores/device"

	let currentUser = $page.data.user;
	$: ({ devices, errors } = $deviceStore);
  
  $: currentDevice = devices.find(device => device.id === currentUser.device_id)
  $: otherDevices = devices.filter(device => device.id !== currentUser.device_id)
</script>

<div class="p-3">
  <p>
  	Here are all the devices that are currently logged in with your Bubbles account. You can log out
  	of each one individually or all other devices.
  </p>
  <p>
  	If you see an entry you do not recognize, log out of that device and change your Bubbles account
  	password immediately.
  </p>
</div>

{#if errors}
	<p class="text-danger">{errors}</p>
{/if}

<div class="mb-4">
  <span class="fw-bold fs-4 mx-3">Current device</span>
  <Device device={currentDevice} current={true} />
</div>

<span class="fw-bold fs-4 mx-3">Other devices</span>
{#each otherDevices as device}
  <Device device={device} />
{/each}
