require(['dojo/request',
    'dojo/dom',
    'dojo/store/Memory',
    'dojo/data/ObjectStore',
    'dojox/grid/DataGrid',
    'dojox/grid/cells',
    'dojox/math/round',
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
   function(request, dom, Memory, ObjectStore, Grid, gridCells, mathRound, DateLocale, DateStamp, baseArray, lang, _CheckBoxSelector, CheckBox, parser){//, registry, query){
       
       //var btCopy, btEdit;
       var grid_adress, grid_phones;
       
       //ADRESS
       request("vcard_adress.json", { handleAs: "json" }).then(function(data_adress){
           var store_adress = new Memory({ data: data_adress, idProperty: "owner_id" });
           var object_adress_store = new ObjectStore({objectStore: store_adress});
           var cells = [
               [
                   new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                   { name: get_filed_name("adress"), field: "adress", width: "25%" },
                   { name: get_filed_name("type"), field: "type", width: "12%" },
                   { name: get_filed_name("geo"), field: "geo", width: "19%", formatter: geoFormatter },
                   { name: get_filed_name("description"), field: "description", width: "15%" },
                   { name: get_filed_name("prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
               ]
           ];
           //gridLayout = [{
           //	type: "dojox.grid._CheckBoxSelector",
           //	"class": "dojoxGridCell dojoDndItem",
           //},
           //	cells
           //];						
           gridLayout = cells;
           function chexboxformater(value){
               if (value == 'True') {
                   return '<input type="radio" checked>';
               } else {
                   return '<input type="radio">';
               }
           }
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
           function get_filed_name(field_key) {
               if (Object.keys(store_adress.data).length===0) { return field_key;}
               verbose_item = store_adress.data[0];
               verbose_name = verbose_item.fields_verbose_name[field_key];
               return verbose_name;
           }
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
           var cells = [
               [
                   new gridCells.RowIndex({ name: "№", width: "3%", styles: 'text-align: center;' }),
                   { name: get_filed_name("tel"), field: "adress", width: "25%" },
                   { name: get_filed_name("extension"), field: "type", width: "12%" },
                   { name: get_filed_name("type"), field: "geo", width: "19%" },
                   { name: get_filed_name("description"), field: "description", width: "15%" },
                   { name: get_filed_name("prefer"), field: "prefer", width: "8%", formatter: chexboxformater, editable: false, cellType: dojox.grid.cells.Bool, styles: 'text-align: center;'}
               ]
           ];
           //gridLayout = [{
           //	type: "dojox.grid._CheckBoxSelector",
           //	"class": "dojoxGridCell dojoDndItem",
           //},
           //	cells
           //];						
           gridLayout = cells;
           function chexboxformater(value){
               if (value == 'True') {
                   return '<input type="radio" checked>';
               } else {
                   return '<input type="radio">';
               }
           }
           function myStyleRow(row){
              /* The row object has 4 parameters, and you can set two others to provide your own styling
              -- index : the row index
              -- selected: whether or not the row is selected
              -- over : whether or not the mouse is over this row
              -- odd : whether or not this row index is odd. */
              var item = grid_phones.getItem(row.index);
              if(item){
                 var type = object_phones_store.getValue(item, "adress", null);
                 if(!!type){ row.customStyles += "background-color:blue;";  }
              }
              grid_phones.focus.styleRow(row);
              grid_phones.edit.styleRow(row);
           }

           function get_filed_name(field_key) {
               var verbose_name = "";
               if (Object.keys(store_phones.data).length===0) { return field_key;}
               verbose_item = store_phones.data[0];
               if (verbose_item) { verbose_name = verbose_item.fields_verbose_name[field_key]; }
               return verbose_name;
           }
           grid_phones = new Grid({
               "class": "grid",
               store: object_phones_store,
               query: { owner_id: "*" },
               columnReordering: false,
               structure: gridLayout, }, "grid_phones");
           grid_phones.startup();

           function reportSelection(node){
               //var items = this.selection.getSelected();
               ////manageButtons(items);
               //var tmp = baseArray.map(items, function(item){
               //	return item.owner_id;
               //}, this);
               //var msg = "You have selected row" + ((tmp.length > 1) ? "s ": " ");
               //node.innerHTML = msg + tmp.join(", ");
           }
           
           grid_phones.on("SelectionChanged",
                   lang.hitch(grid_phones, reportSelection, document.getElementById("results")), true);
       
       }, function(error){ alert(error); }); // END PHONES
       
       
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
               grid_adress.render();
               grid_phones.render();
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