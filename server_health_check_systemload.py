#!/usr/bin/env python3

from server_health_builtcomponents import check_system_cpu_temperature, check_system_memory_free, check_system_memory_available, check_system_memory_total, insert_systemload_db

system_memory_type = "Kibibyte"

#cpu temperature block
system_cpu_temperature = check_system_cpu_temperature()

if system_cpu_temperature[0] == 400:
    cpu_temperature = -1
elif system_cpu_temperature[0] == 200:
    cpu_temperature = system_cpu_temperature[1]

#total system memory block
system_memory_total = check_system_memory_total()

if system_memory_total[0] == 400:
    memory_total = -1
elif system_memory_total[0] == 200:
    memory_total = system_memory_total[1]

#available system memory block
system_memory_available = check_system_memory_available()

if system_memory_available[0] == 400:
    memory_available = -1
elif system_memory_available[0] == 200:
    memory_available = system_memory_available[1]

#free system memory block
system_memory_free = check_system_memory_free()

if system_memory_free[0] == 400:
    memory_free = -1
elif system_memory_free[0] == 200:
    memory_free = system_memory_free[1]

#try inserting system stats into db
try:

    insert_systemload_db(system_cpu_temperature[0], cpu_temperature, system_memory_type, system_memory_total[0], memory_total, system_memory_available[0], memory_available, system_memory_free[0], memory_free)

except Exception as error_on_runnin_system_check:

    print(f"Error: {error_on_runnin_system_check}")