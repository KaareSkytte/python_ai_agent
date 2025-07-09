from functions.get_files_info import get_files_info

# Call 1: get_files_info("calculator", ".")
print("Result for current directory:")
print(get_files_info("calculator", "."))

# Call 2: get_files_info("calculator", "pkg") 
print("Result for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))

# Call 3: get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
print(get_files_info("calculator", "/bin"))

# Call 4: get_files_info("calculator", "../")
print("Result for '../' directory:")
print(get_files_info("calculator", "../"))