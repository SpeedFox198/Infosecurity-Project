<script>
	export let device;
	export let current = false;
  import { invalidate } from "$app/navigation"

  let timeDiff
  $: timeDiff = Date.now() - (device.time * 1000)
	let removeError;
  
  const convertMilliseconds = (ms) => {
    let seconds = ms / 1000;
    let timeUnits = [
      { label: "days", duration: 86400 },
      { label: "hours", duration: 3600 },
      { label: "minutes", duration: 60 },
      { label: "seconds", duration: 1 }
    ]
    
    let result = ""
    timeUnits.every(unit => {
      if (seconds >= unit.duration) {
        let value = Math.floor(seconds / unit.duration)
        result += `${value} ${unit.label}`
        return false
      }
      return true
    })
    
    return result.trim()
  }

	const removeDevice = async () => {
		const response = await fetch(`https://localhost:8443/api/devices/${device.id}`, {
			method: 'DELETE',
			credentials: 'include'
		});
		const result = await response.json();

		if (!response.ok) {
			removeError = result.message;
		}
    
    invalidate("app:devices")
	};
</script>

<div class="border-bottom border-dark device-box p-3 ">
	<div class="flex-row d-flex">
		<div class="flex-column d-flex flex-grow-1">
			<div class="py-2">
				<span>
					Last logged in {convertMilliseconds(timeDiff)} ago
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
		{#if !(current)}
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
</style>
