<script>
import { onMount } from "svelte";
let nav;
let burger;
let navLinks;
function navSlide() {
  //Animate Links
  let links = Array.from(navLinks.children);
  console.log(links);
  links.forEach((link, index) => {
    if (link.style.animation) {
        link.style.animation = ""
    } else {
        link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.5}s`;
    }
  });
  //Burger Animation
  burger.classList.toggle("toggle");
}

onMount(async () => {
  burger.classList.toggle("toggle");
})
</script>

<div class="intro">
  <nav style="top:0;" class="navbar" bind:this={nav}>
    <ul class="nav-links" bind:this={navLinks}>
      <li><a href="index.html" class='active-page'>Profile</a></li>
      <li><a href="aboutme.html">Privacy Settings</a></li>
      <li><a href="guide.html">Devices</a></li>
      <li><a href="feedback.html">Appearance</a></li>
    </ul>
    <div class="burger toggle" bind:this={burger} on:click={navSlide}>
      <div class="line1"></div>
      <div class="line2"></div>
      <div class="line3"></div>
    </div>
  </nav>
</div>

<!--Navbar-->
<style>
nav {
   position: fixed !important; /* to make the navigation bar sticky */
   top: 0%;
   width: 100%;
   display: flex;
   align-items: center;
   min-height: 8vh;
   color:black;
}

.intro{
 height: auto;
 z-index:3;
 width: 100%;
 height: 50px;
 color: white;
 position: relative;
 z-index: 3;
}

.nav-links {
   display: flex;
   justify-content: space-around;
   width: 30%;
}

.nav-links li {
       opacity: 0;
   }

.burger {
    display: block; /* shows the dropdown icon*/
    cursor: pointer;
    align-items: left;
}

body {
       overflow-x: hidden;
   }

.nav-links {
      position: fixed;
      right: 0px;
      height: 100%;
      top: 0;
      z-index:-1;
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 30%;
      transform: translateX(100%);
      transition: transform 0.25s ease-in;
  }

.nav-links li {
   list-style: none;
}

.nav-links a {
   color: black;
   text-decoration: none;
   letter-spacing: 4px;
   font-weight: bold;
   font-size: 14px;
   text-align: right;
   word-spacing: 20px;
   z-index: 3;
   opacity:1;
}

.burger div {
   width: 25px;
   height: 3px;
   background-color: black;
   margin: 5px;
   transition: all 0.3s ease;
}

.navbar ul li a.active-page{ /* to mark out the current page the user is in */
  color:white;
  background-color:black;
  padding:10px;
  border-radius: 30px;
}

@keyframes navLinkFade {
   from {
       opacity: 0;
       transform: translateX(50px);
   }
   to {
       opacity: 1;
       transform: translateX(0);
   }
}

.toggle .line1 { /* the tranformation of the dropdown bar to become a cross (X) */
   transform: rotate(-45deg) translate(-5px, 6px);
}

.toggle .line2 { /* the tranformation of the dropdown bar to become a cross (X) */
   opacity: 0;
}

.toggle .line3 { /* the tranformation of the dropdown bar to become a cross (X) */
   transform: rotate(45deg) translate(-5px, -6px);
}
</style>


