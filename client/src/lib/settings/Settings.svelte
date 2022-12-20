<script>
import SlidingMenu from "$lib/settings/SlidingMenu.svelte";
import Option from "$lib/settings/Option.svelte";

export let display;
export let toggleSettings;

let displayDevices = false;

function toggleDevices() {
  displayDevices = !displayDevices;
}
</script>

<SlidingMenu title="Settings" display={display} right={false} on:click={toggleSettings} zIndex=1>
  <div class="">
    Profile things here...
  </div>
  <div class="d-flex flex-column">
    <Option name="Devices" icon="desktop" on:click={toggleDevices}/>
    <Option name="Things" icon="gear" on:click={undefined}/>
    <Option name="Things" icon="gear" on:click={undefined}/>
  </div>
</SlidingMenu>


<SlidingMenu title="Devices" display={displayDevices} right={true} on:click={toggleDevices} zIndex=2>
  Devices SEttigngs
</SlidingMenu>
