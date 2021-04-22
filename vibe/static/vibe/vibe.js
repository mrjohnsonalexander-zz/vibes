document.addEventListener('DOMContentLoaded', () => {
  // Default vibe form
  vibeForm();
})

function vibeForm() {
  // Form used to create vibes
  console.log('Create vibe form');
  vibe = document.createElement('div');
  vibe.id = 'vibe-id';
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
  form_title.id = 'vibe-form-title-id';
  form_title.placeholder = "What is your vibe's title?"
  // Description
  form.append(document.createElement('input'));
  form_description = form.lastElementChild;
  form_description.classList.add('vibe-description');
  form_description.type = 'text';
  form_description.id = 'vibe-form-description-id';
  form_description.placeholder = "What is your vibe's description?"
  // Location
  form.append(document.createElement('input'));
  form_location = form.lastElementChild;
  form_location.classList.add('vibe-location');
  form_location.type = 'text';
  form_location.id = 'vibe-form-location-id';
  form_location.placeholder = "Seattle"
  // img_url
  form.append(document.createElement('input'));
  form_img_url = form.lastElementChild;
  form_img_url.classList.add('vibe-img-url');
  form_img_url.type = 'text';
  form_img_url.id = 'vibe-form-img-url-id';
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
  form_button.id = 'vibe-form-button';
  form_button.classList.add('vibe-button');
  form_button.type = 'button';
  form_button.value = 'Create';
  document.getElementById('vibe').replaceWith(vibe);
  // Create vibe with form data
  document.querySelector('#vibe-form-button').addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    createVibe(event);
  });
}

async function createVibe(event){
  // Create Vibe and Refresh Page
  // vibeForm values
  var vibe_title = document.querySelector('#vibe-form-title-id').value;
  var vibe_description = document.querySelector('#vibe-form-description-id').value;
  var vibe_location = document.querySelector('#vibe-form-location-id').value;
  var vibe_img_url = document.querySelector('#vibe-form-img-url-id').value;
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken').value
  // Mannuall passing csrf token for vibe form since not using FormModel
  console.log("vibeForm values being POST'd");
  const request = new Request(
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