import PartDesignGui
import Show
import Mesh

Gui.runCommand('Start_Start',0)
Gui.runCommand('Std_Workbench',10) # select workbench part design
Gui.runCommand('Std_ViewStatusBar',1)

### Create new file
App.newDocument()

App.setActiveDocument("Unnamed")
App.ActiveDocument=App.getDocument("Unnamed")
Gui.ActiveDocument=Gui.getDocument("Unnamed")
Gui.activeDocument().activeView().viewDefaultOrientation()
### End of file creation

### Set orthographic view
Gui.runCommand('Std_OrthographicCamera',1)


### Create PartDesign_body
App.activeDocument().addObject('PartDesign::Body','Body')
App.ActiveDocument.getObject('Body').Label = 'Body'

Gui.activateView('Gui::View3DInventor', True)
Gui.activeView().setActiveObject('pdbody', App.activeDocument().Body)
Gui.Selection.clearSelection()
Gui.Selection.addSelection(App.ActiveDocument.Body)
App.ActiveDocument.recompute()
### End command PartDesign_body


### Enabling origin visibility (Planes: XY, XZ & YZ)
Gui.Selection.addSelection('Unnamed','Body')
Gui.Selection.clearSelection()
Gui.Selection.addSelection('Unnamed','Body','Origin.')


### Selecting XY plane
Gui.Selection.addSelection('Unnamed','Body','Origin.XY_Plane.')

### Setting the window for sketch generation
App.getDocument('Unnamed').getObject('Body').newObject('Sketcher::SketchObject','Sketch')
App.getDocument('Unnamed').getObject('Sketch').AttachmentSupport = (App.getDocument('Unnamed').getObject('XY_Plane'),[''])
App.getDocument('Unnamed').getObject('Sketch').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

Gui.getDocument('Unnamed').setEdit(App.getDocument('Unnamed').getObject('Body'), 0, 'Sketch.')


ActiveSketch = App.getDocument('Unnamed').getObject('Sketch')
tv = Show.TempoVis(App.ActiveDocument, tag= ActiveSketch.ViewObject.TypeId)
ActiveSketch.ViewObject.TempoVis = tv
if ActiveSketch.ViewObject.EditingWorkbench:
    tv.activateWorkbench(ActiveSketch.ViewObject.EditingWorkbench)

if ActiveSketch.ViewObject.HideDependent:
    tv.hide(tv.get_all_dependent(App.getDocument('Unnamed').getObject('Body'), 'Sketch.'))

if ActiveSketch.ViewObject.ShowSupport:
    tv.show([ref[0] for ref in ActiveSketch.AttachmentSupport if not ref[0].isDerivedFrom("PartDesign::Plane")])

if ActiveSketch.ViewObject.ShowLinks:
    tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])

tv.sketchClipPlane(ActiveSketch, ActiveSketch.ViewObject.SectionView) # check the indendation
tv.hide(ActiveSketch) # check the indendation
del(tv) # check the indendation
del(ActiveSketch) # check the indendation



ActiveSketch = App.getDocument('Unnamed').getObject('Sketch')

if ActiveSketch.ViewObject.RestoreCamera:
    ActiveSketch.ViewObject.TempoVis.saveCamera()
    
    if ActiveSketch.ViewObject.ForceOrtho:
        ActiveSketch.ViewObject.Document.ActiveView.setCameraType('Orthographic')

Gui.Selection.clearSelection()  # check the indendation



### Create rectangle
Gui.runCommand('Sketcher_CompCreateRectangles',1)
ActiveSketch = App.getDocument('Unnamed').getObject('Sketch')
lastGeoId = len(ActiveSketch.Geometry)
 
