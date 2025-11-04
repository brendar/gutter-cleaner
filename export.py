import FreeCAD
import Mesh

# Open the FreeCAD document
doc = FreeCAD.openDocument("gutter-cleaner.FCStd")

# List of object labels to export
labels_to_export = ["coupler", "shop-vac-adapter", "nozzle"]

# Export each object individually
for label in labels_to_export:
    objects = doc.getObjectsByLabel(label)
    
    if not objects:
        raise ValueError(f"Object with label '{label}' not found in document")
    
    obj = objects[0]  # Get the first object with this label
    output_file = f"stl/{label}.stl"
    Mesh.export([obj], output_file)
    print(f"Exported {label} to {output_file}")


# Find the VarSet
varset = doc.getObject("VarSet")

if varset is None:
    raise ValueError("VarSet object not found in document")

# Ensure this stays larger than pc_tube_fit_min, otherwise the model will break
varset.pc_tube_fit_max = 2.0 

# Loop through pc_tube_fit_min values 0.1 to 1.0 in 0.1 increments
for i in range(1, 11):
    value = i * 0.1
    
    # Modify the attribute
    varset.pc_tube_fit_min = value
    print(f"\nSet pc_tube_fit_min to {value}")
    
    # Recompute the document to apply changes
    recompute_success = doc.recompute()
    if not recompute_success:
        raise RuntimeError(f"Document recomputation failed for pc_tube_fit_min={value}")
    print("Document recomputed successfully")
    
    # Export fit-check-ring with value in filename
    objects = doc.getObjectsByLabel("fit-check-ring")
    
    if not objects:
        raise ValueError("Object with label 'fit-check-ring' not found in document")
    
    obj = objects[0]
    output_file = f"stl/fit-check-rings/fit-check-ring-{value:.1f}-mm.stl"
    
    Mesh.export([obj], output_file)
    print(f"Exported fit-check-ring to {output_file}")


# Close the document
FreeCAD.closeDocument(doc.Name)
print("Export complete!")
exit()

