<script>
import Nav from "./Nav.svelte";
</script>


<!-- Left Section -->
<div class="d-flex flex-column flex-shrink-0 left-section">
  
  <!-- Profile & Settings Section -->
  <div class="d-flex top-left">
    <Nav/>
  </div>

  <!-- Chat List Section -->
  <div class="d-flex bottom-left">

  </div>
</div>


<style>
.left-section {
  width: var(--left-bar-length);
  background-color: var(--primary-light);
}

.top-left {
  /* position: absolute;
  top: 0; */
  height: 4rem;
  width: var(--left-bar-length);
  background-color: var(--primary);
}

.bottom-left {
  height: 100%;
}
</style>
