import 'whatwg-fetch'
import Cookies from 'js-cookie';
const url = "/api/databases/";
const csrftoken = Cookies.get('csrftoken');
const fetchHeaders = new Headers({
    "X-CSRFToken": csrftoken,
    "Accept": "application/json",
    "Content-Type": "application/json"
})

class EditingVars{
  constructor(editingFields, parent){
    this.editMode = false;
    this.editingFields = editingFields;
    this.parent = parent;
  }
  populate(args){
    let x = {
      name: this.name,
      id: this.id,
      description: this.description,
      link: this.link
    } = args;

    this.editMode = true;
  }
  save(){
    let postData = {};
    let editUrl = url + this.id + "/";
    var self = this;
    this.loading = true;
    this.editingFields.forEach(field => {
      postData[field] = this[field]
    });
    fetch(editUrl, {
      method: 'PUT',
      body: JSON.stringify(postData),
      credentials: 'include',
      headers: fetchHeaders
    }).then((response) => {
      response.json().then(function(update){
        self.parent.update(update);
        self.editMode = false;
        self.loading = false;
      });
    });
  }
  cancel(){
    this.editMode = false;
  }
}

class Database {
  constructor(args) {
    this.update(args);
    this.editing = new EditingVars(
      ["name", "id", "description", "link"], this
    );
  }
  update(args){
    let x = {
      name: this.name,
      id: this.id,
      description: this.description,
      link: this.link
    } = args;
  }
  edit (){
    this.editing.populate(this);
  }
  static load(){
    let result = new Promise((resolve, reject) => {
      fetch(url, {headers: fetchHeaders, credentials: 'include'}).then(function(data){
        if(data.status < 400){
          data.json().then(function(rawDatabases){
            let databases = rawDatabases.map(function(rawDatabase){
              return new Database(rawDatabase);
            });
            resolve(databases);
          });
        }
        else{
          reject("fail");
        }
      });
    });
    result.catch(function(){});

    return result;
  }
}


export {Database}
