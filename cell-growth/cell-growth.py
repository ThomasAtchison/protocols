# Cell Growth Protocol    Version 0.3.0

import json
from autoprotocol.protocol import Protocol

# New Protocol object
protocol = Protocol()

# Container IDs

# Engineered Cells
e_cells_id = ""

# Negative Control Cells
nc_cells_id = ""

# Tubes of LB Medium
lb_medium_a_id = ""
lb_medium_b_id = ""
lb_medium_c_id = ""

# Containers
e_cells = protocol.ref("e_cells", id=e_cells_id, cont_type="micro-2.0", storage="cold_4")
nc_cells = protocol.ref("nc_cells", id=nc_cells_id, cont_type="micro-2.0", discard=True)

lb_medium_a = protocol.ref("lb_medium_a", id=lb_medium_a_id, cont_type="micro-2.0", discard=True)
lb_medium_b = protocol.ref("lb_medium_b", id=lb_medium_b_id, cont_type="micro-2.0", discard=True)
lb_medium_c = protocol.ref("lb_medium_c", id=lb_medium_c_id, cont_type="micro-2.0", storage="cold_4")

growth_plate = protocol.ref("growth_plate", cont_type="96-deep", storage="cold_4")
measurement_plate = protocol.ref("measurement_plate", cont_type="96-flat", discard=True)

# This line is due to a bug in the verification algorithm.  Should be removed when the bug is fixed.
lb_medium_c.well("A1").set_volume("1200:microliter")

# Step 1 - Add media to the growth plate for the engineered cells
protocol.transfer(lb_medium_a.well("A1"), growth_plate.well("A1"), "900:microliter")
protocol.transfer(lb_medium_a.well("A1"), growth_plate.well("A1"), "885:microliter")

# Step 2 - Add media to the growth plate for the negative control cells
protocol.transfer(lb_medium_b.well("A1"), growth_plate.well("H1"), "900:microliter")
protocol.transfer(lb_medium_b.well("A1"), growth_plate.well("H1"), "885:microliter")

# TODO - Add antibiotic

# Step 3 - Add the engineered cells to the growth plate and mix
protocol.transfer(e_cells.well("A1"), growth_plate.well("A1"),"30:microliter", mix_after=True)

# Step 4 - Add the negative control cells to the growth plate and mix
protocol.transfer(nc_cells.well("A1"), growth_plate.well("H1"),"30:microliter", mix_after=True)

# Step 5 - Add the engineered cells to the measurement plate
protocol.distribute(growth_plate.well("A1"), measurement_plate.wells_from("A1", 3, columnwise=False), "100:microliter")

# Step 6 - Add the negative control cells to the measurement plate
protocol.distribute(growth_plate.well("H1"), measurement_plate.wells_from("C1", 3, columnwise=False), "100:microliter")

# Step 7 - Add LB medium to the measurement plate
protocol.distribute(lb_medium_c.well("A1"), measurement_plate.wells_from("E1", 3, columnwise=False), "100:microliter")

# Step 8 - Cover the growth plate
protocol.cover(growth_plate, lid="standard")

# Step 9 - Grow new engineered and negative control cells
protocol.incubate(growth_plate, "warm_37", "5:hour", shaking=True)

# Step 10 - Measure indirectly cell concentrations
protocol.absorbance(measurement_plate, ["A1", "A2", "A3", "C1", "C2", "C3", "E1", "E2", "E3",], "600:nanometer","Before Incubation")

# Step 11 - Cover the measurement plate
protocol.cover(measurement_plate, lid="standard")

# Step 12 - Store the measurement plate in the fridge
# This step is being run in series instead of parallel.  Will uncomment it when it runs in parallel.
# The measurement plate remains covered and in room temperature while the growth plate is in the incubator.
#protocol.incubate(measurement_plate, "cold_4", "4:hour")

# Step 13 - Uncover the growth plate
protocol.uncover(growth_plate)

# Step 14 - Uncover the measurement plate
protocol.uncover(measurement_plate)

# Step 15 - Add engineered cells to the measurement plate again
protocol.distribute(growth_plate.well("A1"), measurement_plate.wells_from("A10", 3, columnwise=False), "100:microliter")

# Step 16 - Add negative control cells to the measurement plate again
protocol.distribute(growth_plate.well("H1"), measurement_plate.wells_from("C10", 3, columnwise=False), "100:microliter")

# Step 17 - Add LB medium to the measurement plate again
protocol.distribute(lb_medium_c.well("A1"), measurement_plate.wells_from("E10", 3, columnwise=False), "100:microliter")

# Step 18 - Cover the growth plate
protocol.cover(growth_plate, lid="standard")

# Step 19 - Measure indirectly cell concentrations
protocol.absorbance(measurement_plate, ["A10", "A11", "A12", "C10", "C11", "C12", "E10", "E11", "E12",], "600:nanometer","After Incubation")


print json.dumps(protocol.as_dict(), indent=2)