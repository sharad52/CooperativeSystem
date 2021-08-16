window.onload = function() {
    var mainInput = document.getElementById("datepicker-first");
    var dateHolder = document.getElementById("datepicker-second");
    
    mainInput.nepaliDatePicker({
        ndpYear: true,
        ndpMonth: true,
        ndpYearCount: 15
    });
    dateHolder.nepaliDatePicker({
        ndpYear: true,
        ndpMonth: true,
        ndpYearCount: 15
    });
   
};

let CurrentDate = document.getElementById('aajakomiti');
CurrentDate.innerHTML = "आजको मितीः" + NepaliFunctions.GetCurrentBsDate().year + "/" + NepaliFunctions.GetCurrentBsDate().month + "/" + NepaliFunctions.GetCurrentBsDate().day;

const navToggle = document.querySelector("#display-item");
const subItem = document.querySelector("#hidden-item");

navToggle.addEventListener("click",function(){
	if (subItem.classList.contains("display-item")){
		subItem.classList.remove("display-item");
	}
	else{
		subItem.classList.add("display-item");
	}
	// subItem.classList.toggle("display-item");

});


