const signInBtn = document.getElementById("login");
const signUpBtn = document.getElementById("signup");
const firstForm = document.getElementById("form1");
const secondForm = document.getElementById("form2");
const container = document.querySelector(".panel");

signInBtn.addEventListener("click", () => {
	container.classList.remove("right-active");
});

signUpBtn.addEventListener("click", () => {
	container.classList.add("right-active");
});

firstForm.addEventListener("submit", (e) => e.preventDefault());
secondForm.addEventListener("submit", (e) => e.preventDefault());