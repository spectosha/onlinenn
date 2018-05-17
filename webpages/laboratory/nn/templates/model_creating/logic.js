function init() {
	var $ = go.GraphObject.make;  // for conciseness in defining templates

	myDiagram = $(go.Diagram, "myDiagramDiv",  // must name or refer to the DIV HTML element
	{
		initialContentAlignment: go.Spot.Center,
		allowDrop: true,  // must be true to accept drops from the Palette
		"LinkDrawn": showLinkLabel,  // this DiagramEvent listener is defined below
		"LinkRelinked": showLinkLabel,
		scrollsPageOnFocus: false,
		"undoManager.isEnabled": true,
        scale:0.7
	});

	// when the document is modified, add a "*" to the title and enable the "Save" button
	myDiagram.addDiagramListener("Modified", function(e) {
		var button = document.getElementById("SaveButton");
		if (button) button.disabled = !myDiagram.isModified;
		var idx = document.title.indexOf("*");
		if (myDiagram.isModified) {
			if (idx < 0) document.title += "*";
		} else 
			if (idx >= 0) document.title = document.title.substr(0, idx);
		}
	);
    
    
   

	// helper definitions for node templates

	function nodeStyle() {
		return [
			new go.Binding("location", "loc", go.Point.parse).makeTwoWay(go.Point.stringify),
			{
				locationSpot: go.Spot.Center,
				mouseEnter: function (e, obj) { showPorts(obj.part, true); },
				mouseLeave: function (e, obj) { showPorts(obj.part, false); }
			}
		];
	}

	function makePort(name, spot, output, input) {
		return $(go.Shape, "Circle",
			{
				fill: 'transparent',
				stroke: null,  
				desiredSize: new go.Size(8, 8),
				alignment: spot, alignmentFocus: spot,  
				portId: name,  
				fromSpot: spot, toSpot: spot,  
				fromLinkable: output, toLinkable: input,  
				cursor: "pointer"  
			}
		);
	}
	
	var fieldTemplate = $(go.Panel, "TableRow",
		$(go.TextBlock,
		{ 
			margin: new go.Margin(3, 15), 
			column: 1, 
			font: "bold 13px sans-serif",
			alignment: go.Spot.Left
		},
		new go.Binding("text", "name")),
		$(go.TextBlock,
		{ 
			margin: new go.Margin(0, 15),
			stroke: 'black',
			column: 2, 
			font: "13px sans-serif",
			editable: true 
		},
		new go.Binding("text", "value").makeTwoWay()
		)
	);
	
	var lightText = 'whitesmoke';

	var font = { font: "bold 11pt Helvetica, Arial, sans-serif", stroke: 'whitesmoke' }


	myDiagram.nodeTemplateMap.add("",  // the default category
		$(go.Node, "Auto", nodeStyle(),
			$(go.Shape, { fill: "#EEEEEE"}),
			$(go.Panel, "Vertical",
				$(go.Panel, "Auto",
					{ stretch: go.GraphObject.Horizontal }, //На всю ширину
					$(go.Shape, 
						{ fill: "#1570A6", stroke: null }, 
						new go.Binding("fill", "color")), //Заполняем
					$(go.TextBlock,
						{
							alignment: go.Spot.Center,
							margin: 9,
							stroke: "white",
							textAlign: "center",
							font: "bold 10pt sans-serif"
						},
						new go.Binding("text", "type")
					)
				),
				$(go.Panel, "Auto",
					{ stretch: go.GraphObject.Horizontal }, //На всю ширину
					$(go.Shape, { fill: "#6E6E6E", stroke: null}), //Заполняем
					$(go.TextBlock,
						{
							alignment: go.Spot.Center,
							margin: 3,
							stroke: "white",
							textAlign: "center",
							font: "bold 9pt sans-serif",
							wrap: go.TextBlock.WrapFit,
							editable: true
						},
						new go.Binding("text", "name").makeTwoWay()
					)
				),
				$(go.Panel, "Table",
					{

						defaultStretch: go.GraphObject.Horizontal,
						itemTemplate: fieldTemplate,
						minSize: new go.Size(200, 0)
					},
					new go.Binding("itemArray", "fields").makeTwoWay()
				) 
			),
			makePort("T", go.Spot.Top, true, true),
			makePort("L", go.Spot.Left, true, true),
			makePort("R", go.Spot.Right, true, true),
			makePort("B", go.Spot.Bottom, true, true),
		),
	);

    	myDiagram.nodeTemplateMap.add("Setting",  // the default category
		$(go.Node, "Auto", nodeStyle(),
			$(go.Shape, { fill: "#EEEEEE"}),
			$(go.Panel, "Vertical",
				$(go.Panel, "Auto",
					{ stretch: go.GraphObject.Horizontal }, //На всю ширину
					$(go.Shape, 
						{ fill: "#1570A6", stroke: null }, 
						new go.Binding("fill", "color")), //Заполняем
					$(go.TextBlock,
						{
							alignment: go.Spot.Center,
							margin: 9,
							stroke: "white",
							textAlign: "center",
							font: "bold 10pt sans-serif"
						},
						new go.Binding("text", "name")
					)
				),
				$(go.Panel, "Table",
					{

						defaultStretch: go.GraphObject.Horizontal,
						itemTemplate: fieldTemplate,
						minSize: new go.Size(200, 0)
					},
					new go.Binding("itemArray", "fields").makeTwoWay()
				) 
			)
		)
	);
	
	myDiagram.nodeTemplateMap.add("End",
		$(go.Node, "Spot", nodeStyle(),
			$(go.Panel, "Auto",
				$(go.Shape, "Border",
					{ minSize: new go.Size(120, 50), fill: "#DC3C00", stroke: null }
				 ),
				$(go.TextBlock, "End",
					{ font: "bold 11pt Helvetica, Arial, sans-serif", stroke: lightText },
					new go.Binding("text")
				 )
			),
			// three named ports, one on each side except the bottom, all input only:
			makePort("T", go.Spot.Top, false, true),
			makePort("L", go.Spot.Left, false, true),
			makePort("R", go.Spot.Right, false, true)
		)
	);

	myDiagram.nodeTemplateMap.add("Comment",
		$(go.Node, "Auto", nodeStyle(),
		$(go.Shape, "File",
		{ fill: "#CAC5E2", stroke: null }),
		$(go.TextBlock,
		{
			margin: 5,
			maxSize: new go.Size(300, NaN),
			wrap: go.TextBlock.WrapFit,
			textAlign: "center",
			editable: true,
			font: "bold 12pt Helvetica, Arial, sans-serif",
			stroke: '#303030'
		},
		new go.Binding("text").makeTwoWay())
	));


	// replace the default Link template in the linkTemplateMap
	myDiagram.linkTemplate =
		$(go.Link,  // the whole link panel
			{
				routing: go.Link.AvoidsNodes,
				curve: go.Link.JumpOver,
				corner: 5, toShortLength: 4,
				relinkableFrom: true,
				relinkableTo: true,
				reshapable: true,
				resegmentable: true,
				// mouse-overs subtly highlight links:
				mouseEnter: function(e, link) { link.findObject("HIGHLIGHT").stroke = "rgba(30,144,255,0.2)"; },
				mouseLeave: function(e, link) { link.findObject("HIGHLIGHT").stroke = "transparent"; }
			},
			new go.Binding("points").makeTwoWay(),
			$(go.Shape,  // the highlight shape, normally transparent
				{ isPanelMain: true, strokeWidth: 8, stroke: "transparent", name: "HIGHLIGHT" }),
			$(go.Shape,  // the link path shape
				{ isPanelMain: true, stroke: "gray", strokeWidth: 2 }),
			$(go.Shape,  // the arrowhead
				{ toArrow: "standard", stroke: null, fill: "gray"}),
			$(go.Panel, "Auto",  // the link label, normally not visible
				{ visible: false, name: "LABEL", segmentIndex: 2, segmentFraction: 0.5},
				new go.Binding("visible", "visible").makeTwoWay(),
				$(go.Shape, "RoundedRectangle",  // the label shape
					{ fill: "#F8F8F8", stroke: null }),
				$(go.TextBlock, "Yes",  // the label
					{
						textAlign: "center",
						font: "10pt helvetica, arial, sans-serif",
						stroke: "#333333",
						editable: true
					},
				new go.Binding("text").makeTwoWay())
			)
		);

	function showLinkLabel(e) {
	var label = e.subject.findObject("LABEL");
	if (label !== null) label.visible = (e.subject.fromNode.data.figure === "Diamond");
	}

	myDiagram.toolManager.linkingTool.temporaryLink.routing = go.Link.Orthogonal;
	myDiagram.toolManager.relinkingTool.temporaryLink.routing = go.Link.Orthogonal;

	load();  // load an initial diagram from some JSON text


	jQuery("#accordion").accordion({
		activate: function(event, ui) {
			Settings.requestUpdate();
            Optimizers.requestUpdate();
			Core.requestUpdate();
			Convolutional.requestUpdate();
			Pooling.requestUpdate();
			Locally.requestUpdate();
			Merge.requestUpdate();
			Normalization.requestUpdate();
			Noise.requestUpdate();
		}
    });

	Settings = $(go.Palette, "Settings",
        {
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
          minScale: 0.8,
          maxScale: 0.8,
          scale: 0.8

        });
		Settings.model = new go.GraphLinksModel([
			{ category: "Comment", type: "Comment", text: "Comment" },
            { category: "Setting", type: "Setting", name: "Setting", color: "#7D72B1",
				fields: [
							{ name: "loss", value: "mean_squared_error"},
                            { name: "epochs", value: "1"}
						] 
            }
		])
    
    Optimizers = $(go.Palette, "Optimizers",
        {
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
          minScale: 0.8,
          maxScale: 0.8,
          scale: 0.8

        });
		Optimizers.model = new go.GraphLinksModel([
			{ category: "Setting", type: "Optimizer", name: "SGD", color: "#82264F",
				fields: [
							{ name: "lr", value: "0.01"},
                            { name: "momentum", value: "0.0"},
                            { name: "decay", value: "0.0"}
						] 
            },
            { category: "Setting", type: "Optimizer", name: "RMSprop", color: "#82264F",
				fields: [
							{ name: "lr", value: "0.001"},
							{ name: "rho", value: "0.9"},
							{ name: "epsilon", value: "None"},
							{ name: "decay", value: "0.0"}
						] 
            },
            { category: "Setting", type: "Optimizer", name: "Adagrad", color: "#82264F",
				fields: [
							{ name: "lr", value: "0.01"},
							{ name: "epsilon", value: "None"},
							{ name: "decay", value: "0.0"}
						] 
            },
            { category: "Setting", type: "Optimizer", name: "Adadelta", color: "#82264F",
				fields: [
							{ name: "lr", value: "1.0"},
							{ name: "rho", value: "0.95"},
							{ name: "epsilon", value: "None"},
							{ name: "decay", value: "0.0"}
						] 
            },
            { category: "Setting", type: "Optimizer", name: "Adam", color: "#82264F",
				fields: [
							{ name: "lr", value: "0.001"},
							{ name: "beta_1", value: "0.9"},
							{ name: "beta_2", value: "0.999"},
							{ name: "epsilon", value: "None"},
							{ name: "decay", value: "0.0"},
							{ name: "amsgrad", value: "False"}
						] 
            },
            { category: "Setting", type: "Optimizer", name: "Adamax", color: "#82264F",
				fields: [
							{ name: "lr", value: "0.002"},
							{ name: "beta_1", value: "0.9"},
							{ name: "beta_2", value: "0.999"},
							{ name: "epsilon", value: "None"},
							{ name: "decay", value: "0.0"}
						] 
            }
		])
	
    myDiagram.mouseDrop = function(e) {
        //Реализовать функцию непозволяющую ставить два оптимизатора или loss
        /*
      if (AllowTopLevel) {
        if (!e.diagram.commandHandler.addTopLevelParts(e.diagram.selection, true)) {
          e.diagram.currentTool.doCancel();
        }
      } else {
        if (!e.diagram.selection.all(function(p) { return p instanceof go.Group; })) {
          e.diagram.currentTool.doCancel();
        }
      }
      */
    };
    
	Core = $(go.Palette, "Core",
        { 
			nodeTemplateMap: myDiagram.nodeTemplateMap,
			layout: $(go.GridLayout),
            minScale: 0.8,
            maxScale: 0.8,
            scale: 0.8
        });
	
		Core.model = new go.GraphLinksModel([
			{ type: "Input", name: "Give me a name", color: "#179738",
				fields: [
							{ name: "shape", value: "32"}
						]
			},
			{ category: "End", type: "End"},
			{ type: "Dense", name: "Give me a name", color: "#8595B2",
				fields: [
							{ name: "units", value: "128"},
							{ name: "activation", value: "relu"}
						]
			},
			{ type: "Dropout", name: "Give me a name", color: "#2F3D56",
				fields: [
							{ name: "rate", value: "0.25"}
						]
			},
			{ type: "Flatten", name: "Give me a name", color: "#5C85DB"},
			{ type: "Reshape", name: "Give me a name", color: "#5D5CDB",
				fields: [
							{ name: "target_shape", value: "128"}
						]
			},
			{ type: "Permute", name: "Give me a name", color: "#8F5CDB",
				fields: [
							{ name: "dims", value: "2,1"}
						]
			},
			{ type: "RepeatVector", name: "Give me a name", color: "#6C568A",
				fields: [
							{ name: "n", value: "2"}
						]
			}
		])
	
	Convolutional = $(go.Palette, "Convolutional",
        { 
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
          minScale: 0.8,
          maxScale: 0.8,
          scale: 0.8
        });
	
		Convolutional.model = new go.GraphLinksModel([
			{ type: "Conv1D", name: "Give me a name", color: "#538D60",
				fields: [
							{ name: "filters", value: "32"},
							{ name: "kernel_size", value: "3"},
							{ name: "activation", value: "relu"},
							{ name: "strides", value: "1"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "Conv2D", name: "Give me a name", color: "#4A7352",
				fields: [
							{ name: "filters", value: "32"},
							{ name: "kernel_size", value: "3,3"},
							{ name: "activation", value: "relu"},
							{ name: "strides", value: "1,1"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "Conv2DTranspose", name: "Give me a name", color: "#0071B8",
				fields: [
							{ name: "filters", value: "32"},
							{ name: "kernel_size", value: "3,3"},
							{ name: "activation", value: "relu"},
							{ name: "strides", value: "1,1"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "Conv3D", name: "Give me a name", color: "#345B3C",
				fields: [
							{ name: "filters", value: "32"},
							{ name: "kernel_size", value: "3,3,3"},
							{ name: "activation", value: "relu"},
							{ name: "strides", value: "1,1,1"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "Cropping1D", name: "Give me a name", color: "#88996C",
				fields: [
							{ name: "cropping", value: "1,1"}
						]
			},
			{ type: "Cropping2D", name: "Give me a name", color: "#7D8B5B",
				fields: [
							{ name: "cropping", value: "(0,0),(0,0)"}
						]
			},
			{ type: "Cropping3D", name: "Give me a name", color: "#707C46",
				fields: [
							{ name: "cropping", value: "(1,1),(1,1),(1,1)"}
						]
			},
			{ type: "UpSampling1D", name: "Give me a name", color: "#AA8D9A",
				fields: [
							{ name: "size", value: "2"}
						]
			},
			{ type: "UpSampling2D", name: "Give me a name", color: "#764C5F",
				fields: [
							{ name: "size", value: "2,2"}
						]
			},
			{ type: "UpSampling3D", name: "Give me a name", color: "#58324A",
				fields: [
							{ name: "size", value: "2,2,2"}
						]
			}
		])

	Pooling = $(go.Palette, "Pooling",
        { 
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
          minScale: 0.8,
          maxScale: 0.8,
          scale: 0.8
        });
	
		Pooling.model = new go.GraphLinksModel([
			{ type: "MaxPooling1D", name: "Give me a name", color: "#856BC7",
				fields: [
							{ name: "pool_size", value: "2"},
							{ name: "strides", value: "None"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "MaxPooling2D", name: "Give me a name", color: "#7A49A7",
				fields: [
							{ name: "pool_size", value: "2,2"},
							{ name: "strides", value: "None"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "MaxPooling3D", name: "Give me a name", color: "#5E426C",
				fields: [
							{ name: "pool_size", value: "2,2,2"},
							{ name: "strides", value: "None"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "AveragePooling1D", name: "Give me a name", color: "#8DA6C4",
				fields: [
							{ name: "pool_size", value: "2"},
							{ name: "strides", value: "None"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "AveragePooling2D", name: "Give me a name", color: "#5C7A9D",
				fields: [
							{ name: "pool_size", value: "2,2"},
							{ name: "strides", value: "None"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "AveragePooling3D", name: "Give me a name", color: "#455C78",
				fields: [
							{ name: "pool_size", value: "2,2,2"},
							{ name: "strides", value: "None"},
							{ name: "padding", value: "valid"}
						]
			},
			{ type: "GlobalMaxPooling1D", name: "Give me a name", color: "#AA8455"},
			{ type: "GlobalAveragePooling1D", name: "Give me a name", color: "#C94A54"},
			{ type: "GlobalMaxPooling2D", name: "Give me a name", color: "#785F3F"},
			{ type: "GlobalAveragePooling2D", name: "Give me a name", color: "#782B31"}
		])
	
	Locally = $(go.Palette, "Locally-connected",
        { 
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
            minScale: 0.8,
            maxScale: 0.8,
            scale: 0.8
        });
	
		Locally.model = new go.GraphLinksModel([
			{ type: "LocallyConnected1D", name: "Give me a name", color: "#F6AB37",
				fields: [
							{ name: "filters", value: "32"},
							{ name: "kernel_size", value: "3"},
							{ name: "strides", value: "1"},
							{ name: "padding", value: "valid"},
							{ name: "activation", value: "relu"}
						]
			},
			{ type: "LocallyConnected2D", name: "Give me a name", color: "#B89051",
				fields: [
							{ name: "filters", value: "32"},
							{ name: "kernel_size", value: "3,3"},
							{ name: "strides", value: "1,1"},
							{ name: "padding", value: "valid"},
							{ name: "activation", value: "relu"}
						]
			}
		])
	
	Merge = $(go.Palette, "Merge",
        { 
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
          minScale: 0.8,
          maxScale: 0.8,
          scale: 0.8
        });
	
		Merge.model = new go.GraphLinksModel([
			{ type: "Add", name: "Give me a name", color: "#7D9673"},
			{ type: "Subtract", name: "Give me a name", color: "#7D9673"},
			{ type: "Multiply", name: "Give me a name", color: "#7D9673"},
			{ type: "Average", name: "Give me a name", color: "#7D9673"},
			{ type: "Maximum", name: "Give me a name", color: "#7D9673"},
			{ type: "Concatenate", name: "Give me a name", color: "#7D9673"},
			{ type: "Dot", name: "Give me a name", color: "#7D9673"}
		])
	
	Normalization = $(go.Palette, "Normalization",
        { 
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
          minScale: 0.8,
          maxScale: 0.8,
          scale: 0.8
        });
	
		Normalization.model = new go.GraphLinksModel([
			{ type: "BatchNormalization", name: "Give me a name", color: "#148A79",
				fields: [
							{ name: "axis", value: "-1"},
							{ name: "momentum", value: "0.99"},
							{ name: "epsilon", value: "0.001"},
							{ name: "center", value: "True"},
							{ name: "scale", value: "True"}
						]
			}
		])
	
	Noise = $(go.Palette, "Noise",
        { 
          nodeTemplateMap: myDiagram.nodeTemplateMap,
          layout: $(go.GridLayout),
          minScale: 0.8,
          maxScale: 0.8,
          scale: 0.8
        });
	
		Noise.model = new go.GraphLinksModel([
			{ type: "GaussianNoise", name: "Give me a name", color: "#927A99",
				fields: [
							{ name: "stddev", value: "NaN"}
						]
			},
			{ type: "GaussianDropout", name: "Give me a name", color: "#927A99",
				fields: [
							{ name: "rate", value: "NaN"}
						]
			},
			{ type: "AlphaDropout", name: "Give me a name", color: "#927A99",
				fields: [
							{ name: "rate", value: "NaN"},
							{ name: "seed", value: "1"}
						]
			}
		])
} // end init


// Make all ports on a node visible when the mouse is over the node
function showPorts(node, show) {
var diagram = node.diagram;
if (!diagram || diagram.isReadOnly || !diagram.allowLink) return;
node.ports.each(
function(port) {
port.stroke = (show ? "black" : null);
}
);
}


// Show the diagram's model in JSON format that the user may edit
function save() {
document.getElementById("mySavedModel").value = myDiagram.model.toJson();
myDiagram.isModified = false;
}
function load() {
myDiagram.model = go.Model.fromJson(document.getElementById("mySavedModel").value);
}

// add an SVG rendering of the diagram at the end of this page
function makeSVG() {
var svg = myDiagram.makeSvg({
scale: 0.5
});
svg.style.border = "1px solid black";
obj = document.getElementById("SVGArea");
obj.appendChild(svg);
if (obj.children.length > 0) {
obj.replaceChild(svg, obj.children[0]);
}
}