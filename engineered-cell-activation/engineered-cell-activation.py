# Engineered Cell Activation Protocol    Version 0.1.12
# 
# A protocol for measuring the concentration at which an input molecule activates an engineered cell.
# 
# Developed by Cesar A. Rodriguez
#


import json
from autoprotocol.protocol import Protocol

# New Protocol object
protocol = Protocol()

# Container IDs

# Engineered Cells
e_cells_id = ""

# Negative Control Cells
nc_cells_id = ""

# No Antibiotic Resistance Cells - Used to confirm that the antibiotic added to the media is effective
no_abx_cells_id = ""

# Antibiotic
antibiotic_id = ""

# Tubes of LB Medium
lb_medium_a_id = ""
lb_medium_b_id = ""
lb_medium_c_id = ""

# Deionized Water
water_id = ""

# Input Molecule
input_molecule_id = ""

# Containers
e_cells = protocol.ref("e_cells", id=e_cells_id, cont_type="micro-2.0", storage="cold_4")
nc_cells = protocol.ref("nc_cells", id=nc_cells_id, cont_type="micro-2.0", storage="cold_4")
no_abx_cells = protocol.ref("no_abx_cells", id=no_abx_cells_id, cont_type="micro-2.0", storage="cold_4")

antibiotic = protocol.ref("antibiotic", id=antibiotic_id, cont_type="micro-1.5", storage="cold_4")

lb_medium_a = protocol.ref("lb_medium_a", id=lb_medium_a_id, cont_type="micro-2.0", discard=True)
lb_medium_b = protocol.ref("lb_medium_b", id=lb_medium_b_id, cont_type="micro-2.0", discard=True)
lb_medium_c = protocol.ref("lb_medium_c", id=lb_medium_c_id, cont_type="micro-2.0", storage="cold_4")

measurement_plate = protocol.ref("measurement_plate", cont_type="96-flat", discard=True)

water = protocol.ref("water", id=water_id, cont_type="micro-1.5", discard=True)
input_molecule = protocol.ref("input_molecule", id=input_molecule_id, cont_type="micro-1.5", storage="cold_4")

# This line is due to a bug in the verification algorithm.  Should be removed when the bug is fixed.
#lb_medium_c.well("A1").set_volume("1200:microliter")

# Step 1 - Add antibiotic to LB medium
protocol.transfer(antibiotic.well("A1"), lb_medium_a.well("A1"), "2:microliter")
protocol.transfer(antibiotic.well("A1"), lb_medium_b.well("A1"), "2:microliter")
protocol.transfer(antibiotic.well("A1"), lb_medium_c.well("A1"), "2:microliter")

# Step 2 - Add LB medium with antibiotic to the measurement plate
protocol.distribute(lb_medium_a.well("A1"), measurement_plate.wells_from("A1", 10), "150:microliter")
protocol.distribute(lb_medium_b.well("A1"), measurement_plate.wells_from("C1", 10), "150:microliter")
protocol.distribute(lb_medium_c.well("A1"), measurement_plate.wells_from("E1", 3), "150:microliter")

# Step 3 - Add the engineered cells to the measurement plate
protocol.transfer(e_cells.well("A1"), measurement_plate.wells_from("A1", 10), "30:microliter", mix_after=True)

# Step 4 - Add the negative control cells to the measurement plate
protocol.transfer(nc_cells.well("A1"), measurement_plate.wells_from("C1", 10), "30:microliter", mix_after=True)

# Step 5 - Add no antibiotic resistance cells to the measurement plate
protocol.distribute(no_abx_cells.well("A1"), measurement_plate.wells_from("E1", 3), "30:microliter")

# Step 6 - Measure indirectly cell concentration
protocol.absorbance(measurement_plate, measurement_plate.wells_from("A1", 10) , "600:nanometer","Before Growth - Engineered Cells")
protocol.absorbance(measurement_plate, measurement_plate.wells_from("C1", 10) , "600:nanometer","Before Growth - Negative Control Cells")
protocol.absorbance(measurement_plate, measurement_plate.wells_from("E1", 3) , "600:nanometer","Before Growth - No Antibiotic Resistance Cells")

# Step 7 - Grow cells
protocol.cover(measurement_plate, lid="standard")
protocol.incubate(measurement_plate, "warm_37", "2:hour", shaking=True)
protocol.uncover(measurement_plate)