geoList = []
geoList.append(Part.LineSegment(App.Vector(-25.139629, 18.901154, 0.000000),App.Vector(-25.139629, -18.901154, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(-25.139629, -18.901154, 0.000000),App.Vector(25.139629, -18.901154, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(25.139629, -18.901154, 0.000000),App.Vector(25.139629, 18.901154, 0.000000)))
geoList.append(Part.LineSegment(App.Vector(25.139629, 18.901154, 0.000000),App.Vector(-25.139629, 18.901154, 0.000000)))

App.getDocument('Unnamed').getObject('Sketch').addGeometry(geoList,False)
del geoList

constrGeoList = []
constrGeoList.append(Part.Point(App.Vector(0.000000, 0.000000, 0.000000)))
App.getDocument('Unnamed').getObject('Sketch').addGeometry(constrGeoList,True)
del constrGeoList

constraintList = []
constraintList.append(Sketcher.Constraint('Coincident', 0, 2, 1, 1))
constraintList.append(Sketcher.Constraint('Coincident', 1, 2, 2, 1))
constraintList.append(Sketcher.Constraint('Coincident', 2, 2, 3, 1))
constraintList.append(Sketcher.Constraint('Coincident', 3, 2, 0, 1))
constraintList.append(Sketcher.Constraint('Vertical', 0))
constraintList.append(Sketcher.Constraint('Vertical', 2))
constraintList.append(Sketcher.Constraint('Horizontal', 1))
constraintList.append(Sketcher.Constraint('Horizontal', 3))
constraintList.append(Sketcher.Constraint('Symmetric', 2, 1, 0, 1, 4, 1))
App.getDocument('Unnamed').getObject('Sketch').addConstraint(constraintList)
del constraintList

App.getDocument('Unnamed').getObject('Sketch').addConstraint(Sketcher.Constraint('Coincident', 4, 1, -1, 1))


### Select dimension tool
Gui.runCommand('Sketcher_CompDimensionTools',0)



### Dimension the sketch

# Avoid Gui.Selection
# Causes access violation when selection is invalid

sketch = App.getDocument('Unnamed').getObject('Sketch')

# Ensure you're in edit mode
Gui.getDocument('Unnamed').setEdit(sketch)

# Add horizontal constraint to edge 3 (index 3 = top edge)
sketch.addConstraint(Sketcher.Constraint('DistanceX', 3, 2, 3, 1, 50.0))

# Add vertical constraint to edge 2 (index 2 = right edge)
sketch.addConstraint(Sketcher.Constraint('DistanceY', 2, 1, 2, 2, 30.0))

# Recompute
App.ActiveDocument.recompute()

# Exit sketch
Gui.getDocument('Unnamed').resetEdit()

# Select sketch in the model tree
Gui.Selection.clearSelection()
Gui.Selection.addSelection('Unnamed','Body','Sketch.')


### Begin command PartDesign_Pad
App.getDocument('Unnamed').getObject('Body').newObject('PartDesign::Pad','Pad')
App.getDocument('Unnamed').getObject('Pad').Profile = (App.getDocument('Unnamed').getObject('Sketch'), ['',])
App.getDocument('Unnamed').getObject('Pad').Length = 10
App.ActiveDocument.recompute()
App.getDocument('Unnamed').getObject('Pad').ReferenceAxis = (App.getDocument('Unnamed').getObject('Sketch'),['N_Axis'])
App.getDocument('Unnamed').getObject('Sketch').Visibility = False
App.ActiveDocument.recompute()

App.getDocument('Unnamed').getObject('Pad').ViewObject.ShapeAppearance=getattr(App.getDocument('Unnamed').getObject('Body').getLinkedObject(True).ViewObject,'ShapeAppearance',App.getDocument('Unnamed').getObject('Pad').ViewObject.ShapeAppearance)
App.getDocument('Unnamed').getObject('Pad').ViewObject.LineColor=getattr(App.getDocument('Unnamed').getObject('Body').getLinkedObject(True).ViewObject,'LineColor',App.getDocument('Unnamed').getObject('Pad').ViewObject.LineColor)
App.getDocument('Unnamed').getObject('Pad').ViewObject.PointColor=getattr(App.getDocument('Unnamed').getObject('Body').getLinkedObject(True).ViewObject,'PointColor',App.getDocument('Unnamed').getObject('Pad').ViewObject.PointColor)
App.getDocument('Unnamed').getObject('Pad').ViewObject.Transparency=getattr(App.getDocument('Unnamed').getObject('Body').getLinkedObject(True).ViewObject,'Transparency',App.getDocument('Unnamed').getObject('Pad').ViewObject.Transparency)
App.getDocument('Unnamed').getObject('Pad').ViewObject.DisplayMode=getattr(App.getDocument('Unnamed').getObject('Body').getLinkedObject(True).ViewObject,'DisplayMode',App.getDocument('Unnamed').getObject('Pad').ViewObject.DisplayMode)
Gui.getDocument('Unnamed').setEdit(App.getDocument('Unnamed').getObject('Body'), 0, 'Pad.')
Gui.Selection.clearSelection()

### End command PartDesign_Pad
Gui.Selection.clearSelection()
App.getDocument('Unnamed').getObject('Pad').Length = 50.000000
App.getDocument('Unnamed').getObject('Pad').TaperAngle = 0.000000
App.getDocument('Unnamed').getObject('Pad').UseCustomVector = 0
App.getDocument('Unnamed').getObject('Pad').Direction = (0, 0, 1)
App.getDocument('Unnamed').getObject('Pad').ReferenceAxis = (App.getDocument('Unnamed').getObject('Sketch'), ['N_Axis'])
App.getDocument('Unnamed').getObject('Pad').AlongSketchNormal = 1
App.getDocument('Unnamed').getObject('Pad').Type = 0
App.getDocument('Unnamed').getObject('Pad').UpToFace = None
App.getDocument('Unnamed').getObject('Pad').Reversed = 0
App.getDocument('Unnamed').getObject('Pad').Midplane = 0
App.getDocument('Unnamed').getObject('Pad').Offset = 0
App.getDocument('Unnamed').recompute()
Gui.getDocument('Unnamed').resetEdit()
App.getDocument('Unnamed').getObject('Sketch').Visibility = False


### selecting the top face

Gui.Selection.addSelection('Unnamed','Body','Pad.Face6',10.6145,7.35568,50)



### create new sketch

Gui.runCommand('PartDesign_NewSketch',0)

App.getDocument('Unnamed').getObject('Body').newObject('Sketcher::SketchObject','Sketch001')
App.getDocument('Unnamed').getObject('Sketch001').AttachmentSupport = (App.getDocument('Unnamed').getObject('Pad'),['Face6',])
App.getDocument('Unnamed').getObject('Sketch001').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

Gui.getDocument('Unnamed').setEdit(App.getDocument('Unnamed').getObject('Body'), 0, 'Sketch001.')
ActiveSketch = App.getDocument('Unnamed').getObject('Sketch001')
tv = Show.TempoVis(App.ActiveDocument, tag= ActiveSketch.ViewObject.TypeId)
ActiveSketch.ViewObject.TempoVis = tv
if ActiveSketch.ViewObject.EditingWorkbench:
    tv.activateWorkbench(ActiveSketch.ViewObject.EditingWorkbench)

if ActiveSketch.ViewObject.HideDependent:
    tv.hide(tv.get_all_dependent(App.getDocument('Unnamed').getObject('Body'), 'Sketch001.'))

if ActiveSketch.ViewObject.ShowSupport:
    tv.show([ref[0] for ref in ActiveSketch.AttachmentSupport if not ref[0].isDerivedFrom("PartDesign::Plane")])

if ActiveSketch.ViewObject.ShowLinks:
    tv.show([ref[0] for ref in ActiveSketch.ExternalGeometry])

tv.sketchClipPlane(ActiveSketch, ActiveSketch.ViewObject.SectionView)
tv.hide(ActiveSketch)
del(tv)
del(ActiveSketch)



ActiveSketch = App.getDocument('Unnamed').getObject('Sketch001')
if ActiveSketch.ViewObject.RestoreCamera:
    ActiveSketch.ViewObject.TempoVis.saveCamera()

if ActiveSketch.ViewObject.ForceOrtho:
    ActiveSketch.ViewObject.Document.ActiveView.setCameraType('Orthographic')

Gui.Selection.clearSelection()


# Create the sketch on Pad.Face6 


doc = App.getDocument('Unnamed')

# Optional cleanup: remove previous empty sketches (if needed)
for obj in doc.Objects:
    if obj.TypeId == 'Sketcher::SketchObject' and len(obj.Geometry) == 0:
        doc.removeObject(obj.Name)

# Create sketch on top face (Face6 of Pad)
body = doc.getObject('Body')
sketch = body.newObject('Sketcher::SketchObject', 'Sketch_Circle')
sketch.AttachmentSupport = (doc.getObject('Pad'), ['Face6'])
sketch.MapMode = 'FlatFace'

# Add circle at origin
circle = Part.Circle(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 10)
sketch.addGeometry(circle, False)

# Add constraints
sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))  # center to origin
sketch.addConstraint(Sketcher.Constraint('Diameter', 0, 20.0))       # diameter 20 mm

