var mode = 'markup';

function str_to_pointslist(str){
    let re = new RegExp('[0-9]{1,10}, [0-9]{1,10}', 'g');
    let pointsNumber = []
    do{ 
        var point = re.exec(str);
        if(point != null){
            xy = point[0].split(', ');
            x = parseInt(xy[0]);
            y = parseInt(xy[1]);
            pointsNumber.push([x, y]);
        }
    }while(point != null);
    return pointsNumber
};

function sendRequest(url, method, data, handler, resType=null)
{
    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = () => {
        if (xhr.readyState == 4)
        {
            if (xhr.status == 200)
            {   
                if(handler){
                    handler(xhr);
                } 
            }
            else
            {
                console.log('Что-то пошло не так');
            }
        }
        else
        {
            console.log('Загрузка');
        }
    }

    if(resType){xhr.responseType = resType}
    
    xhr.open(method, url, true);
    if (method.toLowerCase() == 'post'){
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(data));
    }
    else {xhr.send(null);}
};


function availability_check(){
    let url = "/availability_check";
    let str_split = window.location.href.split('/')
    let last = str_split.length
    let information = {prj_tsk: str_split[last-2]+'_'+str_split[last-1]};
    let handler = (res) =>{
        if (res.response[0] != '{'){
            document.location.href = res.response;
        }
    }
    sendRequest(url, 'POST', information, handler);
};

function send_info2(flag){
    let form = document.createElement('form');
    form.action = '/change_status';
    form.method = 'POST';
    form.innerHTML = '<input name="button" value="' + flag + '">';
    document.body.append(form);
    form.submit();
};

function distance(point1, point2){
    a = (point1[0] - point2[0]); 
    b = (point1[1] - point2[1]); 
    c = Math.pow((a*a + b*b), 0.5);
    return c
};