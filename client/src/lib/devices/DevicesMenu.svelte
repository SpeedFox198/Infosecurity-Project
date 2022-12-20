<script>
	import { page } from '$app/stores';
	import Device from '$lib/devices/Device.svelte';
  import { deviceStore } from "$lib/stores/device"

	let currentUser = $page.data.user;
	$: ({ devices, errors } = $deviceStore);
</script>

<h2>Devices</h2>
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
	<Device {device} currentDeviceId={currentUser.device_id} />
{/each}