# Step 8 - Measure indirectly cell concentration
protocol.absorbance(measurement_plate, measurement_plate.wells_from("A1", 10) , "600:nanometer","After Growth - Engineered Cells")
protocol.absorbance(measurement_plate, measurement_plate.wells_from("C1", 10) , "600:nanometer","After Growth - Negative Control Cells")
protocol.absorbance(measurement_plate, measurement_plate.wells_from("E1", 3) , "600:nanometer","After Growth - No Antibiotic Resistance Cells")


# Step 9 - Add water to the measurement plate
protocol.distribute(water.well("A1"), measurement_plate.wells_from("H2", 8), "180:microliter")

# Step 10 - Dilute the input molecule
protocol.transfer(input_molecule.well("A1"), measurement_plate.well("H1"), "200:microliter")
protocol.transfer(measurement_plate.well("H1"), measurement_plate.well("H2"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H2"), measurement_plate.well("H3"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H3"), measurement_plate.well("H4"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H4"), measurement_plate.well("H5"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H5"), measurement_plate.well("H6"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H6"), measurement_plate.well("H7"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H7"), measurement_plate.well("H8"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H8"), measurement_plate.well("H9"), "20:microliter", mix_after=True)

# Step 11 - Add the input molecules to the engineered cells
protocol.transfer(measurement_plate.well("H1"), measurement_plate.well("A1"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H2"), measurement_plate.well("A2"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H3"), measurement_plate.well("A3"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H4"), measurement_plate.well("A4"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H5"), measurement_plate.well("A5"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H6"), measurement_plate.well("A6"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H7"), measurement_plate.well("A7"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H8"), measurement_plate.well("A8"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H9"), measurement_plate.well("A9"), "20:microliter", mix_after=True)

# Step 12 - Add the input molecules to the negative control cells
protocol.transfer(measurement_plate.well("H1"), measurement_plate.well("C1"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H2"), measurement_plate.well("C2"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H3"), measurement_plate.well("C3"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H4"), measurement_plate.well("C4"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H5"), measurement_plate.well("C5"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H6"), measurement_plate.well("C6"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H7"), measurement_plate.well("C7"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H8"), measurement_plate.well("C8"), "20:microliter", mix_after=True)
protocol.transfer(measurement_plate.well("H9"), measurement_plate.well("C9"), "20:microliter", mix_after=True)

# Step 13 - Cells respond
protocol.cover(measurement_plate, lid="standard")
protocol.incubate(measurement_plate, "warm_37", "2:hour", shaking=True)
protocol.uncover(measurement_plate)

# Step 14 - Measure the bulk response of the cell population
protocol.fluorescence(measurement_plate, meaurement_plate.wells_from("A1", 10), excitation="450:nanometer", emission="460:nanometer", dataref="Response - Engineered Cells - 460 nm")
protocol.fluorescence(measurement_plate, meaurement_plate.wells_from("A1", 10), excitation="450:nanometer", emission="470:nanometer", dataref="Response - Engineered Cells - 470 nm")
protocol.fluorescence(measurement_plate, meaurement_plate.wells_from("A1", 10), excitation="450:nanometer", emission="480:nanometer", dataref="Response - Engineered Cells - 480 nm")

protocol.fluorescence(measurement_plate, meaurement_plate.wells_from("C1", 10), excitation="450:nanometer", emission="460:nanometer", dataref="Response - Negative Control Cells - 460 nm")
protocol.fluorescence(measurement_plate, meaurement_plate.wells_from("C1", 10), excitation="450:nanometer", emission="470:nanometer", dataref="Response - Negative Control Cells - 470 nm")
protocol.fluorescence(measurement_plate, meaurement_plate.wells_from("C1", 10), excitation="450:nanometer", emission="480:nanometer", dataref="Response - Negative Control Cells - 480 nm")

protocol.absorbance(measurement_plate, measurement_plate.wells_from("A1", 10) , "600:nanometer","After Response - Engineered Cells")
protocol.absorbance(measurement_plate, measurement_plate.wells_from("C1", 10) , "600:nanometer","After Response - Negative Control Cells")
protocol.absorbance(measurement_plate, measurement_plate.wells_from("E1", 3) , "600:nanometer","After Response - No Antibiotic Resistance Cells")

# Step 15 - Measure the response per cell
# Under development

print json.dumps(protocol.as_dict(), indent=2)