
(function() {
    var createBasedButton = document.getElementById('createBased');
    var favDialog = document.getElementById('createBasedStep1');
    var favDialog2 = document.getElementById('createBasedStep2');

    var selectProjectBtn = document.getElementById('selectProjectBtn');
    var selectProject = document.getElementById('selectProject');

    var send_btn = document.getElementById('send_data');

    var fld_list = document.getElementsByTagName('fieldset');
    
    var cont_menu = document.getElementsByClassName('context-menu')[0];

    var glob;

    var exprtDsetBtnList = document.getElementsByClassName('context-menu__link');

    document.onmousedown = function(){
      cont_menu.style = 'display: None' 
    }

    var len = fld_list.length;
    for (let i = 0; i<len; i++){
      fld_list[i].addEventListener('dblclick', function(){
        fld_list[i].getElementsByTagName('button')[0].onclick();
      });
      
      fld_list[i].oncontextmenu = function(){return false}

      fld_list[i].addEventListener('contextmenu', function(event){
        let prjName = fld_list[i].getElementsByTagName('legend')[0].textContent.split('Name: ')[1];
        
        let x = event.x;
        let y = event.y;
        cont_menu.style = 'top: '+ 0 +'px; left: '+ 0 +'px; display: block' 
        if (x > window.innerWidth - cont_menu.clientWidth){
          x = window.innerWidth - cont_menu.clientWidth;
        }
        if (y > window.innerHeight - cont_menu.clientHeight){
          y = window.innerHeight - cont_menu.clientHeight;
        }
        cont_menu.style = 'top: '+ y +'px; left: '+ x +'px; display: block' 

        let len = exprtDsetBtnList.length;
        for (let i = 0; i<len; i++){
          exprtDsetBtnList[i].onmousedown = function(){
            let frmt = this.textContent
            let url = '/projects/export_ds/' + prjName + '/' + frmt.toLowerCase();
            document.location = url;
          } 
        }

        return false;
      });
    };
    

      createBasedButton.addEventListener('click', function() {
        favDialog.showModal();
      });


    selectProjectBtn.addEventListener('click', function() {
      if (selectProject.value === ''){
        return 0;
      }
      glob = selectProject.value;
      favDialog2.showModal();
    });


    send_btn.addEventListener('click', function() {
        var formaBase = document.getElementById('baseForm');
        var formData = new FormData(formaBase);
        formData.set('projectBase', glob)


        var xhr = new XMLHttpRequest();
        // xhr.upload.onprogress = function(event){
        //   console.log('Загружено ' + event.loaded + ' из ' + event.total)
        // }
        xhr.open("POST", "/projects/uploadBased", true);
        xhr.send(formData);
      });

  })();