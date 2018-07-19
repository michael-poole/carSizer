// 2-batches.js

var toolbar = { 
	// batch "1" is visible initially
	view:"toolbar", 
	width:500, 
	id:"mybar", 
	visibleBatch:"batch 1", 
	cols:
	[
		{ view:"button", value:"Login", batch:"batch 1", width: 100, align: "left" },
		{ view:"button", value:"Cancel", batch:"batch 1", width: 100, align: "center" },
		{ batch:1 },
		{ view:"button", value:"Register", batch:"batch 1", width: 100, align: "right" },

		{ view:"richselect", batch:"batch 2", label: 'richselect', yCount:"3", value:1, 
		  options:
		  [
			{ id:1, value:"One"   }, 
			{ id:2, value:"Two"   }, 
			{ id:3, value:"Three" }
		  ]		
		},

		{ view:"checkbox", batch:"batch 3", id: "field_a", label:"Do repeat", align:"right", value: 0},
		{ view:"counter", batch: "batch 3", value:100, min: 90, max: 110 }
	]
};

webix.ui
({
	view:"window",
	width:500,
	top:100,
	left:300,
	head:toolbar,
	body:
	{ 
		view:"radio", id:"rad", label: "select", click:"change_batch", 
		options:[ "batch 1","batch 2", "batch 3" ]
	} 
}).show();

function change_batch()
{
	var mode = $$("rad").getValue();
	if(mode) $$("mybar").showBatch(mode);
}