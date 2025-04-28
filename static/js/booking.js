document.addEventListener('DOMContentLoaded', () => {
    const today = new Date().toISOString().split('T')[0];

    const startDateInput = document.querySelector('input[name="startdate"]');
    const endDateInput = document.querySelector('input[name="enddate"]');

    if(!startDateInput.value) {
      startDateInput.value = today;
    }
    if(!endDateInput.value) {
      endDateInput.value = today;
    }

    startDateInput.min = today;
    endDateInput.min = startDateInput.value;

    startDateInput.addEventListener('change', () => {
      endDateInput.min = startDateInput.value;
      if (startDateInput.value > endDateInput.value) {
        endDateInput.value = startDateInput.value;
      }
    });
  });