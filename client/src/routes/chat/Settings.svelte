<script>
export let display;
export let toggleSettings;

let settingsSection;

</script>


<div class="sidenav" class:display bind:this={settingsSection}>
  <!-- svelte-ignore a11y-invalid-attribute -->
  <a href="javascript:void(0)" class="closebtn" on:click={toggleSettings}>&times;</a>
  <!-- svelte-ignore a11y-invalid-attribute -->
  <a href="#">About</a>
  <!-- svelte-ignore a11y-invalid-attribute -->
  <a href="#">Services</a>
  <!-- svelte-ignore a11y-invalid-attribute -->
  <a href="#">Clients</a>
  <!-- svelte-ignore a11y-invalid-attribute -->
  <a href="#">Contact</a>
</div>


<style>
.sidenav {
  height: 100%;
  width: 0;
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  background-color: #111;
  overflow-x: hidden;
  transition: 0.25s;
  padding-top: 60px;
  text-align:center;
}

.sidenav a {
  padding: 8px 8px 8px 32px;
  text-decoration: none;
  font-size: 25px;
  color: #818181;
  display: block;
  transition: 0.3s;

}

.sidenav a:hover{
  color: #f1f1f1;
}

.sidenav .closebtn {
  position: absolute;
  top: 0;
  right: 25px;
  font-size: 36px;
  margin-left: 50px;
}

.display {
  width: 100%;
}

@media screen and (max-height: 450px) {
  .sidenav {padding-top: 15px;}
  .sidenav a {font-size: 18px;}
}
</style>
