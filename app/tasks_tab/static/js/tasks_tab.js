var edit_attr = 0;
var tsk_ind;

var pageL = 0;
var pageR = 0;

var control_panel = document.getElementsByClassName('Control');
// var attr_inp_list= control_panel[0].getElementsByTagName('input');
var in_work = document.getElementsByClassName('in_work')[0];
var on_inspection = document.getElementsByClassName('on_inspection')[0];


function scrollAddLeft(){
    if ((this.scrollHeight - (this.scrollTop + this.clientHeight))<=1.5){
        pageL = pageL + 1;
        info = {page: pageL,
                status: 'left'}
        let url = "/tasks/get_tasks";
        let handler = (res)=>{
            tasks = res.response.getElementsByTagName('fieldset');
            let len_task = tasks.length
            for (let i=0; i<len_task; i++){
                this.append(tasks.item(0))
            }
        }
        sendRequest(url, 'POST', info, handler, 'document');
    };
};

function scrollAddRight(){
    if ((this.scrollHeight - (this.scrollTop + this.clientHeight))<=1.5){
        pageR = pageR + 1;
        info = {page: pageR,
                status: 'right'}
        let url = "/tasks/get_tasks";
        let handler = (res)=>{
            tasks = res.response.getElementsByTagName('fieldset');
            let len_task = tasks.length
            for (let i=0; i<len_task; i++){
                this.append(tasks.item(0))
            }
        }
        sendRequest(url, 'POST', info, handler, 'document');
    };
};

in_work.addEventListener('scroll', scrollAddLeft);
on_inspection.addEventListener('scroll', scrollAddRight);


function on_off_edit_attr(){
    var len = attr_inp_list.length;
    for (let i = 0; i<len; i++){
        if (edit_attr===1){attr_inp_list[i].readOnly  = false;}
        else{attr_inp_list[i].readOnly  = true;}
    };
}


function view_attr(attr){
    attr_inp_list[0].value = attr['LA'];
    attr_inp_list[1].value = attr['ALT'];
    attr_inp_list[2].value = attr['LAT'];
    attr_inp_list[3].value = attr['LON'];
    attr_inp_list[4].value = attr['SUN'];
    attr_inp_list[5].value = attr['SPA'];
    attr_inp_list[6].value = attr['SIZE'];
    attr_inp_list[7].value = attr['DATE'];
    attr_inp_list[8].value = attr['TIME'];
};


in_work.addEventListener(`dragstart`, (evt) => {
    evt.target.classList.add(`selected`);
    evt.dataTransfer.setData('task', evt.target.id);
})

in_work.addEventListener(`dragend`, (evt) => {
    evt.target.classList.remove(`selected`);
});

in_work.addEventListener('dragover', (evt) => {
    evt.preventDefault();
});

in_work.addEventListener('drop', (evt) => {
    evt.stopPropagation();
    let a = evt.dataTransfer.getData('task');
    if (document.getElementById(a).getAttribute('class').split(' ')[1] === 'inspec'){
        let form = document.createElement('form');
        form.action = document.getElementById(a).getAttribute('name');
        form.method = 'POST';
        form.innerHTML = '<input name="button" value="' + '<<' + '">';
        document.body.append(form);
        form.submit();
    }
})


on_inspection.addEventListener(`dragstart`, (evt) => {
    evt.target.classList.add(`selected`);
    evt.dataTransfer.setData('task', evt.target.id);
})

on_inspection.addEventListener(`dragend`, (evt) => {
    evt.target.classList.remove(`selected`);
});

on_inspection.addEventListener('dragover', (evt) => {
    evt.preventDefault();
});


on_inspection.addEventListener('drop', (evt) => {
    evt.stopPropagation();
    let a = evt.dataTransfer.getData('task');
    if (document.getElementById(a).getAttribute('class').split(' ')[1] === 'todo'){
        let form = document.createElement('form');
        form.action = document.getElementById(a).getAttribute('name');
        form.method = 'POST';
        form.innerHTML = '<input name="button" value="' + '>>' + '">';
        document.body.append(form);
        form.submit();
    }
})
