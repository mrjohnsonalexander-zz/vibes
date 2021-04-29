document.addEventListener('DOMContentLoaded', () => {
  // Profile Fan
  document.querySelector('#fan-button').addEventListener('click', (event) => {
    event.preventDefault();
    event.stopPropagation();
    fan();
  });
  // Default vibe form
  vibeForm();
  // Default load vibes
  load_vibes();
})

// Continuous vibe scroll
let counter = 1;
// Paginator(vibes, 10) is returned from views.py 
const vibe_batch_count = 10;
let vibes_loaded = false;
window.onscroll = () => {
  if (window.screen.height + window.scrollY >= document.body.offsetHeight) {
    if(!vibes_loaded) {
      // load_vibes updates vibes_loaded to false when complete
      vibes_loaded = true;
      load_vibes();
    }
  }
}

async function load_vibes(){
  // Client batch
  var start = counter;
  const end = start + vibe_batch_count -1;
  // Get page of vibe records
  
  await fetch(`/vibes?page=${end / 10}`, {
    method: 'GET',
  }).then(resp => resp.json()).then(vibes => {
    for (i = 0; i < 10; i++) {
      // add page of vibe records to UI
      vibe = vibes[i];
      add_vibeRecord(vibe);
    }
    counter = end + 1;
  })
  // Enable next firing
  vibes_loaded = false;
}

function add_vibeRecord(vibe) {
  // Adding vibe record
  vibe_r = document.createElement('div');
  vibe_r.dataset.vibeid = vibe.id;
  vibe_r.id = `vibe-${vibe.id}`;
  vibe_r.classList.add('vibe-record');
  // record Pic
  vibe_r.append(document.createElement('a'));
  pic = vibe_r.firstElementChild;
  pic.href = `/vibe/${vibe.id}`
  pic.append(document.createElement('img'));
  img = pic.firstElementChild;
  img.id = `vibe-pic-${vibe.id}`
  img.classList.add("pic");
  img.src = vibe.img_url;
  img.alt = "Image not found";
  // record metadata
  vibe_r.append(document.createElement('ul'));
  ul = vibe_r.lastElementChild;
  ul.classList.add("vibe-metadata");
  // Link to vibe creator's profile
  ul.append(document.createElement('li'));
  profile = ul.firstElementChild;
  profile.id = `vibe-record-creator-${vibe.id}`;
  profile.append(document.createElement('a'));
  profile_attr = profile.firstElementChild;
  profile_attr.href = `/profile/${vibe.creator}`;
  profile_attr.innerHTML = vibe.creator;
  // vibeForm replaces record for editing
  ul.append(document.createElement('li'));
  edit = ul.lastElementChild;
  edit.append(document.createElement('a'));
  edit_attr = edit.lastElementChild;
  edit_attr.href = `javascript:vibeForm(${vibe.id});`;
  edit_attr.innerHTML = 'Edit';
  // record title
  ul.append(document.createElement('li'));
  title = ul.lastElementChild;
  title.id = `vibe-record-title-${vibe.id}`;
  title.innerHTML = vibe.title;
  // record description
  ul.append(document.createElement('li'));
  description = ul.lastElementChild;
  description.id = `vibe-record-description-${vibe.id}`;
  description.innerHTML = vibe.description;
  // record location
  ul.append(document.createElement('li'));
  loc = ul.lastElementChild;
  loc.id = `vibe-record-location-${vibe.id}`;
  loc.innerHTML = vibe.location;
  // record date_created
  ul.append(document.createElement('li'));
  date_created = ul.lastElementChild;
  date_created.id = `vibe-record-date-${vibe.id}`;
  date_created.innerHTML = vibe.date_created;
  // record cheers
  ul.append(document.createElement('li'));
  cheers = ul.lastElementChild;
  cheers.append(document.createElement('a'));
  cheers_emoji = cheers.lastElementChild;
  cheers_emoji.href = `javascript:vibeCheers(${vibe.id});`;
  cheers_emoji.innerHTML = "&#127867;";
  cheers.append(document.createElement('a'));
  cheers_count = cheers.lastElementChild;
  cheers_count.innerHTML = vibe.cheers;
  // Add vibe record
  console.log(`adding vibe ${vibe.id} record`);
  document.querySelector('#vibes').append(vibe_r);
}

