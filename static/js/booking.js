function test() {
    const startdateInput = document.getElementById('startdate');
    const startdateString = startdateInput.value;
    const startdate = new Date(startdateString);

    const enddateInput = document.getElementById('enddate');
    const enddateString = enddateInput.value;
    const enddate = new Date(enddateString);

    console.log(startdate);
    console.log(enddate);
}