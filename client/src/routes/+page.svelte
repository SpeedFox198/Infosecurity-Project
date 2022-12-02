<svelte:head>
  <title>{"Bubbles"}</title>
</svelte:head>

<script>
var myInput = document.getElementById("psw");
var letter = document.getElementById("letter");
var capital = document.getElementById("capital");
var number = document.getElementById("number");
var length = document.getElementById("length");
const passwordRegex = `(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}`

// When the user clicks on the password field, show the message box
myInput.onfocus = function() {
  document.getElementById("message").style.display = "block";
}

// When the user clicks outside of the password field, hide the message box
myInput.onblur = function() {
  document.getElementById("message").style.display = "none";
}

// When the user starts to type something inside the password field
myInput.onkeyup = function() {
  // Validate lowercase letters
  var lowerCaseLetters = /[a-z]/g;
  if(myInput.value.match(lowerCaseLetters)) {  
    letter.classList.remove("invalid");
    letter.classList.add("valid");
  } else {
    letter.classList.remove("valid");
    letter.classList.add("invalid");
  }
  
  // Validate capital letters
  var upperCaseLetters = /[A-Z]/g;
  if(myInput.value.match(upperCaseLetters)) {  
    capital.classList.remove("invalid");
    capital.classList.add("valid");
  } else {
    capital.classList.remove("valid");
    capital.classList.add("invalid");
  }

  // Validate numbers
  var numbers = /[0-9]/g;
  if(myInput.value.match(numbers)) {  
    number.classList.remove("invalid");
    number.classList.add("valid");
  } else {
    number.classList.remove("valid");
    number.classList.add("invalid");
  }
  
  // Validate length
  if(myInput.value.length >= 8) {
    length.classList.remove("invalid");
    length.classList.add("valid");
  } else {
    length.classList.remove("valid");
    length.classList.add("invalid");
  }
}
</script>

<style>
.background{
  background-color: var(--grey);
}

.logo-with-text{
  padding: 8rem
}

.login{
  background-color: var(--white);
  margin: 8rem
}

.login-btn{
  background-color: var(--primary-dark)
}

.forgot-pw{
  color: var(--primary-light)
}

</style>
<main class="background h-100">
  <div class="container-fluid">
    <div class="row">
      <!-- Bubbles Logo -->
      <div class="bubbles-name col-md-6">
        <img class="logo-with-text" src="/with-text.svg" alt="Bubbles">
      </div>

      <!-- Login -->
      <div class="login col-md-4 card rounded-4 shadow">
        <div class=" p-5 pb-4 border-bottom-0">
          <h1 class="card-title fw-bold mb-0 fs-2">Log in and start chatting!</h1>
        </div>

        <div class="card-body p-5 pt-0">
          <form class="">
            <div class="form-floating mb-3">
              <input type="text" class="form-control rounded-3" id="floatingInput" placeholder="name@example.com" required>
              <label for="floatingInput">Email address or username</label>
            </div>
            <div class="form-floating mb-3">
              <input type="password" class="form-control rounded-3" id="floatingPassword" placeholder="Password" required>
              <label for="floatingPassword">Password</label>
            </div>
            <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">Log in</button>
            <a class="forgot-pw card-link text-center" href="/">Forgotten password?</a>
            
            <hr class="my-4">
            <h2 class="fs-5 fw-bold mb-3">Don't have an account yet?</h2>
            <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3" type="submit">
              Create new account
            </button>
            
          </form>
        </div>
      </div>

      <!-- Sign up -->
      <div class="login col-md-4 card rounded-4 shadow">
        <div class=" p-5 pb-4 border-bottom-0">
          <h1 class="card-title fw-bold mb-0 fs-2">Sign up and start chatting!</h1>
        </div>

        <div class="card-body p-5 pt-0">
          <form class="">
            <!-- email address -->
            <div class="form-floating mb-3">
              <input type="email" class="form-control rounded-3" id="floatingInput" placeholder="name@example.com" required>
              <label for="floatingInput">Email address</label>
            </div>

            <!-- username -->
            <div class="form-floating mb-3">
              <input type="email" class="form-control rounded-3" id="floatingInput" placeholder="username" required>
              <label for="floatingInput">Username</label>
            </div>

            <!-- password -->
            <div class="form-floating mb-3">
              <input type="password" class="form-control rounded-3" id="psw" name="psw" pattern="{passwordRegex}" title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters" placeholder="Password" required>
              <label for="floatingPassword">Password</label>
            </div>
            <!-- confirm password -->
            <div class="form-floating mb-3">
              <input type="password" class="form-control rounded-3" id="floatingPassword" placeholder="Password" required>
              <label for="floatingPassword">Confirm password</label>
            </div>

            <!-- password reuirements -->
            <div id="message">
              <h3>Password must contain the following:</h3>
              <p id="letter" class="invalid">A <b>lowercase</b> letter</p>
              <p id="capital" class="invalid">A <b>capital (uppercase)</b> letter</p>
              <p id="number" class="invalid">A <b>number</b></p>
              <p id="length" class="invalid">Minimum <b>8 characters</b></p>
            </div>


            <button class="login-btn w-100 mb-2 btn btn-lg rounded-3 btn-primary" type="submit">Sign up</button>
            <small class="text-muted">By clicking Sign up, you agree to the terms of use.</small>
            
            <hr class="my-4">
            <h2 class="fs-5 fw-bold mb-3">Already have an account?</h2>
            <button class="w-100 py-2 mb-2 btn btn-outline-dark rounded-3" type="submit">
              Log in here
            </button>
            
          </form>
        </div>
      </div>
    </div>
  </div>
</main>