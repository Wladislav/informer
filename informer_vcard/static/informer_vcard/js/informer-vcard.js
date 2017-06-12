require(['dojo/request',
    'dojo/dom',
    'dojo/store/Memory',
    'dojo/data/ObjectStore',
    'dojox/grid/DataGrid',
    'dojox/grid/cells',
    'dojo/date/locale',
    'dojo/date/stamp',
    'dojo/_base/array',
    'dojo/_base/lang',				 
    'dojox/grid/_CheckBoxSelector',
    'dijit/form/CheckBox',
    'dojo/parser',
    'dijit/registry',
    'dijit/layout/ContentPane',
    'dijit/form/Button',
    'dijit/form/DateTextBox',
    'dijit/form/TimeTextBox',
    'dojo/query',
    'dojo/domReady!'],
   function(request, dom, Memory, ObjectStore, Grid, gridCells, DateLocale, DateStamp, baseArray, lang, _CheckBoxSelector, CheckBox, parser){//, registry, query){
       
        //var btCopy, btEdit;
        var grid_adress, grid_phones, grid_email, grid_social, grid_messenger, grid_hobby, grid_interest, grid_expertise;
       
        function get_filed_name(mem_store, field_key) {
            var verbose_name = "";
            if (Object.keys(mem_store.fields_verbose_name).length===0) { return field_key;}
            verbose_item = mem_store.fields_verbose_name;
            if (verbose_item) { verbose_name = verbose_item[field_key]; }
            return verbose_name;
        }       
        function chexboxformater(value){
            if (value == 'True') {
                return '<input type="radio" checked>';
            } else {
                return '<input type="radio">';
            }
        }       
        //ADRESS
        request("vcard_adress.json", { handleAs: "json" }).then(function(data_adress){
            var store_adress = new Memory({ data: data_adress, idProperty: "owner_id" });
            var object_adress_store = new ObjectStore({objectStore: store_adress});
            var cells = [
                [
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_adress,"adress"), field: "adress", width: "25%" },
                    { name: get_filed_name(data_adress,"type"), field: "type", width: "12%" },
                    { name: get_filed_name(data_adress,"geo"), field: "geo", width: "19%", formatter: geoFormatter },
                    { name: get_filed_name(data_adress,"description"), field: "description", width: "15%" },
                    { name: get_filed_name(data_adress,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]
            ];
            //gridLayout = [{
            //	type: "dojox.grid._CheckBoxSelector",
            //	"class": "dojoxGridCell dojoDndItem",
            //},
            //	cells
            //];						
            gridLayout = cells;
            function myStyleRow(row){
               /* The row object has 4 parameters, and you can set two others to provide your own styling
               -- index : the row index
               -- selected: whether or not the row is selected
               -- over : whether or not the mouse is over this row
               -- odd : whether or not this row index is odd. */
               var item = grid_adress.getItem(row.index);
               if(item){
                  var type = object_adress_store.getValue(item, "adress", null);
                  if(!!type){ row.customStyles += "background-color:blue;";  }
               }
               grid_adress.focus.styleRow(row);
               grid_adress.edit.styleRow(row);
            }
            function geoFormatter(value) {	return value.replace(/,/i, ' ');}
            
            grid_adress = new Grid({
                "class": "grid",
                store: object_adress_store,
                query: { owner_id: "*" },
                //onStyleRow: myStyleRow,
                columnReordering: false,
                structure: gridLayout, }, "grid_adress");
            grid_adress.startup();
            //grid_adress.on("RowClick", function(evt){
            //	var idx = evt.rowIndex,
            //			rowData = grid.getItem(idx);
            //	document.getElementById("results").innerHTML =
            //			"You have clicked on " + rowData.last + ", " + rowData.first + ".";
            //}, true);
            
            function reportSelection(node){
                //var items = this.selection.getSelected();
                ////manageButtons(items);
                //var tmp = baseArray.map(items, function(item){
                //	return item.owner_id;
                //}, this);
                //var msg = "You have selected row" + ((tmp.length > 1) ? "s ": " ");
                //node.innerHTML = msg + tmp.join(", ");
            }
           
            grid_adress.on("SelectionChanged",
                    lang.hitch(grid_adress, reportSelection, document.getElementById("results")), true);
       
        }, function(error){ alert(error); });  // END ADRESS

        //PHONES
        request("vcard_phones.json", { handleAs: "json" }).then(function(data_phones){
            var store_phones = new Memory({ data: data_phones, idProperty: "owner_id" });
            var object_phones_store = new ObjectStore({objectStore: store_phones});
            var cells = [[
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_phones,"tel"), field: "tel", width: "15%" },
                    { name: get_filed_name(data_phones,"extension"), field: "extension", width: "10%" },
                    { name: get_filed_name(data_phones,"type"), field: "type", width: "19%" },
                    { name: get_filed_name(data_phones,"description"), field: "description", width: "25%" },
                    { name: get_filed_name(data_phones,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]];
            gridLayout = cells;
            grid_phones = new Grid({
                "class": "grid",
                store: object_phones_store,
                query: { owner_id: "*" },
                columnReordering: false,
                structure: gridLayout, }, "grid_phones");
            grid_phones.startup();
        }, function(error){ alert(error); }); // END PHONES
       
        //EMAIL
        request("vcard_emails.json", { handleAs: "json" }).then(function(data_email){
            var store_email = new Memory({ data: data_email, idProperty: "owner_id" });
            var object_email_store = new ObjectStore({objectStore: store_email});
            var cells = [[
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_email,"email"), field: "email", width: "15%" },
                    { name: get_filed_name(data_email,"type"), field: "type", width: "19%" },
                    { name: get_filed_name(data_email,"description"), field: "description", width: "25%" },
                    { name: get_filed_name(data_email,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]];
            gridLayout = cells;
            grid_email = new Grid({
                "class": "grid",
                store: object_email_store,
                query: { owner_id: "*" },
                columnReordering: false,
                structure: gridLayout, }, "grid_email");
            grid_email.startup();
        }, function(error){ alert(error); }); // END EMAIL
        
        //SOCIAL
        request("vcard_social.json", { handleAs: "json" }).then(function(data_social){
            var store_social = new Memory({ data: data_social, idProperty: "owner_id" });
            var object_social_store = new ObjectStore({objectStore: store_social});
            var cells = [[
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_social,"url"), field: "url", width: "15%" },
                    { name: get_filed_name(data_social,"description"), field: "description", width: "25%" },
                    { name: get_filed_name(data_social,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]];
            gridLayout = cells;
            grid_social = new Grid({
                "class": "grid",
                store: object_social_store,
                query: { owner_id: "*" },
                columnReordering: false,
                structure: gridLayout, }, "grid_social");
            grid_social.startup();
        }, function(error){ alert(error); }); // END SOCIAL
        
       //MESSENGER
        request("vcard_messeng.json", { handleAs: "json" }).then(function(data_messenger){
            var store_messenger = new Memory({ data: data_messenger, idProperty: "owner_id" });
            var object_messenger_store = new ObjectStore({objectStore: store_messenger});
            var cells = [[
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_messenger,"type"), field: "type", width: "15%" },
                    { name: get_filed_name(data_messenger,"identifier"), field: "identifier", width: "25%" },
                    { name: get_filed_name(data_messenger,"description"), field: "description", width: "25%" },
                    { name: get_filed_name(data_messenger,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]];
            gridLayout = cells;
            grid_messenger = new Grid({
                "class": "grid",
                store: object_messenger_store,
                query: { owner_id: "*" },
                columnReordering: false,
                structure: gridLayout, }, "grid_messenger");
            grid_messenger.startup();
        }, function(error){ alert(error); }); // END MESSENGER
        
       //HOBBY
        request("vcard_hobby.json", { handleAs: "json" }).then(function(data_hobby){
            var store_hobby = new Memory({ data: data_hobby, idProperty: "owner_id" });
            var object_hobby_store = new ObjectStore({objectStore: store_hobby});
            var cells = [[
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_hobby,"hobby"), field: "hobby", width: "25%" },
                    { name: get_filed_name(data_hobby,"type"), field: "type", width: "15%" },
                    { name: get_filed_name(data_hobby,"description"), field: "description", width: "25%" },
                    { name: get_filed_name(data_hobby,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]];
            gridLayout = cells;
            grid_hobby = new Grid({
                "class": "grid",
                store: object_hobby_store,
                query: { owner_id: "*" },
                columnReordering: false,
                structure: gridLayout, }, "grid_hobby");
            grid_hobby.startup();
        }, function(error){ alert(error); }); // END HOBBY
       //INTEREST
        request("vcard_interest.json", { handleAs: "json" }).then(function(data_interest){
            var store_interest = new Memory({ data: data_interest, idProperty: "owner_id" });
            var object_interest_store = new ObjectStore({objectStore: store_interest});
            var cells = [[
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_interest,"interest"), field: "interest", width: "25%" },
                    { name: get_filed_name(data_interest,"type"), field: "type", width: "15%" },
                    { name: get_filed_name(data_interest,"description"), field: "description", width: "25%" },
                    { name: get_filed_name(data_interest,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]];
            gridLayout = cells;
            grid_interest = new Grid({
                "class": "grid",
                store: object_interest_store,
                query: { owner_id: "*" },
                columnReordering: false,
                structure: gridLayout, }, "grid_interest");
            grid_interest.startup();
        }, function(error){ alert(error); }); // END INTEREST          
       //EXPERTISE
        request("vcard_expertise.json", { handleAs: "json" }).then(function(data_expertise){
            var store_expertise = new Memory({ data: data_expertise, idProperty: "owner_id" });
            var object_expertise_store = new ObjectStore({objectStore: store_expertise});
            var cells = [[
                    new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                    { name: get_filed_name(data_expertise,"expertise"), field: "expertise", width: "25%" },
                    { name: get_filed_name(data_expertise,"type"), field: "type", width: "15%" },
                    { name: get_filed_name(data_expertise,"description"), field: "description", width: "25%" },
                    { name: get_filed_name(data_expertise,"prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
                ]];
            gridLayout = cells;
            grid_expertise = new Grid({
                "class": "grid",
                store: object_expertise_store,
                query: { owner_id: "*" },
                columnReordering: false,
                structure: gridLayout, }, "grid_expertise");
            grid_expertise.startup();
        }, function(error){ alert(error); }); // END EXPERTISE
        
        //function manageButtons(items){
        //	if (items.length != 1) {
        //		btCopy.set("disabled", true);
        //		btEdit.set("disabled", true);
        //		} else {
        //		btCopy.set("disabled", false);
        //		btEdit.set("disabled", false);
        //		UID = items[0].uid;
        //		}
        //	if (items.length > 0) {
        //		btDelete.set("disabled", false);
        //	} else {
        //		btDelete.set("disabled", true);
        //	}
        //}						
       
        parser.parse(dom.byId('container')).then(function(){
            
            //var tabb_names = query('a[data-toggle="tab"]', dom.byId('container'));
            $('a[data-toggle="tab"]').on('shown.bs.tab', function () {
                if (grid_adress) {grid_adress.render();}
                if (grid_phones) {grid_phones.render();}
                if (grid_email)  {grid_email.render();}
                if (grid_social) {grid_social.render();}
                if (grid_messenger) {grid_messenger.render();}
                if (grid_expertise) {grid_hobby.render();}
                if (grid_hobby) {grid_hobby.render();}
                if (grid_interest) {grid_hobby.render();}
            });
           ////Кнопки
           //btCopy = registry.byId("btCopy");
           //btEdit = registry.byId("btEdit");
           //btDelete = registry.byId("btDelete");
           ////Состояние
           //btCopy.set("disabled", true);
           //btEdit.set("disabled", true);
           //btDelete.set("disabled", true);
           ////События
           //btEdit.on("Click", function(){
           //	document.location.href = '/'+dojoConfig.locale+'/vcards/'+UID+'/change';
           //	});
           //on(dom.byId("vcard_submit"), "click", function(){
           //	var inputs_start = query('input[type=hidden][name|=start]', container);
           //	var inputs_end = query('input[type=hidden][name|=end]', container);
           //	var inputs_bday = query('input[type=hidden][name|=bday]', container);
           //	if (inputs_start[0].value) inputs_start[0].value = inputs_start[0].value+" "+inputs_start[1].value.substring(1);
           //	if (inputs_end[0].value) inputs_end[0].value = inputs_end[0].value+" "+inputs_end[1].value.substring(1);
           //	if (inputs_bday[0].value) inputs_bday[0].value = inputs_bday[0].value+" "+inputs_bday[1].value.substring(1);
           //	});						
       });					
       
});