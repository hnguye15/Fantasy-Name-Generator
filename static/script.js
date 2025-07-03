//Modal Components
Vue.component("modal", {
	template: "#modal-template"
});
var app = new Vue({
	el: "#app",

	//Data
	data: {
		serviceURL: "",
		authenticated: false,
		userData: null,
		loggedIn: null,
		editModal: false,
		user: {
			username: "",
			password: "",
			email: ""
		},
		selectedName: {
			name: "",
			gender: "",
			background: ""
		}
	},
	
	//Lifecycle Hooks
	mounted: function() {
		var userSavedNames = [];
		var savedNameCount = 0;
		axios
			.get(this.serviceURL+"/login")
			.then(response => {
				if (response.data.status == "success") {
					this.authenticated = true;
					this.user.username = localStorage.getItem("savedUsername");
					this.loggedIn = response.data.status;
					userSavedNames = response.data.names;
					this.dispSavedNames();
				}
				document.getElementById("body").style.display="";
				document.getElementById("savedNamesList").style.display = "";
			})
		.catch(e => {
			this.authenticated = false;
			document.getElementById("body").style.display="";
			document.getElementById("savedNamesList").style.display = "";
			console.log(e);
		});
	},
	
	//Methods
	methods: {
		showPopup(id, closeNext, openNext) {
			if (closeNext != "") {
				document.getElementById(closeNext).close();
			}
			if (openNext != "") {
				document.getElementById(openNext).showModal();
			}
			if (id == "registerLayer") {
				this.user.username = "";
				this.user.password = "";
				document.getElementById("passwordConfirm").value = "";
				this.user.email = "";
			}
			if (id == "changePasswordLayer") {
				document.getElementById("oldPassword").value = "";
			}
			if (id == "feedbackLayer") {
				this.dispSavedFeedback();
			}
			document.getElementById(id).showModal();
		},
		
		closePopup(id, closeNext, openNext) {
			if (closeNext != "") {
				document.getElementById(closeNext).close();
			}
			if (openNext != "") {
				document.getElementById(openNext).showModal();
			}
			if (id == "loginLayer") {
				this.user.username = "";
				this.user.password = "";
			}
			if (id == "registerLayer") {
				this.user.username = "";
				this.user.password = "";
				this.user.email = "";
				document.getElementById("passwordConfirm").value = "";
			}
			if(id == "changePasswordLayer") {
				document.getElementById("oldPassword").value = "";
				document.getElementById("newPassword").value = "";
			}
			document.getElementById(id).close();
		},
		
		login() {
			var userSavedNames = [];
			var savedNameCount = 0;
			if (this.user.username != "" && this.user.password != "") {
				if (validateUsername(this.user.username) && validatePassword(this.user.password)) {
					axios
					.post(this.serviceURL+"/login", {
						"username": this.user.username,
						"password": this.user.password
					})
					.then(response => {
						if (response.data[0].status == "success") {
							document.getElementById("loginLayer").close();
							this.authenticated = true;
							localStorage.setItem("savedUsername", this.user.username);
							this.loggedIn = response.data[0].status;
							this.dispSavedNames();
						}
						else {
							alertUser("Incorrect username or password!");
							this.user.password = "";
						}
					})
					.catch(e => {
						alertUser("Incorrect username or password!");
						this.user.password = "";
						console.log(e);
					});		
				}
				
			} else {
				alertUser("Username and password are required!");
			}
		},

		register() {
			if (this.user.username != "" && this.user.password != "" && this.user.email != "" && document.getElementById("passwordConfirm").value != "") {
				if (validateUsername(this.user.username) && validatePassword(this.user.password) && validateEmail(this.user.email) && validatePassword(document.getElementById("passwordConfirm").value)) {
					if (document.getElementById("passwordRegister").value == document.getElementById("passwordConfirm").value) {
						axios
						.post(this.serviceURL+"/register", {
							"username": this.user.username,
							"password": this.user.password,
							"email": this.user.email
						})
						.then(response => {
							if (response.data[0].status == "success") {
								this.authenticated = true;
								localStorage.setItem("savedUsername", this.user.username);
								this.loggedIn = response.data[0].status;
								document.getElementById("registerLayer").close();
								document.getElementById("loginLayer").close();
								alertUser("Registration successful!");
							}
							else {
								alertUser("Something was wrong with registration!");
							}
						})
						.catch(e => {
							alertUser("Username already taken!");
							console.log(e);
						});						
					}
					else {alertUser("Password confirmation did not match!")}
				}
			}
			else {alertUser("All the fields are required!");}
			
		},

		logout() {
		axios
		.delete(this.serviceURL+"/logout")
		.then(response => {
			this.user.username = "";
			this.user.password = "";
			this.user.email = "";
			this.authenticated = false;
			document.getElementById("savedNamesList").style.display = "none";
			window.location.reload();
		})
		.catch(e => {
			console.log(e);
		});
		
		},
		
		generateNames() {
			var genderIn = document.getElementById("genderSelect").value;
			var backgroundIn = document.getElementById("backgroundSelect").value;
			var countIn = document.getElementById("totalSelect").value;
			var noMiddleName = document.getElementById("noMiddleName").checked;
			var firstNames = [];
			var middleNames = [];
			var lastNames = [];
			var fullName = "";
			var generatedNames = [];
			var ul = document.getElementById("generatedNamesList");
			ul.innerHTML = "";
			var nameCount = 0;
			
			if (genderIn == "" || backgroundIn == "" || countIn == "") {
				alertUser("Please select all the required fields!");
			}
			else {				
				const queryParam = {
					params: {
						"gender": genderIn,
						"background": backgroundIn,
						"count": parseInt(countIn)
					}
				};
				axios.all([
					axios.get(this.serviceURL+"/first-name", queryParam),
					axios.get(this.serviceURL+"/middle-name", queryParam),
					axios.get(this.serviceURL+"/last-name", queryParam)
				])
				.then(axios.spread((response1, response2, response3) => {
					firstNames = response1.data.names;
					middleNames = response2.data.names;
					lastNames = response3.data.names;
					if (backgroundIn == "Orc") {
						for (let i = 0; i < countIn; i++) {
							fullName = firstNames[i].FIRST_NAME;
							generatedNames.push(fullName);
						}
					}
					else {
						if (noMiddleName) {
							for (let i = 0; i < countIn; i++) {
								fullName = firstNames[i].FIRST_NAME + " " + lastNames[i].LAST_NAME;
								generatedNames.push(fullName);
							}
						}
						else {
							for (let i = 0; i < countIn; i++) {
								fullName = firstNames[i].FIRST_NAME + " " + middleNames[i].MIDDLE_NAME + " " + lastNames[i].LAST_NAME;
								generatedNames.push(fullName);
							}
						}
					}
					for (name of generatedNames) {
						var li = document.createElement("li");
						$("li").css("margin-bottom", "0.5em");
						//Automatically escape special characters with document.createTextNode()
						li.appendChild(document.createTextNode(name));
						li.setAttribute("id", "name#" + nameCount);
						li.set
						ul.appendChild(li);
						nameCount++;
					}
					$("#generatedNamesList li").on("click", function () {
						$("#generatedNamesList li").removeClass('selected');
						$(this).attr('class', 'selected');
						app.selectedName.name = $(this).text();
						app.selectedName.gender = genderIn;
						app.selectedName.background = backgroundIn;
					});
					$(document).click(function(event) {
						if (!$(event.target).is("#generatedNamesList li")) {
							$('#generatedNamesList li').removeClass("selected");
						}
					});
				}))	
				.catch(e => {
					console.log(e);
				});
			}		
		},
	
		saveName() {
			var userSavedNames = [];
			var savedNameCount = 0;
			var isFound = false;
			const queryParamSave = {
				"name": this.selectedName.name,
				"gender": this.selectedName.gender,
				"background": this.selectedName.background
			}

			if (this.selectedName.name == "" || this.selectedName.gender == "" || this.selectedName.background == "") {
				alertUser("Please select a generated name first!");
			}
			else {
				axios
				.get(this.serviceURL + "/user/" + this.user.username + "/saved-names", { 
					params: {
						"count": 0
					}
				})
				.then(response => {
					userSavedNames = response.data.names;
					for (name of userSavedNames) {
						if (this.selectedName.name == userSavedNames[savedNameCount].NAME) {
							isFound = true;
							break;
						}
						savedNameCount++;
					}
					savedNameCount = 0;
					if (isFound) {
						alertUser("Name already exists in your list!");
					}
					else {
						axios
						.post(this.serviceURL + "/user/" + this.user.username + "/saved-names", queryParamSave)
						.then(response => {
							var message = response.data.status;
							this.dispSavedNames();
						})
						.catch(e => {
							alertUser("There was a error saving the selected name!");
							console.log(e);
						});
					}
				})
				.catch(e => {
					alertUser("There was an error retrieving user data!");
					console.log(e);
				});
			}
			this.selectedName.name = "";
			this.selectedName.gender = "";
			this.selectedName.background = "";
		},
		
		deleteName(deleteAll) {
			var userSavedNames = [];
			var savedNameCount = 0;
			var isFound = false;
			
			if (deleteAll == "yes") {
				axios
					.delete(this.serviceURL + "/user/" + this.user.username + "/saved-names", { data: { name: "", confirmDeleteAll: deleteAll } })
					.then(response => {
						var message = response.data.status;
						this.dispSavedNames();
					})
					.catch(e => {
						alertUser("There was a error deleting all names!");
						console.log(e);
					});
			}
			else if (this.selectedName.name == "") {
				alertUser("Please select a name first!");
			}
			else {
				axios
				.get(this.serviceURL + "/user/" + this.user.username + "/saved-names", { 
					params: {
						"count": 0
					}
				})
				.then(response => {
					userSavedNames = response.data.names;
					for (name of userSavedNames) {
						if (this.selectedName.name == userSavedNames[savedNameCount].NAME) {
							isFound = true;
							break;
						}
						savedNameCount++;
					}
					savedNameCount = 0;
					
					if (isFound && deleteAll == "no") {
						axios
						.delete(this.serviceURL + "/user/" + this.user.username + "/saved-names", { data: { name: this.selectedName.name, confirmDeleteAll: deleteAll } })
						.then(response => {
							var message = response.data.status;
							this.dispSavedNames();
						})
						.catch(e => {
							alertUser("There was a error deleting the selected name!");
							console.log(e);
						});
					}
					else {
						alertUser("Cannot find the name to delete!");
					}
				})
				.catch(e => {
					alertUser("There was an error retrieving user data!");
					console.log(e);
				});
			}
		},
		
		dispSavedNames() {
			var userSavedNames = [];
			var savedNameCount = 0;
			axios
			.get(this.serviceURL + "/user/" + this.user.username + "/saved-names", { 
				params: {
					"count": 0
				}
			})
			.then(response => {
				userSavedNames = response.data.names;
				var savedUl = document.getElementById("savedNamesList");
				savedUl.innerHTML = "";
				for (name of userSavedNames) {
					var savedLi = document.createElement("li");
					$("li").css("margin-bottom", "0.5em");
					//Automatically escape special characters with document.createTextNode()
					savedLi.appendChild(document.createTextNode(userSavedNames[savedNameCount].NAME));
					savedLi.setAttribute("id", "savedName#" + savedNameCount);
					savedUl.appendChild(savedLi);
					savedNameCount++;
				}
				$("#savedNamesList li").on("click", function () {
					$("#savedNamesList li").removeClass('selected');
					$(this).attr('class', 'selected');
					app.selectedName.name = $(this).text();
				});
				$(document).click(function(event) {
					if (!$(event.target).is("#savedNamesList li")) {
						$('#savedNamesList li').removeClass("selected")
					}
				});
			})
			.catch(e => {
				alertUser("There was an error retrieving user data!");
				console.log(e);
			});
		},
		
		saveFeedback() {
			var userSavedNames = [];
			var isFound = false;
			var feedback = document.getElementById("feedbackField").value;
			const queryParamSave = {
				"feedback": feedback
			}

			if (feedback == "") {
				alertUser("Feedback cannot be blank!");
			}
			else {
				axios
					.post(this.serviceURL + "/user/" + this.user.username + "/feedback", queryParamSave)
					.then(response => {
						var message = response.data.status;
						document.getElementById("feedbackField").value = "";
						this.dispSavedFeedback();
					})
					.catch(e => {
						alertUser("There was a error saving feedback!");
						console.log(e);
					});
			}
		},
		
		dispSavedFeedback() {
			var userSavedFeedback = [];
			var savedFeedbackCount = 0;
			axios
			.get(this.serviceURL + "/user/" + this.user.username + "/feedback")
			.then(response => {
				userSavedFeedback = response.data.feedbacks;
				var savedUl = document.getElementById("savedFeedbackList");
				savedUl.innerHTML = "";
				for (feedback of userSavedFeedback) {
					var savedLi = document.createElement("li");
					$("li").css("margin-bottom", "0.5em");
					//Automatically escape special characters with document.createTextNode()
					savedLi.appendChild(document.createTextNode(userSavedFeedback[savedFeedbackCount].USER_ID + ": " + userSavedFeedback[savedFeedbackCount].FEEDBACK));
					savedLi.setAttribute("id", "savedFeedback#" + savedFeedbackCount);
					savedUl.appendChild(savedLi);
					savedFeedbackCount++;
				}
			})
			.catch(e => {
				alertUser("There was an error retrieving feedback!");
				console.log(e);
			});
		},
		
		changePassword() {
			var oldPassword = document.getElementById("oldPassword").value;
			var newPassword = document.getElementById("newPassword").value;
			
			if (document.getElementById("oldPassword").value != "" && document.getElementById("newPassword").value != "") {
				if (oldPassword != newPassword) {
					if (validatePassword(oldPassword) && validatePassword(newPassword)) {
						axios
						.post(this.serviceURL + "/user/" + this.user.username + "/password", {
							"username": this.user.username,
							"oldPassword": this.user.password,
							"newPassword": newPassword
						})
						
						.then(response => {
							if (response.data[0].status == "success") {
								document.getElementById("oldPassword").value = "";
								document.getElementById("newPassword").value = "";
								document.getElementById("changePasswordLayer").close();
								document.getElementById("menuLayer").showModal();
								alertUser("Password change successful!");
							}
							else {
								alertUser("Incorrect old password!");
							}
						})
						.catch(e => {
							alertUser("Something was wrong with password change!");
							console.log(e);
						});
					}
				}
				else {alertUser("Old password and new password cannot match!");}
			}
			else {alertUser("All the fields are required!");}
		},
	}
});

