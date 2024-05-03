


function handleClear(){
    var formData = new FormData();
    formData.append('coords', "clear");
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/click', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload();
        }
    };
    xhr.send(formData); 
}


function handleCompute(){
    
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/compute', true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.reload();
        }
    };
    xhr.send(); 
}



function handleFile() {
  var fileInput = document.getElementById('fileInput');
  var imageDisplay = document.getElementById('imageDisplay');

  var file = fileInput.files[0];
  if (!file) {
      alert("Veuillez sélectionner un fichier.");
      return;
  }

  var formData = new FormData();
  formData.append('file', file);

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/upload', true);
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          console.log('Fichier uploadé avec succès');
          window.location.reload();
      } else if (xhr.readyState === 4 && xhr.status !== 200) {
          console.log('Erreur lors de l\'upload du fichier');
      }
  };
  xhr.send(formData);
  
}

function onClickEvent(event){
  var rect = imageDisplay.getBoundingClientRect();
  var x = (event.clientX - rect.left) / (rect.right -rect.left); // Position horizontale du clic par rapport à l'image
  var y = (event.clientY - rect.top)/((rect.bottom -rect.top)); // Position verticale du clic par rapport à l'image
  
  console.log('Position du clic : ' + x + ', ' + y);

  var formData = new FormData();
  formData.append('coords', x + ';' + y);
  
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/click', true);
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          window.location.reload();
      }
  };
  xhr.send(formData);
}