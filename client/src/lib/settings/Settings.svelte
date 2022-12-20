<script>
  import SlidingMenu from "$lib/settings/SlidingMenu.svelte";
  import Option from "$lib/settings/Option.svelte";
	import DevicesMenu from "../devices/DevicesMenu.svelte";
  import { invalidate } from "$app/navigation"

export let display;
export let toggleSettings;

let displayDevices = false;

function toggleDevices() {
  displayDevices = !displayDevices;
}
</script>

<SlidingMenu title="Settings" display={displaySettings} on:click={toggleSettings} right={false}>
  <div class="">
    Profile things here...
  </div>
  <div class="d-flex flex-column">
    <Option name="Devices" icon="desktop" on:click={toggleDevices}/>
    <Option name="Security" icon="gear" on:click={toggleSecurity}/>
    <Option name="Things" icon="gear" on:click={undefined}/>
  </div>
</SlidingMenu>


<SlidingMenu title="Devices" display={displayDevices} right={true} on:click={toggleDevices}>
  <DevicesMenu />
</SlidingMenu>


<SlidingMenu title="Security" display={displaySecurity} on:click={toggleSecurity} right={true}>
  Security Settings
</SlidingMenu>