//Helper Functions
function alertUser(content) {
	document.getElementById("alertContent").innerText = content;
	document.getElementById("alert").showModal();
}

function validateUsername(username) {
	if (username.length > 50) {
		alertUser("Your username is too long!")
		return false;
	}
	else if (username.length < 8) {
		alertUser("Your username is too short!");
		return false;
	}
	const checks = [
        /[!-/]/,
		/[:-@]/,
		/[[-`]/,
		/[{-~]/,
		/[ ]/
    ];
	
	let score = checks.reduce((acc, rgx) => acc + rgx.test(username), 0);
	
	if (score > 0) {
		alertUser("Username must not contain any special characters!");
		return false;
	}
	
	return true;
}

function validatePassword(password) {
	if (password.length > 64) {
		alertUser("Your password is too long!")
		return false;
	}
	else if (password.length < 8) {
		alertUser("Your password is too short!");
		return false;
	}
	
	const checks = [
        /[a-z]/,     // Lowercase
        /[A-Z]/,     // Uppercase
        /\d/,        // Digit
        /[@.#$!%^&*.?]/ // Special character
    ];
	
	const otherCharCheck = [
		/(?![@.#$!%^&*.?])[!-/]/,
		/(?![@.#$!%^&*.?])[:-@]/,
		/(?![@.#$!%^&*.?])[[-`]/,
		/(?![@.#$!%^&*.?])[{-~]/,
		/[ ]/
	];
	
    let score = checks.reduce((acc, rgx) => acc + rgx.test(password), 0);
	
	let otherScore = otherCharCheck.reduce((acc, rgx) => acc + rgx.test(password), 0);
	
	if (score < 4) {
		alertUser("Your password is not strong enough!");
		return false;
	}
	
	if (otherScore > 0) {
		alertUser("Password must not contain insecure special characters!");
		return false;
	}
	
	return true;
}

function validateEmail(email) {
	const check = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
	if (!check.test(email)) {
		alertUser("Invalid email format!");
		return false;
	}
	else {return true;}
}

//SOURCES:
//Password validation: https://www.geeksforgeeks.org/javascript-program-to-validate-password-using-regular-expressions/
//Email validation: https://www.mailercheck.com/articles/email-validation-javascript
//Cheat sheet: https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html