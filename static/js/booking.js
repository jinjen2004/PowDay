function test() {
    const startdateInput = document.getElementById('startdate');
    const startdateString = startdateInput.value;
    const startdate = new Date(startdateString + "T00:00");

    const enddateInput = document.getElementById('enddate');
    const enddateString = enddateInput.value;
    const enddate = new Date(enddateString + "T00:00");

    const today = new Date();

    if(startdate > enddate || startdate <= today) {
        document.getElementById("validtext").innerHTML = "invalid date input";
    }
    else {
        document.getElementById("validtext").innerHTML = "";
    }
}