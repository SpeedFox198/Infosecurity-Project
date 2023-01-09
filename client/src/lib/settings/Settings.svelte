<script>
import SlidingMenu from "$lib/settings/templates/SlidingMenu.svelte";
import Option from "$lib/settings/templates/Option.svelte";
import DevicesMenu from "$lib/devices/DevicesMenu.svelte";
import { invalidate } from "$app/navigation";

export let displaySettings;
export let toggleSettings;

let displayGeneral = false;
let displaySecurity = false;
let displaySusFiles = false;  // Scan suspicious files menu 
let displayMagic = false;     // Disappearing messages menu, *MAGIC! POOF!* (๑°༥°๑)
let displayData = false;
let displayDevices = false;

const toggleGeneral = async () => displayGeneral = !displayGeneral;
const toggleSecurity = async () => displaySecurity = !displaySecurity;
const toggleSusFiles = async () => displaySusFiles = !displaySusFiles;
const toggleMagic = async () => displayMagic = !displayMagic;
const toggleData = async () => displayData = !displayData;

async function toggleDevices () {
  displayDevices = !displayDevices;
  invalidate("app:devices");
}
</script>


<SlidingMenu title="Settings" display={displaySettings} on:click={toggleSettings} right={false}>
  <div class="">
    Profile things here...
  </div>
  <div class="d-flex flex-column">
    <Option name="General Settings" icon="gear" on:click={toggleGeneral}/>
    <Option name="Privacy and Security" icon="lock" on:click={toggleSecurity}/>
    <Option name="Devices" icon="desktop" on:click={toggleDevices}/>
  </div>
</SlidingMenu>


<SlidingMenu title="General Settings" display={displayGeneral} on:click={toggleGeneral} right={true}>
  <!-- Button trigger modal -->
  <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#Authenticator">
    Enable 2-Factor Authentication
  </button>
  <!-- Modal -->
  <div class="modal fade" id="Authenticator" tabindex="-1" aria-labelledby="AuthenticatorLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content modalIndex">
        <div class="modal-header">
          <h5 class="modal-title" id="AuthenticatorLabel">2-Factor Authentication</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div class="d-flex justify-content-center align-items-center h-100">
            <div class="card">
              <div class="card-header">
                Please follow the instructions to enable 2-Factor Authentication.
              </div>
              <div class="card-body">
                <form class="needs-validation" method="POST" action="" novalidate>
                  <input type="hidden" name="csrf_token" value=""/>
                  <input type="submit" value="SUBMIT" class="input-group btn"/>
                </form>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>
</SlidingMenu>


<SlidingMenu title="Privacy and Security" display={displaySecurity} on:click={toggleSecurity} right={true}>
  <Option name="Scan incoming files" icon="file-shield" on:click={toggleSusFiles}/>
  <Option name="Disappearing messages" icon="stopwatch" on:click={toggleMagic}/>
  <Option name="Request personal data" icon="file-zipper" on:click={toggleData}/>
</SlidingMenu>
<SlidingMenu title="Scan incoming files" display={displaySusFiles} on:click={toggleSusFiles} right={true}>
</SlidingMenu>
<SlidingMenu title="Disappearing messages" display={displayMagic} on:click={toggleMagic} right={true}>
</SlidingMenu>
<SlidingMenu title="Request personal data" display={displayData} on:click={toggleData} right={true}>
</SlidingMenu>


<SlidingMenu title="Devices" display={displayDevices} on:click={toggleDevices} right={true}>
  <DevicesMenu />
</SlidingMenu>

<style>
  .modalIndex {
    z-index: 9999;
  }
</style>