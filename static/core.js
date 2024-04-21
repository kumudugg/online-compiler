function handleTabKeyPress(event) {
    if (event.keyCode === 9) {
        event.preventDefault();
        var textarea = document.getElementsByTagName("textarea")[0];
        
        // Get the current cursor position
        var start = textarea.selectionStart;
        var end = textarea.selectionEnd;
        
        // Insert tab character at the cursor position
        textarea.value = textarea.value.substring(0, start) + "\t" + textarea.value.substring(end);
        
        // Move the cursor position after the inserted tab
        textarea.selectionStart = textarea.selectionEnd = start + 1;
    }
}


function clearAll() {
    document.getElementsByTagName("textarea")[0].value = " ";
    document.getElementsByTagName("pre")[0].innerHTML = " ";
}


document.addEventListener("DOMContentLoaded", function() {
    // Get the textarea element
    var codeTextarea = document.getElementsByTagName("textarea")[0];
    
    // Store the code entered by the user when the form is submitted
    document.getElementById("execute").addEventListener("click", function() {
        localStorage.setItem("userCode", codeTextarea.value);
    });
    
    // Restore the code when the page is loaded
    var savedCode = localStorage.getItem("userCode");
    if (savedCode) {
        codeTextarea.value = savedCode;
    }
});



