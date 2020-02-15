from _pynetworktables import NetworkTables

NetworkTables.initialize(server='roborio-XXX-frc.local')
robot_table = NetworkTables.getTable('SmartDashboard')