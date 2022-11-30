//------------------------------------------------------------------------------------------------------------------
//                          REGISTRATION FORM VALIDATIONS
//------------------------------------------------------------------------------------------------------------------

  
  //FIRSTNAME VALIDATION
  function check_firstName() {
    var fname = /^[a-zA-Z]\s/;
    const first_name = document.getElementById("first_name").value.trim();
    //alert("Hii")
    if (first_name === "") {
      document.getElementById("Fname").innerHTML =
        "FirstName must not be Blank";
      document.getElementById("first_name").focus();
    } else {
      if (fname.test(first_name)) {
        //alert("h1")
        if (first_name.length < 3 || first_name.length > 10) {
          document.getElementById("Fname").innerHTML =
            "First Name must be minimum 4 characters and maximum 20 characters";
          document.getElementById("first_name").focus();
        } else {
          document.getElementById("Fname").innerHTML = "";
        }
      }
    }
  }
  
  //LASTNAME VALIDATION
  function check_lastName() {
    var lname = /^[a-zA-Z]\s/;
    const last_name = document.getElementById("last_name").value.trim();
    //alert("Hii")
    if (last_name === "") {
      document.getElementById("Lname").innerHTML =
        "LastName must not be Blank";
      document.getElementById("last_name").focus();
    } else {
      if (lname.test(last_name)) {
        //alert("h1")
        if (last_name.length < 3 || last_name.length > 20) {
          document.getElementById("Lname").innerHTML =
            "LastName must be minimum 3 characters and maximum 20 characters";
          document.getElementById("last_name").focus();
        } else {
          document.getElementById("Lname").innerHTML = "";
        }
      }
    }
  }

  
  //EMAIL VALIDATION
  function check_Email() {
    const email = document.getElementById("Email").value.trim();
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    if (email === "") {
      document.getElementById("Mail").innerHTML = "Email must not be Blank";
      document.getElementById("Email").focus();
    } else {
      if (email.match(mailformat)) {
        document.getElementById("Mail").innerHTML = "";
      } else {
        document.getElementById("Mail").innerHTML = "Email must be Valid";
        document.getElementById("Email").focus();
      }
    }
  }
  // PHONE NUMBER VALIDATION
  function check_phno() {
    var phone_number = document.getElementById("Phno").value.trim();
    if (phone_number === "") {
      document.getElementById("phone").innerHTML =
        "Phone Number cannot be Blank..";
      document.getElementById("Phno").focus();
    } else if (isNaN(phone_number)) {
      document.getElementById("phone").innerHTML = "Not a valid data";
      document.getElementById("Phno").focus();
    } else if (phone_number.length < 10) {
      document.getElementById("phone").innerHTML = "Phone Number must be10 Digits";
      document.getElementById("Phno").focus();
    } else {
      document.getElementById("phone").innerHTML = "";
    }
  }

  //ZIPCODE
  function zipcode_check() {
    var zip = document.getElementById("Zip").value.trim();
    if (zip.length > 6) {
      document.getElementById("Zipcode").innerHTML = "Minimum 6 Digits";
      document.getElementById("Zip").focus();
    } else if (zip.match(/^[0-9]$/)) {
      document.getElementById("Zipcode").innerHTML = "Contains Only Digits";
      document.getElementById("Zip").focus();
    }
  }

  
  
  
  
  
  // //^(?=.{8,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$
  //  └─────┬────┘└───┬──┘└─────┬─────┘└─────┬─────┘ └───┬───┘
  //  │         │         │            │           no _ or . at the end
  //  │         │         │            │
  //  │         │         │            allowed characters
  //  │         │         │
  //  │         │         no __ or _. or ._ or .. inside
  //  │         │
  //  │         no _ or . at the beginning
  //  │
  //  username is 8-20 characters long