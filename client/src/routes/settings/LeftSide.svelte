<script>
    import LeftNav from "./LeftNav.svelte";
</script>

<!-- Left Section -->
<div class="d-flex flex-column flex-shrink-0 left-section">
  
    <!-- Profile & Settings Section -->
    <div class="d-flex top-left">
        <LeftNav/>
    </div>
  
    <!-- Chat List Section -->
    <div class="d-flex flex-column bottom-left">
        
    </div>
  </div>
  
  <footer>
  </footer>
  
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
    overflow-y: scroll;
  }
  </style>