document.addEventListener('DOMContentLoaded', () => {
  // Default vibe form
  vibeForm();
  // Profile Fan
  document.querySelector('#fan-button').addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    fan();
  });
})

async function fan(){
// Add or Remove Profile fan
console.log('fan-button clicked')
vibe_button = document.querySelector('#fan-button');
await fetch(`/fan/${vibe_button.dataset.vibeid}/${vibe_button.dataset.fan}`, {
method: 'PUT',
}).then(response => response.json()).then(result => {console.log(result)});
console.log(`Profile ${vibe_button.dataset.profileid} fans updated`)
}

function vibeForm(vibe_id='') {
  console.log('Create vibe form');
  vibe = document.createElement('div');
  vibe.dataset.vibeid = vibe_id;
  vibe.id = `vibe-${vibe_id}`;
  vibe.classList.add("vibe-form");
  vibe.append(document.createElement('h4'));
  headers = vibe.firstElementChild;
  headers.classList.add("vibe-header");
  headers.innerHTML = "Vibe";
  vibe.append(document.createElement('form'));
  form = vibe.lastElementChild;
  form.method = 'POST';
  form.action = '/vibe';
  form.enctype="multipart/form-data"
  // Title
  form.append(document.createElement('input'));
  form_title = form.firstElementChild;
  form_title.classList.add('vibe-title');
  form_title.type = 'text';
  form_title.id = `vibe-form-title-${vibe_id}`;
  form_title.placeholder = "What is your vibe's title?"
  // Description
  form.append(document.createElement('input'));
  form_description = form.lastElementChild;
  form_description.classList.add('vibe-description');
  form_description.type = 'text';
  form_description.id = `vibe-form-description-${vibe_id}`;
  form_description.placeholder = "What is your vibe's description?"
  // Location
  form.append(document.createElement('input'));
  form_location = form.lastElementChild;
  form_location.classList.add('vibe-location');
  form_location.type = 'text';
  form_location.id = `vibe-form-location-${vibe_id}`;
  form_location.placeholder = "Seattle"
  // img_url
  form.append(document.createElement('input'));
  form_img_url = form.lastElementChild;
  form_img_url.classList.add('vibe-img-url');
  form_img_url.type = 'text';
  form_img_url.id = `vibe-form-img-url-${vibe_id}`;
  form_img_url.placeholder = "https://i.redd.it/61iy0forpz331.jpg"
  // csrf token
  form.append(document.createElement('input'));
  form_csrf = form.lastElementChild;
  form_csrf.type = 'hidden';
  form_csrf.name = 'csrfmiddlewaretoken';
  form_csrf.value = getCookie('csrftoken');
  // Button
  form.append(document.createElement('input'));
  form_button = form.lastElementChild;
  form_button.id = `vibe-form-button-${vibe_id}`;
  form_button.classList.add('vibe-button');
  form_button.type = 'button';
  form_button.value = 'Create';
  // Create new Update form with existing vibe data
  if (vibe_id == '') {    
    document.getElementById('vibe').replaceWith(vibe);
    // Create vibe with form data
    document.querySelector('#vibe-form-button-').addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      createVibe();
    });
  } else {
    form_title.placeholder = document.querySelector(`#vibe-record-title-${vibe_id}`).innerText;
    form_description.placeholder = document.querySelector(`#vibe-record-description-${vibe_id}`).innerText;
    form_location.placeholder = document.querySelector(`#vibe-record-location-${vibe_id}`).innerText;
    form_img_url.placeholder = document.querySelector(`#vibe-pic-${vibe_id}`).src;
    document.getElementById(`vibe-${vibe_id}`).replaceWith(vibe);
    form_button.value = 'Save';
    // Create vibe with form data
    document.querySelector(`#vibe-form-button-${vibe_id}`).addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      updateVibe(event);
    });
  } 
}

async function updateVibe(event){
  // Get vibe form Values
  vibe_id = event.target.parentElement.parentElement.getAttribute("data-vibeid");
  var vibe_title = document.querySelector(`#vibe-form-title-${vibe_id}`).value;
  var vibe_description = document.querySelector(`#vibe-form-description-${vibe_id}`).value;
  var vibe_location = document.querySelector(`#vibe-form-location-${vibe_id}`).value;
  var vibe_img_url = document.querySelector(`#vibe-form-img-url-${vibe_id}`).value;
  var csrftoken = document.querySelector('[name=csrfmiddlewaretoken').value
  // Get placeholders if no value provided
  if (vibe_title == '') {
    vibe_title = document.querySelector(`#vibe-form-title-${vibe_id}`).placeholder;
  }
  if (vibe_description == '') {
    vibe_description = document.querySelector(`#vibe-form-description-${vibe_id}`).placeholder;
  }
  if (vibe_location == '') {
    vibe_location = document.querySelector(`#vibe-form-location-${vibe_id}`).placeholder;
  }
  if (vibe_img_url == '') {
    vibe_img_url = document.querySelector(`#vibe-form-img-url-${vibe_id}`).placeholder;
  }
  // Mannuall passing csrf token for vibe form since not using FormModel
  console.log("Vibe being updated");
  var request = new Request(
    `/vibe/${vibe_id}`,
    {headers: {'X-CSRFToken': csrftoken}}
  );
  await fetch(request, {
      method: 'PUT',
      body: JSON.stringify({
          title: vibe_title,
          description: vibe_description,
          location: vibe_location,
          img_url: vibe_img_url,
      })
  }).then(response => {
        if (response.status == 200) {
            location.reload()
        } else {
          console.log(response);
        }
      })
}

async function createVibe(){
  // Create Vibe and Refresh Page
  // vibeForm values
  var vibe_title = document.querySelector('#vibe-form-title-').value;
  var vibe_description = document.querySelector('#vibe-form-description-').value;
  var vibe_location = document.querySelector('#vibe-form-location-').value;
  var vibe_img_url = document.querySelector('#vibe-form-img-url-').value;
  var csrftoken = document.querySelector('[name=csrfmiddlewaretoken').value
  // Mannuall passing csrf token for vibe form since not using FormModel
  console.log("vibeForm values being POST'd");
  request = new Request(
    '/vibe',
    {headers: {'X-CSRFToken': csrftoken}}
  );
  await fetch(request, {
      method: 'POST',
      body: JSON.stringify({
          title: vibe_title,
          description: vibe_description,
          location: vibe_location,
          img_url: vibe_img_url,
      })
  }).then(response => {
        if (response.status == 200) {
            location.reload()
        } else {
          console.log(response);
        }
      })
}

// This function comes from:
// https://docs.djangoproject.com/en/3.1/ref/csrf/
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}