# Recompute document
doc.recompute()



### create cylindrical pocket
doc = App.getDocument('Unnamed')
body = doc.getObject('Body')
sketch = doc.getObject('Sketch_Circle')  # make sure this is your circle sketch

# Create the pocket feature
pocket = body.newObject('PartDesign::Pocket', 'Pocket')
pocket.Profile = (sketch, [''])
pocket.Type = 1  # 1 = Through all
pocket.Reversed = False
pocket.Midplane = False
pocket.UseCustomVector = False

# Final recompute
doc.recompute()

# Optional: Hide sketch for cleanliness
sketch.Visibility = False


### Isometric view
Gui.activeDocument().activeView().viewIsometric()
Gui.SendMsgToActiveView("ViewFit")




### Add fillet to multiple edges 

doc = App.getDocument("Unnamed")
body = doc.getObject("Body")
pocket = doc.getObject("Pocket")

# Create Fillet feature
fillet = body.newObject("PartDesign::Fillet", "Fillet")
fillet.Base = (pocket, [
    "Edge8", "Edge2", "Edge5", "Edge1",
    "Edge10", "Edge13", "Edge7", "Edge4",
    "Edge9", "Edge11", "Edge6", "Edge3"
])
fillet.Radius = 1.0

# Hide Pocket
pocket.ViewObject.Visibility = False

