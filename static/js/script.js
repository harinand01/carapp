document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const hamburger = document.querySelector('.hamburger-menu');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger && navLinks) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // Auto-dismiss alerts after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => {
                alert.remove();
            }, 500); // Wait for transition to finish
        }, 3000);
    });

    // Client-Side Form Validation
    const vehicleForm = document.querySelector('.add-vehicle-container form');
    if (vehicleForm) {
        vehicleForm.addEventListener('submit', (e) => {
            let isValid = true;
            const errors = [];

            // Get fields by their name attribute or placeholder/context if name isn't easy via standard class
            // Django forms render with name="make", name="year", etc.
            const makeInput = vehicleForm.querySelector('input[name="make"]');
            const modelInput = vehicleForm.querySelector('input[name="model"]');
            const plateInput = vehicleForm.querySelector('input[name="license_plate"]');
            const yearInput = vehicleForm.querySelector('input[name="year"]');

            // Basic Required Checks (redundant with HTML5 'required' usually, but good for custom UI)
            if (makeInput && !makeInput.value.trim()) {
                isValid = false;
                errors.push("Make is required.");
                makeInput.style.borderColor = "var(--danger)";
            }
            if (modelInput && !modelInput.value.trim()) {
                isValid = false;
                errors.push("Model is required.");
                modelInput.style.borderColor = "var(--danger)";
            }
            if (plateInput && !plateInput.value.trim()) {
                isValid = false;
                errors.push("License Plate is required.");
                plateInput.style.borderColor = "var(--danger)";
            }

            // Year Validation
            if (yearInput) {
                const currentYear = new Date().getFullYear();
                const yearVal = parseInt(yearInput.value);

                if (isNaN(yearVal) || yearVal < 1900 || yearVal > currentYear + 1) {
                    isValid = false;
                    errors.push(`Year must be between 1900 and ${currentYear + 1}.`);
                    yearInput.style.borderColor = "var(--danger)";
                } else {
                    yearInput.style.borderColor = ""; // Reset
                }
            }

            if (!isValid) {
                e.preventDefault(); // Stop submission

                // Show errors - create a temporary alert box
                const existingAlert = document.querySelector('.js-error-alert');
                if (existingAlert) existingAlert.remove();

                const alertBox = document.createElement('div');
                alertBox.className = 'alert error js-error-alert';
                alertBox.innerHTML = `<strong>Validation Error:</strong><br>${errors.join('<br>')}`;

                // Insert before the form
                vehicleForm.insertBefore(alertBox, vehicleForm.firstChild);

                // Auto dismiss this new alert too
                setTimeout(() => {
                    alertBox.style.opacity = '0';
                    setTimeout(() => alertBox.remove(), 500);
                }, 5000);
            }
        });

        // Clear error styles on input
        const inputs = vehicleForm.querySelectorAll('input');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                input.style.borderColor = "";
            });
        });
    }

    // Booking Form Validation
    const bookingForm = document.querySelector('.booking-container form');
    if (bookingForm) {
        const dateInput = bookingForm.querySelector('input[name="booking_date"]');
        const timeSelect = bookingForm.querySelector('select[name="time_slot"]');

        // Helper to check and disable past times
        const checkTimeSlots = () => {
            if (!dateInput || !timeSelect) return;

            const selectedDateVal = dateInput.value;
            if (!selectedDateVal) return;

            // Handle date parsing carefully so timezone issues don't mess up "today" check
            // input value is YYYY-MM-DD. unique logic:
            const today = new Date();
            const todayStr = today.toISOString().split('T')[0];
            const isToday = (selectedDateVal === todayStr);

            if (isToday) {
                const currentHour = today.getHours();
                const currentMinute = today.getMinutes();

                Array.from(timeSelect.options).forEach(option => {
                    // Assuming format "HH:MM - HH:MM" e.g. "09:00 - 10:00"
                    const text = option.text.trim();
                    const match = text.match(/^(\d{1,2}):(\d{2})/);

                    if (match) {
                        const slotHour = parseInt(match[1], 10);
                        const slotMinute = parseInt(match[2], 10);

                        // Compare time
                        if (slotHour < currentHour || (slotHour === currentHour && slotMinute < currentMinute)) {
                            option.disabled = true;
                            // Add a visual indicator like (Passed)
                            if (!option.text.includes('(Passed)')) {
                                option.text += ' (Passed)';
                            }
                        } else {
                            option.disabled = false;
                            option.text = option.text.replace(' (Passed)', '');
                        }
                    }
                });
            } else {
                // If not today, enable all
                Array.from(timeSelect.options).forEach(option => {
                    option.disabled = false;
                    option.text = option.text.replace(' (Passed)', '');
                });
            }
        };

        // 1. Set 'min' attribute to today to disable past dates in the picker
        if (dateInput) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.setAttribute('min', today);

            // Listen for changes
            dateInput.addEventListener('change', checkTimeSlots);
            // Run once on load
            checkTimeSlots();
        }

        // 2. Validate on submit
        bookingForm.addEventListener('submit', (e) => {
            let isValid = true;
            const errors = [];

            if (dateInput) {
                const inputVal = dateInput.value; // YYYY-MM-DD
                const todayStr = new Date().toISOString().split('T')[0];

                if (!inputVal) {
                    isValid = false;
                    errors.push("Date is required.");
                    dateInput.style.borderColor = "var(--danger)";
                } else if (inputVal < todayStr) {
                    isValid = false;
                    errors.push("You cannot book for a past date.");
                    dateInput.style.borderColor = "var(--danger)";
                } else {
                    dateInput.style.borderColor = "";
                }
            }

            const vehicleSelect = bookingForm.querySelector('select[name="vehicle"]');
            if (vehicleSelect && !vehicleSelect.value) {
                isValid = false;
                errors.push("Please select a vehicle.");
                vehicleSelect.style.borderColor = "var(--danger)";
            }

            // Check time slot purely based on disabled state or re-calc
            if (timeSelect && timeSelect.value) {
                const selectedOption = timeSelect.options[timeSelect.selectedIndex];
                if (selectedOption.disabled) {
                    isValid = false;
                    errors.push("Selected time slot has already passed.");
                    timeSelect.style.borderColor = "var(--danger)";
                } else {
                    timeSelect.style.borderColor = "";
                }
            }

            if (!isValid) {
                e.preventDefault();

                const existingAlert = document.querySelector('.js-error-alert');
                if (existingAlert) existingAlert.remove();

                const alertBox = document.createElement('div');
                alertBox.className = 'alert error js-error-alert';
                alertBox.innerHTML = `<strong>Booking Error:</strong><br>${errors.join('<br>')}`;

                // Insert before the form content wrapper or typically the first child
                bookingForm.insertBefore(alertBox, bookingForm.firstChild);

                setTimeout(() => {
                    alertBox.style.opacity = '0';
                    setTimeout(() => alertBox.remove(), 500);
                }, 5000);
            }
        });
    }
});
