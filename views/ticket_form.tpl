<html>
 <head>
   <title>New Employee - Company Name</title>
   <link rel="stylesheet" href="/inc/form_styles.css">
 </head>
<body>
  <div class="background-image"></div>
  <div class="wrapper">
      <div id="one"><img src="/inc/company-logo.png" alt="Company Logo" style="max-width:45%;"></div>
      <div id="two">New Employee Arrival<br />IT Setup Request</div>
  </div>
  <div id="ticket_form">
  % if feedback:
      <div class="feedback">{{feedback}}</div>
  % end

  <div class="overlay">
    Add a blip here to explain what this form is.
    <div class="notice">
      <ul>
        <li> More info
        <li> Some more info
      </ul>
    </div>
  <form action="create_ticket" method="post" onsubmit="
    if(form_being_submitted) {
      alert('The tickets are being created, please wait a moment...');
      newEmployeeForm.disabled = true;
      return false;
    }
    if(checkForm(this)) {
      newEmployeeForm.value = 'Creating tickets, please standby...';
      form_being_submitted = true;
      return true;
    }
    return false;
">
  <ul>

    <li><input type="text" placeholder="Starting date of new employee (mm/dd/yy):"
      name="date_starting" class="field" required>
    </li>

    <li><input type="text" placeholder="Arriving employee name:"
      name="employee_name" class="field" required>
    </li>

    <li>If replacing a previous employee, does the new hire need access to that person's voicemail?<br />
      <input type="radio" name="voicemail"  value="No" checked /> No
      <input type="radio" name="voicemail"  value="Yes" /> Yes
    <li>

      <li>Is the new hire Staff or Other?<br />
        <input type="radio" name="position_type"  value="Staff" checked /> Staff
        <input type="radio" name="position_type"  value="Other" /> Other<br />
      <li>

    <li>New phone number or same phone number as a previous employee?<br />
      <input type="radio" name="phoneext"  value="Reuse predecessors extension" checked /> Same Phone #
      <input type="radio" name="phoneext"  value="New" /> New Phone #
    <li>

    <li>
      <input type="text" placeholder="Phone Extension of Previous Employee (if any):" name="prevext" class="field">
    </li>

    <li>Access to predecessor's email?<br />
      <input type="radio" name="predecessoremail"  value="No" checked /> No
      <input type="radio" name="predecessoremail"  value="Yes" /> Yes
    <li>

    <li>Forward predecessor's email aliases (if any)?<br />
      <input type="radio" name="fwdaliases"  value="No" checked /> No
      <input type="radio" name="fwdaliases"  value="Yes" /> Yes
    <li>

      <li>Can the new hire's email address be auto-published in the directory?<br />
        <input type="radio" name="publish_email"  value="No" /> No
        <input type="radio" name="publish_email"  value="Yes" checked/> Yes
      <li>

    <li>Will the new hire need to administrate calendars?<br />
      <input type="radio" name="admin_calendars"  value="No" checked /> No
      <input type="radio" name="admin_calendars"  value="Yes" /> Yes<br />
      <div class="info">Please list which in the bottom comment box, if any.</div>
    <li>

    <li>Is there an existing computer for this position, or is a new one necessary?<br />
      <input type="radio" name="existing_machine"  value="Yes, a machine exists" checked /> Yes, a machine already exists
      <input type="radio" name="existing_machine"  value="New machine needed" /> New machine needed
    <li>

    <li>Desired operating system?<br />
      <input type="radio" name="os"  value="Mac" checked /> Mac
      <input type="radio" name="os"  value="Windows" /> Windows
      <input type="radio" name="os"  value="Linux" /> Linux
    <li>

    <li>Transfer files from predecessor's machine?<br />
      <input type="radio" name="transfer_files"  value="Yes" checked /> Yes
      <input type="radio" name="transfer_files"  value="No" /> No
    <li>

    <li>Which of the following network resources will the new hire need access to?<br />
      	&nbsp; &nbsp; <input type="checkbox" value="Folder" name="folder">Department folder shares<br />
      	&nbsp; &nbsp; <input type="checkbox" value="specialapp1" name="specialapp1">Special app 1<br />
        &nbsp; &nbsp; <input type="checkbox" value="specialapp2" name="specialapp2">Special app 2<br />
    </li>

    <li>Has HR &amp; the supervisor approved VPN access for this user?<br />
      <input type="radio" name="vpn"  value="No" checked /> No
      <input type="radio" name="vpn"  value="Yes" /> Yes<br />
    <li>

    <li>
      <input type="text" placeholder="Schedule Technology Training with New Hire (mm/dd/yy hh am/pm):" name="tech_training" class="field" required>
    </li>

    <li>
      <input type="text" placeholder="Office Location / Room Number:" name="room" class="field" required>
    </li>

    <li>
      <textarea placeholder="Any additional info you'd like to supply?" name="description" rows="6" class="field"></textarea>
    </li>

    % if no_email:
    <li><input type="email" placeholder="Supervisor's email address:" name="email" class="field" required>
      <div class="info">This field is only requested when you don't have active support desk sessions.  After this submission we'll remember you (for this session).</div>
      </li>
    % end

    <li>
      <div id="submit_button">
        <input type="submit" name="newEmployeeForm" value="Submit">
      </div>
    </li>

    % if feedback:
    <li>
      <div class="feedback">{{feedback}}
      </div>
    </li>
    % end
  </ul>
  </form>
  </div>
  </div>
  <script type="text/javascript">
    var form_being_submitted = false;

    function checkForm(form) {
      if(form.date_starting.value == "") {
        alert("Please enter the start date of the new employee");
        form.date_starting.focus();
        return false;
      }
      if(form.employee_name.value == "") {
        alert("Please enter the employee name");
        form.employee_name.focus();
        return false;
      }
      if(form.tech_training.value == "") {
        alert("Please pick a date for tech training");
        form.tech_training.focus();
        return false;
      }
      if(form.room.value == "") {
        alert("Please specify their office number");
        form.room.focus();
        return false;
      }
      if(form.email.value == "") {
        alert("Please specify the supervisor email");
        form.email.focus();
        return false;
      }
      return true;
    }

    function resetForm(form)
    {
      form.newEmployeeForm.disabled = false;
      form.newEmployeeForm.value = "Submit";
      form_being_submitted = false;
    }

  </script>
</body>
</html>
