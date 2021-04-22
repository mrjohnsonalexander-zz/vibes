document.addEventListener('DOMContentLoaded', () => {
  // Default vibe form
  vibeForm();
})

function vibeForm() {
  // TODO Add additional vibe form inputs
  // Vibe sharing form
  console.log('Create vibe form for');
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
  // Title
  form.append(document.createElement('input'));
  form_title = form.firstElementChild;
  form_title.classList.add('vibe-title');
  form_title.type = 'text';
  form_title.id = 'vibe-form-title-id';
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
  form_title.placeholder = "What vibe do you want to give?'"
  document.getElementById('vibe').replaceWith(vibe);
  // Button PUT post update
  document.querySelector('#vibe-form-button').addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    createVibe(event);
  });
}

async function createVibe(event){
  // Create vibe
  var vibe_title = document.querySelector('#vibe-form-title-id').value;
  console.log(vibe_title);
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken').value
  // Mannuall passing csrf token for vibe form since not using FormModel
  const request = new Request(
    '/vibe',
    {headers: {'X-CSRFToken': csrftoken}}
  );
  await fetch(request, {
      method: 'POST',
      body: JSON.stringify({
          title: vibe_title
      })
  }).then(response => response.json()).then(result => {console.log(result)});
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