# Recompute to apply fillet
doc.recompute()



### Adding chamfer

# Access document and objects
doc = App.getDocument("Unnamed")
body = doc.getObject("Body")
fillet = doc.getObject("Fillet")  # Chamfer will be applied after fillet

# Create Chamfer feature
chamfer = body.newObject("PartDesign::Chamfer", "Chamfer")

# Assign base object and edge list (replace with actual valid edges)
chamfer.Base = (fillet, ["Face19"])  # ← Replace with real edge names

# Set chamfer distances
chamfer.Size = 1.0  # You can also use Size2 and useTwoDistances for asymmetric chamfer

# Recompute to apply chamfer
doc.recompute()



### Begin command Std_Export
__objs__ = []
__objs__.append(FreeCAD.getDocument("Unnamed").getObject("Body"))
import Mesh
if hasattr(Mesh, "exportOptions"):
    options = Mesh.exportOptions(u"/home/naveen/Desktop/Unnamed-Body.stl")
    Mesh.export(__objs__, u"/home/naveen/Desktop/Unnamed-Body.stl", options)
else:
    Mesh.export(__objs__, u"/home/naveen/Desktop/Unnamed-Body.stl")

del __objs__
### End command Std_Export

App.closeDocument("Unnamed")
App.setActiveDocument("")
### End of Code ###