<script>
	export let device;
	export let currentDeviceId;

	let time = new Date(device.time * 1000).toLocaleString('en-SG'); // JS uses milliseconds instead of seconds
	let removeError;

	const removeDevice = async () => {
		const response = await fetch(`https://localhost:8443/api/devices/${device.id}`, {
			method: 'DELETE',
			credentials: 'include'
		});
		const result = await response.json();

		if (!response.ok) {
			removeError = result.message;
		}
    
    location.reload()
	};
</script>

<div class="border-bottom border-dark device-box box-width p-3 ">
	<div class="flex-row d-flex">
		<div class="flex-column d-flex flex-grow-1">
			{#if currentDeviceId === device.id}
				<span class="fw-bold fs-4 pb-2">Current device</span>
			{/if}
			<div class="py-2">
				<span>
					Last logged in at {time}
				</span>
			</div>
			<div class="py-2">
				<span>
					{device.browser}, {device.os}
				</span>
			</div>
			<div class="py-2">
				<span>Location: {device.location}</span>
			</div>
		</div>
		{#if !(currentDeviceId === device.id)}
			<div class="d-flex justify-content-center">
				<button class="btn" title="Log out device" on:click={removeDevice}>
					<i class="fa-solid fa-xmark fs-1" />
				</button>
			</div>
		{/if}
	</div>
	<div class="flex-row d-flex">
		{#if (removeError)}
			<span class="text-danger">{removeError}</span>	
		{/if}
	</div>
</div>

<style>
	.device-box {
		background-color: var(--grey);
	}

	.box-width {
		max-width: 50vh;
	}
</style>
