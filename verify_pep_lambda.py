from pep_lambda import lambda_handler

result = lambda_handler({'prid': 103}, None)

print('result calling lambda_handler:')
print(result)
