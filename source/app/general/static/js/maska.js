var select_list = document.getElementsByClassName('select_class');
var maska_list = document.getElementsByClassName('maska');

var show_all_btn = document.getElementById('show_all');
var hide_all_btn = document.getElementById('hide_all');


function change_class_code(projectName_, taskIndex_, maskID_, code_){
    let url = "/task_edit/change_class_code";
    let dt = {projectName: projectName_,
                taskIndex: taskIndex_,
                maskID: maskID_,
                code: code_
                };

    sendRequest(url, 'POST', dt, false);
}

function updateNameMask(maskID_){

    maska_list[Number(maskID_)].remove();
    document.getElementById('shape_'+maskID_).remove();

    maska_list = document.getElementsByClassName('maska');
    let len = maska_list.length;
    for (let i = 0; i<len; i++){
        if(i >= maskID_){
            document.getElementById('shape_'+(i+1)).remove();

            let maskaDOM = maska_list[i];

            let msk_name = maska_list[i].getElementsByClassName('mask_index')[0].textContent.split(' ');
            msk_name[1] = Number(msk_name[1])-1;
            maska_list[i].getElementsByClassName('mask_index')[0].textContent = msk_name.join(' ');


            let opt = select_list[i].getElementsByTagName('option');
            let col_opt = opt.length 
            for (let n = 0; n<col_opt; n++){
                let info_list = opt[n].value.split(';');
                info_list[2] = Number(info_list[2]) - 1 ;
                opt[n].value = info_list.join(';');
            }

            let points_str =  maskaDOM.getElementsByTagName('input')[0].value.split(';')[0];
            let points = str_to_pointslist(points_str);
            let coef = 1/Math.pow(2, imagesInfo.curLayer);
            for(let i=0; i<points.length; i++){
                points[i] = [points[i][0]*coef, points[i][1]*coef]; 
            }

            let index = maskaDOM.getElementsByClassName('mask_index')[0].textContent.split(' ')[1]
            let clr = maskaDOM.getElementsByTagName('input')[0].value.split(';')[1];
            let type = maskaDOM.getElementsByClassName('type')[0].innerHTML.split(' ')[1];

            createMask(cnv_mask, maskaDOM, points, clr, type, index);

            if(maskaDOM.getElementsByClassName('maska_view_check')[0].checked){
                // maskaDOM.getElementsByClassName('maska_view_check')[0].checked = true;
            maskaDOM.getElementsByClassName('maska_view_check')[0].dispatchEvent(new Event('change'));
            }
        }
    }
}

function delete_mask(projectName_, taskIndex_, maskID_){
    let url = "/task_edit/delete_mask";
    let dt = {projectName: projectName_,
                taskIndex: taskIndex_,
                maskID: maskID_
                };
    let handler = (req)=>{
        // location.reload();
        updateNameMask(maskID_)
    }
    sendRequest(url, 'POST', dt, handler);
};

