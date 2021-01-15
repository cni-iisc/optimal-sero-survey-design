// setting the heading and enabling input fields based on the design method
var method = document.getElementsByName("method");
var fixedP = document.getElementById("fixedP");
var dynamicP = document.getElementById("dynamicP");
var headText = document.getElementById("heading");
headText.innerText = "Enter parameters";
fixedP.style.display = 'block';
dynamicP.style.display = 'none';

for(var i = 0; i < method.length; i++) {
    method[i].onclick = function() {
      var val = this.value;
      if(val == 'local'){  
        headText.innerText = "Enter parameters";
        fixedP.style.display = 'block';   // show
        dynamicP.style.display = 'none';// hide
      }
      else if(val == 'grid'){
        headText.innerText = "Enter parameter ranges";
        fixedP.style.display = 'none';
        dynamicP.style.display = 'block';
      }    
   }
 }

// setting the input field as editable based on option selected
$('input:radio[name="option"]').change(function(){
    if($(this).val() == 'error'){
      $("label[for='margin']").text("Margin of error");
      $("label[for='budget']").text("Enter budget");

      $("#budget").prop('readonly', false);
      $("#margin").prop('readonly', true);
    }
    if($(this).val() == 'cost'){
      $("label[for='margin']").text("Enter margin of error");
      $("label[for='budget']").text("Budget");

      $("#budget").prop('readonly', true);
      $("#margin").prop('readonly', false);
    }
});
  

// Run on page load
window.onload = function() {

  // If values are not blank, restore them to the fields
  var cRAT = sessionStorage.getItem('cRAT');
  if (cRAT !== null) $('#cRAT').val(cRAT);
  var cRTPCR = sessionStorage.getItem('cRTPCR'); 
  if (cRTPCR !== null) $('#cRTPCR').val(cRTPCR);
  var cIGG = sessionStorage.getItem('cIGG');
  if (cIGG !== null) $('#cIGG').val(cIGG);
  var dEffect = sessionStorage.getItem('dEffect');
  if (dEffect !== null) $('#dEffect').val(dEffect);

  var p1 = sessionStorage.getItem('p1');
  if (p1 !== null) $('#p1').val(p1);
  var p2 = sessionStorage.getItem('p2');
  if (p2 !== null) $('#p2').val(p2);
  var p3 = sessionStorage.getItem('p3');
  if (p3 !== null) $('#p3').val(p3);
  var p1_start = sessionStorage.getItem('p1_start');
  if (p1_start !== null) $('#p1_start').val(p1_start);
  var p2_start = sessionStorage.getItem('p2_start');
  if (p2_start !== null) $('#p2_start').val(p2_start);
  var p3_start = sessionStorage.getItem('p3_start');
  if (p3_start !== null) $('#p3_start').val(p3_start);
  var p1_end = sessionStorage.getItem('p1_end');
  if (p1_end !== null) $('#p1_end').val(p1_end);
  var p2_end = sessionStorage.getItem('p2_end');
  if (p2_end !== null) $('#p2_end').val(p2_end);
  var p3_end = sessionStorage.getItem('p3_end');
  if (p3_end !== null) $('#p3_end').val(p3_end);

  // restore the values of the radio buttons that were checked
  //Method
  var methodVal = sessionStorage.getItem('method'); // local storage value
  if (methodVal !== null){
    $("input[name=method][value="+methodVal+"]").prop('checked', true);
  }
  else{
    $("input[name=method][value=local]").prop('checked', true);
  }

  var optionVal = sessionStorage.getItem('option'); // local storage value
  console.log(optionVal)
  if (optionVal !== null){
    $("input[name=option][value="+optionVal+"]").prop('checked', true);
  }
  else{
    $("input[name=option][value=cost]").prop('checked', true);
  }
  

}

// Before refreshing the page, save the form data to sessionStorage
window.onbeforeunload = function() {

  sessionStorage.setItem("cRAT", $('#cRAT').val());
  sessionStorage.setItem("cRTPCR", $('#cRTPCR').val());
  sessionStorage.setItem("cIGG", $('#cIGG').val());
  sessionStorage.setItem("dEffect", $('#dEffect').val());
  sessionStorage.setItem("method", $('input:radio[name="method"]:checked').val());
  sessionStorage.setItem("option", $('input:radio[name="option"]:checked').val());
  sessionStorage.setItem("p1" , $("#p1").val());
  sessionStorage.setItem("p2" , $("#p2").val());
  sessionStorage.setItem("p3" , $("#p3").val());

  sessionStorage.setItem("p1_start" , $("#p1_start").val());
  sessionStorage.setItem("p1_end" , $("#p1_end").val());
  sessionStorage.setItem("p2_start" , $("#p2_start").val());
  sessionStorage.setItem("p2_end" , $("#p2_end").val());
  sessionStorage.setItem("p3_start" , $("#p3_start").val());
  sessionStorage.setItem("p3_end" , $("#p3_end").val());
}  

