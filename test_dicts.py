
value = {'name': 'brett', 'version': 'stuff'}
allowed_keys = {'name', 'version', 'description', 'authors'}

any_test_case = any(key in value for key in allowed_keys)
print("any_test_case: " + str(any_test_case))
any_not_in_test_case = any(key in value for key in allowed_keys)
print("any_not_in_test_case: " + str(any_not_in_test_case))
all_test_case = all(key in value for key in allowed_keys)
print("all_test_case: " + str(all_test_case))
all_not_in_test_case = all(key in value for key in allowed_keys)
print("all_not_in_test_case: " + str(all_not_in_test_case))
if (not isinstance(value, dict) or
    not any(key in value for key in allowed_keys)):
    raise ValueError("package must be a dictionary with allowed keys: 'name', 'version', 'description', 'authors'")