async function fan(){
  // Add or Remove Profile fan
  vibe_button = document.querySelector('#fan-button');
  await fetch(`/fan/${vibe_button.dataset.profileid}/${vibe_button.dataset.fan}`, {
      method: 'PUT',
  }).then(response => response.json()).then(result => {console.log(result)});
  console.log(`Profile ${vibe_button.dataset.profileid} fans updated`)
}

function vibeForm(vibe_id='') {
  // Vibe form with placeholders
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
        // Update vibe without reload and log errors
        if (response.status == 200) {
          vibeRecord(vibe_id);
        } else {
          console.log(response);
          vibeRecord(vibe_id);
        }
      })
}

async function vibeRecord(vibe_id) {
  // Get vibe data, replace vibe form with record
  await fetch(`/vibe_details/${vibe_id}`, {
      method: 'GET',
     }).then(response => response.json()).then(result => {
          // Create vibe record
          vibe_r = document.createElement('div');
          vibe_r.dataset.vibeid = vibe_id;
          vibe_r.id = `vibe-${vibe_id}`;
          vibe_r.classList.add('vibe-record');
          // record Pic
          vibe_r.append(document.createElement('a'));
          pic = vibe_r.firstElementChild;
          pic.href = `/vibe/${vibe_id}`
          pic.append(document.createElement('img'));
          img = pic.firstElementChild;
          img.id = `vibe-pic-${vibe_id}`
          img.classList.add("pic");
          img.src = result.img_url;
          img.alt = "Image not found";
          // record metadata
          vibe_r.append(document.createElement('ul'));
          ul = vibe_r.lastElementChild;
          ul.classList.add("vibe-metadata");
          // Link to vibe creator's profile
          ul.append(document.createElement('li'));
          profile = ul.firstElementChild;
          profile.id = `vibe-record-creator-${result.id}`;
          profile.append(document.createElement('a'));
          profile_attr = profile.firstElementChild;
          profile_attr.href = `/profile/${result.creator}`;
          profile_attr.innerHTML = result.creator;
          // vibeForm replaces record for editing
          ul.append(document.createElement('li'));
          edit = ul.lastElementChild;
          edit.append(document.createElement('a'));
          edit_attr = edit.lastElementChild;
          edit_attr.href = `javascript:vibeForm(${result.id});`;
          edit_attr.innerHTML = 'Edit';
          // record title
          ul.append(document.createElement('li'));
          title = ul.lastElementChild;
          title.id = `vibe-record-title-${vibe_id}`;
          title.innerHTML = result.title;
          // record description
          ul.append(document.createElement('li'));
          description = ul.lastElementChild;
          description.id = `vibe-record-description-${vibe_id}`;
          description.innerHTML = result.description;
          // record location
          ul.append(document.createElement('li'));
          loc = ul.lastElementChild;
          loc.id = `vibe-record-location-${vibe_id}`;
          loc.innerHTML = result.location;
          // record date_created
          ul.append(document.createElement('li'));
          date_created = ul.lastElementChild;
          date_created.id = `vibe-record-date-${vibe_id}`;
          date_created.innerHTML = result.date_created;
          // record cheers
          ul.append(document.createElement('li'));
          cheers = ul.lastElementChild;
          cheers.append(document.createElement('a'));
          cheers_emoji = cheers.lastElementChild;
          cheers_emoji.href = `javascript:vibeCheers(${vibe_id});`;
          cheers_emoji.innerHTML = "&#127867;";
          cheers.append(document.createElement('a'));
          cheers_count = cheers.lastElementChild;
          cheers_count.innerHTML = result.cheers;
          // Replace vibeForm with vibe Record
          console.log("replacing div")
          document.getElementById(`vibe-${vibe_id}`).replaceWith(vibe_r);
      });
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

async function vibeCheers(vibe_id){
  // Heart Emjoi will add/remove like for current user
  console.log(`Updating vibe ${vibe_id} cheers`);
  await fetch(`/cheers/${vibe_id}`, {
      method: 'PUT',
  }).then(response => {console.log(response)});
  // Update HTML with vibe.cheers
  vibeRecord(vibe_id);
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