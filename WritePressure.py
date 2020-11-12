import os
import GlobalVariables as Parameters
import WriteBoundaryConditions as Header
import BoundaryConditions as boundary_conditions


def write_boundary_condition(BC, outlet_type, pressure, case_name, version):

    # create new boundary file
    file_id = open(os.path.join(case_name, '0', 'p'), 'w')

    # write header
    Header.write_boilerplate(file_id, version, 'p', 'volScalarField')

    # write dimensions and internfield
    initial_field = 'uniform ' + str(pressure)
    file_id.write('\ndimensions      [0 2 -2 0 0 0 0];\n\ninternalField   ' + initial_field + ';\n\n')

    # write boundary conditions
    file_id.write('boundaryField\n{\n')
    for key in BC:
        file_id.write('    ' + key + '\n    {\n')
        if BC[key] == Parameters.WALL:
            boundary_conditions.neumann(file_id)
        elif BC[key] == Parameters.OUTLET:
            if outlet_type == Parameters.NEUMANN:
                boundary_conditions.dirichlet(file_id, initial_field)
            elif outlet_type == Parameters.ADVECTIVE:
                boundary_conditions.advective(file_id)
            elif outlet_type == Parameters.INLET_OUTLET:
                boundary_conditions.dirichlet(file_id, initial_field)
        elif BC[key] == Parameters.SYMMETRY:
            boundary_conditions.neumann(file_id)
        elif BC[key] == Parameters.INLET:
            boundary_conditions.neumann(file_id)
        elif BC[key] == Parameters.CYCLIC:
            boundary_conditions.periodic(file_id)
        elif BC[key] == Parameters.EMPTY:
            boundary_conditions.empty(file_id)
        file_id.write('    }\n')

    file_id.write('}')
    file_id.close()