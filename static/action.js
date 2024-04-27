// file upload script

// const fileUploader = document.getElementById('file-uploader');
// fileUploader.addEventListener('change', (event) => {

//   const files = event.target.files;
//   console.log('files', files);
  
//   const feedback = document.getElementById('feedback');
//   const reply = `File ${files[0].name} uploaded successfully!`;
//   feedback.innerHTML = reply;
// });


document.addEventListener('DOMContentLoaded', function() {
    const fileUploader = document.getElementById('file-uploader');

    // Check if file-uploader element exists before adding event listener
    if (fileUploader) {
        fileUploader.addEventListener('change', (event) => {
            const files = event.target.files;
            console.log('files', files);
            
            const feedback = document.getElementById('feedback');
            if (feedback) {
                const reply = `File ${files[0].name} uploaded successfully!`;
                feedback.innerHTML = reply;
            } else {
                console.error("Feedback element not found.");
            }
        });
    } else {
        console.error("File uploader element not found.");
    }
});