function createMask(svg, maskControl, points, clr, type, i){
    let obj_maska;
    if(type==='polygon'){
        obj_maska = svg.polygon(points);
    }
    else if(type==='point'){
        obj_maska = svg.circle(R).move(points[0][0]-R/2, points[0][1]-R/2);
    }
    else if(type==='circle'){
        let radius = distance(points[0], points[1]);
        obj_maska = svg.ellipse(radius*2).move(points[0][0]-radius, points[0][1]-radius)
                                            .fill('none').stroke({ width: 2,  color: '#000000'});
    }
    else{
        let width = points[1][0] - points[0][0];
        let height = points[2][1] - points[1][1];
        let x;
        let y;
        if (width<0){x = points[1][0]}
        else {x = points[0][0] }

        if (height<0){y = points[2][1]}
        else {y = points[0][1] }
        if(type==='rect'){
            obj_maska = svg.rect(Math.abs(width), Math.abs(height))
                                .move(x, y);       
        }
        if(type==='line'){
            obj_maska = svg.polyline(points).fill('none');
        }
    }
    if(type==='line'){
        obj_maska.stroke({ width: 2,  color: clr})
            .id("shape_"+i)
            .on('mouseover', (event)=>{
                maskControl.style.background = 'LightGrey';
            })
            .on('mouseout', (event)=>{
                maskControl.style.background = 'white';
            })
            .hide();
    }
    else{
        obj_maska.fill(clr+'55')
            .stroke({ width: 2,  color: clr})
            .id("shape_"+i)
            .on('mouseover', (event)=>{
                maskControl.style.background = 'LightGrey';
                el = document.getElementById('shape_'+i);
                el.style.fill = clr+'bb';
                })
            .on('mouseout', (event)=>{
                maskControl.style.background = 'white';
                el = document.getElementById('shape_'+i);
                el.style.fill = clr+'55';    
            })
            .hide();
    }
    

            
    maskControl.onmouseover = (event)=>{
        maskControl.style.background = 'LightGrey';
        el = document.getElementById('shape_'+i);
        if(el.tagName != 'polyline'){
            clr = maskControl.getElementsByTagName('input')[0].value.split(';')[1];
            el.style.fill = clr+'bb'; 
        };
        
    };

    maskControl.onmouseout = (event)=>{
        maskControl.style.background =  'white'
        el = document.getElementById('shape_'+i);
        if(el.tagName != 'polyline'){
            clr = maskControl.getElementsByTagName('input')[0].value.split(';')[1];
            el.style.fill = clr+'55';
        }; 
    };

    maskControl.getElementsByTagName('input')[0].onchange = (event)=>{
        if (curMode != 'edit'){
            flag = maskControl.getElementsByTagName('input')[0].checked;
            el = document.getElementById('shape_'+i);
            if(flag){el.style.display = '';}
            else{el.style.display = 'none'}
        }
    };

    if(maskControl.getElementsByClassName('select_class').length === 0){
        return obj_maska;
    }

    maskControl.getElementsByClassName('select_class')[0].onchange = function(){
        let info_list = this.value.split(';');
        change_class_code(info_list[0], info_list[1], info_list[2], info_list[3]);
        let point_color = maska_list[i].getElementsByTagName('input')[0].value.split(';');
        point_color[1] = info_list[4];
        maskControl.getElementsByTagName('input')[0].value = point_color.join(';');
        maskControl.getElementsByClassName('color_img')[0].style.background = point_color[1]
        obj_maska.stroke({color: point_color[1]})
    };

    maskControl.getElementsByClassName('content_mask')[0].ondblclick = (event)=>{
        if (curMode === 'edit'){return}
        curMode = 'edit';
        if(curShape.object){
            curShape.object.remove();
            curShape.object = null;
            if(curShape.group){
                curShape.group.remove();
                curShape.group = null;
            }   
        }
        
        points_str =  maskControl.getElementsByTagName('input')[0].value.split(';')[0];
        points = str_to_pointslist(points_str);

        let coef = 1/Math.pow(2, imagesInfo.curLayer);
        for(let i=0; i<points.length; i++){
            points[i] = [points[i][0]*coef, points[i][1]*coef]; 
        }

        curTool = maskControl.getElementsByClassName('type')[0].innerHTML.split(' ')[1];
        curShape.points = points;
        curShape.type = curTool;
        let object_test = document.getElementById('shape_'+i);
        curShape.object = SVG(object_test);
        object_test.style.display = '';
        curShape.maskID = maskControl.getElementsByClassName('mask_index')[0].textContent.split(' ')[1]
        curShape.group = cnv_mask.group();
        
        if(type==='polygon'){
            drawPolygon();
        }
        else if(type==='rect'){
            drawRect();
        }
        else if(type==='line'){
            drawLine();
        }
        else if(type==='point'){
            drawPoint();
        }
        else if(type==='circle'){
            drawCircle();
        }
    };

    maskControl.getElementsByClassName('delete_btn')[0].onclick = (event)=>{
        let info_list = select_list[i].value.split(';');
        delete_mask(info_list[0], info_list[1], info_list[2])
    };
    
    return obj_maska;

};

function createAllMask(){
    let len = maska_list.length;
    for (let i = 0; i<len; i++){
        let svg = SVG('#svg');
        let points_str =  maska_list[i].getElementsByTagName('input')[0].value.split(';')[0];
        let points = str_to_pointslist(points_str);
        let clr = maska_list[i].getElementsByTagName('input')[0].value.split(';')[1];
        let type = maska_list[i].getElementsByClassName('type')[0].innerHTML.split(' ')[1];

        createMask(svg, maska_list[i],points, clr, type, i);
    }
};

function showAll(){
    let len = maska_list.length;
    document.getElementById('show_all').style.display = 'none';
    document.getElementById('hide_all').style.display = ''; 
    for (let i = 0; i<len; i++){
        let el = document.getElementById('shape_'+i);
        if (el.style.display==='none'){
            el.style.display='';
            maska_list[i].getElementsByTagName('input')[0].checked = true;
        }
    }
};

function hideAll(){
    let len = maska_list.length;
    document.getElementById('show_all').style.display = '';
    document.getElementById('hide_all').style.display = 'none'; 
    for (let i = 0; i<len; i++){
        let el = document.getElementById('shape_'+i);
        if (el.style.display===''){
            el.style.display='none';
            maska_list[i].getElementsByTagName('input')[0].checked = false;
        }
    }
};

show_all_btn.addEventListener('click', showAll);

hide_all_btn.addEventListener('click', hideAll);
